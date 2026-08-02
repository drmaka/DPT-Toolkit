from __future__ import annotations
import math, itertools
from collections import defaultdict
import numpy as np
import pandas as pd
import networkx as nx

def classify(dc,qc,tau_d=.65,tau_q=.65):
    if dc < tau_d and qc < tau_q: return 'I'
    if dc < tau_d and qc >= tau_q: return 'II'
    if dc >= tau_d and qc < tau_q: return 'III'
    return 'IV'

def dominates(a,b,tol=1e-12):
    return a['dc'] <= b['dc']+tol and a['qc']+tol >= b['qc'] and (a['dc'] < b['dc']-tol or a['qc'] > b['qc']+tol)

def dominance_matrix(records):
    ids=[r['id'] for r in records]; out=pd.DataFrame(False,index=ids,columns=ids)
    for a,b in itertools.permutations(records,2): out.loc[a['id'],b['id']]=dominates(a,b)
    return out

def frontier(records):
    return [r for r in records if not any(dominates(o,r) for o in records if o['id']!=r['id'])]

def weighted_distance(a,b,w_d=1.0,w_q=1.0):
    if w_d<=0 or w_q<=0: raise ValueError('Distance weights must be positive')
    return math.sqrt(w_d*(a['dc']-b['dc'])**2+w_q*(a['qc']-b['qc'])**2)

def neighbourhood(records,qid,epsilon,w_d=1,w_q=1):
    q=next(r for r in records if r['id']==qid)
    return [(r['id'],weighted_distance(q,r,w_d,w_q)) for r in records if r['id']!=qid and weighted_distance(q,r,w_d,w_q)<epsilon]

def path_length(records,path,w_d=1,w_q=1):
    by={r['id']:r for r in records}
    return sum(weighted_distance(by[a],by[b],w_d,w_q) for a,b in zip(path,path[1:]))

def admissibility_graph(records,edges,w_d=1,w_q=1):
    by={r['id']:r for r in records}; G=nx.Graph()
    for r in records: G.add_node(r['id'])
    for e in edges:
        a,b=e[0],e[1]; length=e[2] if len(e)>2 and e[2] is not None else weighted_distance(by[a],by[b],w_d,w_q)
        G.add_edge(a,b,weight=float(length))
    return G

def geodesic(G,source,target):
    return {"path":nx.shortest_path(G,source,target,weight='weight'),"length":nx.shortest_path_length(G,source,target,weight='weight')}

def utility(record,lam=.5): return record['qc']-lam*record['dc']

def budget_select(records,beta,lam=.5,top_n=None):
    feasible=[dict(r,utility=utility(r,lam)) for r in records if r['dc']<=beta]
    feasible.sort(key=lambda r:(-r['utility'],-r['qc'],r['dc'],r['id']))
    return feasible if top_n is None else feasible[:top_n]

def threshold_sensitivity(records,thresholds):
    return pd.DataFrame([{'threshold':t,'question':r['id'],'region':classify(r['dc'],r['qc'],t,t)} for t in thresholds for r in records])

def weight_sensitivity(component_rows,weight_schemes):
    rows=[]
    for name,w in weight_schemes.items():
        denom=4*sum(w.values())
        for r in component_rows:
            dc=sum(r[c]*w[c] for c in w)/denom
            rows.append({'scheme':name,'question':r['id'],'dc':dc})
    return pd.DataFrame(rows)

def distance_error_bound(eps_d,eps_q,w_d=1,w_q=1): return 2*math.sqrt(w_d*eps_d**2+w_q*eps_q**2)

def dynamic_changes(time_records):
    rows=[]
    for qid,g in pd.DataFrame(time_records).sort_values('time').groupby('id'):
        prev=None
        for _,r in g.iterrows():
            d={'id':qid,'time':r.time,'dc':r.dc,'qc':r.qc,'delta_dc':None,'delta_qc':None}
            if prev is not None: d.update(delta_dc=r.dc-prev.dc,delta_qc=r.qc-prev.qc)
            rows.append(d); prev=r
    return pd.DataFrame(rows)

def threshold_scarcity(records,thresholds):
    n=len(records)
    return pd.DataFrame([{'threshold':t,'count':sum(r['qc']>=t for r in records),'proportion':sum(r['qc']>=t for r in records)/n if n else float('nan')} for t in thresholds])

def cohen_kappa(a,b,weights='quadratic'):
    a=np.asarray(a); b=np.asarray(b); cats=np.array(sorted(set(a)|set(b))); k=len(cats); idx={c:i for i,c in enumerate(cats)}
    O=np.zeros((k,k));
    for x,y in zip(a,b): O[idx[x],idx[y]]+=1
    O/=max(1,O.sum()); pa=O.sum(1); pb=O.sum(0); E=np.outer(pa,pb)
    if weights=='unweighted': W=np.ones((k,k))-np.eye(k)
    else:
        ii,jj=np.indices((k,k)); W=((ii-jj)/(max(1,k-1)))**2 if weights=='quadratic' else abs(ii-jj)/max(1,k-1)
    den=(W*E).sum(); return 1-(W*O).sum()/den if den else 1.0

def krippendorff_alpha_ordinal(matrix):
    """Ordinal alpha; rows=units, columns=coders, NaN allowed."""
    x=np.asarray(matrix,dtype=float); vals=sorted(set(x[~np.isnan(x)])); rank={v:i for i,v in enumerate(vals)}
    pairs=[]
    for row in x:
        r=row[~np.isnan(row)]
        pairs += [(u,v) for i,u in enumerate(r) for v in r[i+1:]]
    if not pairs:return float('nan')
    dist=lambda u,v:((rank[u]-rank[v])/max(1,len(vals)-1))**2
    Do=np.mean([dist(u,v) for u,v in pairs]); pooled=x[~np.isnan(x)]
    expected=[dist(u,v) for i,u in enumerate(pooled) for v in pooled[i+1:]]
    De=np.mean(expected) if expected else 0
    return 1-Do/De if De else 1.0

def icc_two_way_random(matrix):
    """ICC(2,1), rows=targets and columns=raters, complete matrix required."""
    X=np.asarray(matrix,dtype=float)
    if np.isnan(X).any(): raise ValueError('ICC requires complete ratings')
    n,k=X.shape; gm=X.mean(); rm=X.mean(1); cm=X.mean(0)
    msr=k*np.sum((rm-gm)**2)/(n-1); msc=n*np.sum((cm-gm)**2)/(k-1)
    mse=np.sum((X-rm[:,None]-cm[None,:]+gm)**2)/((n-1)*(k-1))
    return (msr-mse)/(msr+(k-1)*mse+k*(msc-mse)/n)
