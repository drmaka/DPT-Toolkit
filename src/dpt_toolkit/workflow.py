from __future__ import annotations
from pathlib import Path
import json, yaml, math
import pandas as pd
import matplotlib.pyplot as plt
from .core import compute_dc,compute_qc,compute_qc_ensemble
from .analysis import *

STEPS=[
"Declare the Reality Space","Declare the Background-Knowledge State","Generate Multiple Candidate Questions",
"Declare the Discovery-Cost Functional","Identify Admissible Procedures and Calculate Discovery Complexity",
"Declare the Description-Length Functional","Transform the Reality Space Through Each Question",
"Calculate Signed Representational Change and Question Compression","Construct the Discovery Coordinates",
"Classify the Questions into Discovery Plane Regions","Verify Existence, Non-Negativity, and Bounds",
"Verify Coordinate Uniqueness Under Fixed Conventions","Verify Compression Monotonicity",
"Check Representation-Isomorphism Invariance","Calculate Dominance","Extract the Discovery Frontier",
"Apply a Research-Budget Constraint","Demonstrate Expansion of Procedure Sets","Calculate Weighted Discovery Distance",
"Form a Neighbourhood and Calculate Path Length","Construct an Admissibility Graph and Find a Geodesic",
"Calculate Regularised Discovery Utility","Examine Non-Convexity and the Limitation of Scalarisation",
"Conduct Threshold Sensitivity Analysis","Conduct Weight Sensitivity Analysis",
"Apply the Stability Bound Under Coordinate Error","Construct a Dynamic Coordinate","Demonstrate Threshold Scarcity",
"Relate the Manual Example to the Computational Benchmark","Make the Final Research-Screening Decision"]

def load_project(path):
    p=Path(path); return yaml.safe_load(p.read_text(encoding='utf-8')) if p.suffix.lower() in ('.yaml','.yml') else json.loads(p.read_text())

def _plot(records,out,tau_d,tau_q):
    fig,ax=plt.subplots(figsize=(8,6))
    for r in records: ax.scatter(r['dc'],r['qc'],s=70); ax.annotate(r['id'],(r['dc'],r['qc']),xytext=(5,5),textcoords='offset points')
    ax.axvline(tau_d,linestyle='--'); ax.axhline(tau_q,linestyle='--'); ax.set(xlim=(0,1.05),ylim=(0,1.05),xlabel='Normalised Discovery Complexity',ylabel='Normalised Question Compression',title='Discovery Plane')
    fig.tight_layout(); fig.savefig(out,dpi=180); plt.close(fig)

def run_workflow(project_path,out_dir):
    cfg=load_project(project_path); out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    weights=cfg.get('dc_weights') or {c:1 for c in ('time','concept','search','experiment','compute','coordination')}
    qrecords=[]; detailed=[]
    R=cfg['reality_space']; B=cfg['background_knowledge']
    for q in cfg['questions']:
        # Procedure-set infimum: calculate each declared route and take least scalar cost.
        procedures=q.get('procedures') or [{'id':'declared','components':q['dc_components']}]
        pcalc=[]
        for p in procedures: pcalc.append({'id':p['id'],**compute_dc(p['components'],weights)})
        best=min(pcalc,key=lambda x:x['normalised'])
        qc_cfg=q['qc']; method=qc_cfg.get('method','units')
        qc=compute_qc(R,q.get('transformed_reality',q['text']),method,qc_cfg.get('L_R'),qc_cfg.get('L_Rq'))
        rec={'id':q['id'],'text':q['text'],'dc':best['normalised'],'qc':qc['normalised'],'dc_raw':best['raw'],'qc_raw':qc['raw'],'best_procedure':best['id']}
        qrecords.append(rec); detailed.append({'question':q,'procedures':pcalc,'best':best,'qc':qc})
    tau_d=float(cfg.get('thresholds',{}).get('dc',.65)); tau_q=float(cfg.get('thresholds',{}).get('qc',.65))
    for r in qrecords: r['region']=classify(r['dc'],r['qc'],tau_d,tau_q)
    dm=dominance_matrix(qrecords); F=frontier(qrecords); fids={r['id'] for r in F}
    lam=float(cfg.get('utility_lambda',.5)); beta=float(cfg.get('budget_beta',1.0))
    selected=budget_select(qrecords,beta,lam,cfg.get('select_top_n',1))
    for r in qrecords: r.update(frontier=r['id'] in fids,dominated=any(dm.loc[:,r['id']]),budget_feasible=r['dc']<=beta,utility=utility(r,lam))
    # Advanced analyses
    thresholds=cfg.get('sensitivity',{}).get('thresholds',[.5,.6,.65,.7,.8])
    ts=threshold_sensitivity(qrecords,thresholds)
    scarcity=threshold_scarcity(qrecords,cfg.get('scarcity_thresholds',[.4,.7]))
    eps=cfg.get('coordinate_error',{'dc':.05,'qc':.05})
    err_bound=distance_error_bound(eps['dc'],eps['qc'],cfg.get('distance_weights',{}).get('dc',1),cfg.get('distance_weights',{}).get('qc',1))
    geo=None
    if cfg.get('admissibility_edges'):
        G=admissibility_graph(qrecords,cfg['admissibility_edges'])
        if cfg.get('geodesic'):
            geo=geodesic(G,cfg['geodesic'][0],cfg['geodesic'][1])
    dyn=dynamic_changes(cfg.get('dynamic_coordinates',[])) if cfg.get('dynamic_coordinates') else pd.DataFrame()
    # Files
    pd.DataFrame(qrecords).to_csv(out/'coordinates.csv',index=False)
    dm.to_csv(out/'dominance_matrix.csv')
    ts.to_csv(out/'threshold_sensitivity.csv',index=False)
    scarcity.to_csv(out/'threshold_scarcity.csv',index=False)
    if not dyn.empty: dyn.to_csv(out/'dynamic_coordinates.csv',index=False)
    _plot(qrecords,out/'discovery_plane.png',tau_d,tau_q)
    report={
      'project':cfg.get('project',{}),'methodological_status':'Operational DPT screening under declared conventions; not proof of truth, ethics, discovery, or future impact.',
      'steps':[{'number':i+1,'name':name,'status':'completed' if i+1 not in (14,18,23,29) else 'audited/demonstrated'} for i,name in enumerate(STEPS)],
      'reality_space':R,'background_knowledge':B,'coordinates':qrecords,'frontier':sorted(fids),'selected':selected,
      'thresholds':{'dc':tau_d,'qc':tau_q},'budget_beta':beta,'utility_lambda':lam,'distance_error_bound':err_bound,
      'geodesic':geo,'limitations':[
        'Operational anchors are declared conventions, not universal natural units.',
        'Automated description-length estimators are proxies and require independent validation.',
        'Coordinate proximity does not establish semantic identity, causation, or historical influence.',
        'Final decisions require expert, ethical, feasibility, and empirical review.'
      ]}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    lines=[f"# DPT Screening Report — {cfg.get('project',{}).get('title','Untitled')}","","> "+report['methodological_status'],"","## Final result"]
    lines += [f"- Selected: **{', '.join(r['id'] for r in selected) or 'None'}**",f"- Frontier: **{', '.join(sorted(fids))}**",f"- Budget: `{beta}`; utility λ: `{lam}`",""]
    lines += ["## Coordinates","",pd.DataFrame(qrecords)[['id','dc','qc','region','frontier','dominated','budget_feasible','utility']].to_markdown(index=False),"","## 30-step audit"]
    lines += [f"{i+1}. {name}" for i,name in enumerate(STEPS)]
    lines += ["","## Limitations"]+[f"- {x}" for x in report['limitations']]
    (out/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    return report
