from __future__ import annotations
import json, math, zlib
from pathlib import Path
from typing import Any, Iterable
import numpy as np
from .anchors import COMPONENTS

def _validate_score(x: float) -> float:
    x=float(x)
    if not 0 <= x <= 4: raise ValueError(f"DC component score {x} is outside 0..4")
    return x

def compute_dc(components: dict[str,float], weights: dict[str,float]|None=None) -> dict[str,Any]:
    """Compute weighted DC from six anchored component scores.

    Returns both the six-dimensional vector and scalar. Scalar is normalised to [0,1]
    by the theoretical maximum 4*sum(weights), not by the observed sample maximum.
    """
    missing=[c for c in COMPONENTS if c not in components]
    if missing: raise ValueError(f"Missing DC components: {missing}")
    vec={c:_validate_score(components[c]) for c in COMPONENTS}
    weights=weights or {c:1.0 for c in COMPONENTS}
    if any(float(weights.get(c,0))<=0 for c in COMPONENTS): raise ValueError("All DC weights must be positive")
    raw=sum(vec[c]*float(weights[c]) for c in COMPONENTS)
    max_raw=4*sum(float(weights[c]) for c in COMPONENTS)
    return {"vector":vec,"weights":weights,"raw":raw,"max_raw":max_raw,"normalised":raw/max_raw}

def _canonical_bytes(obj: Any) -> bytes:
    if isinstance(obj, (dict,list,tuple)): text=json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))
    else: text=str(obj)
    return text.encode('utf-8')

def description_length(obj: Any, method: str='units', declared_units: float|None=None) -> float:
    """Transparent description-length proxies.

    units: use declared auditable units; utf8: bytes; zlib: compressed bytes;
    graph_mdl: simple node/edge/attribute code length for node-link dicts.
    """
    if method=='units':
        if declared_units is None: raise ValueError("declared_units required for method='units'")
        if declared_units < 0: raise ValueError("Description length must be nonnegative")
        return float(declared_units)
    b=_canonical_bytes(obj)
    if method=='utf8': return float(len(b))
    if method=='zlib': return float(len(zlib.compress(b,9)))
    if method=='graph_mdl':
        if not isinstance(obj,dict): raise ValueError("graph_mdl expects {'nodes': [...], 'edges': [...]} representation")
        n=max(1,len(obj.get('nodes',[]))); m=len(obj.get('edges',[]))
        attrs=len(_canonical_bytes(obj))
        return float(math.log2(n+1)*n + math.log2(n*n+1)*m + math.log2(attrs+1))
    raise ValueError(f"Unknown description method: {method}")

def compute_qc(R: Any, Rq: Any, method: str='units', L_R: float|None=None, L_Rq: float|None=None) -> dict[str,Any]:
    before=description_length(R,method,L_R)
    after=description_length(Rq,method,L_Rq)
    delta=before-after
    qc=max(0.0,delta)
    return {"method":method,"L_R":before,"L_Rq":after,"delta_L":delta,"raw":qc,
            "normalised":qc/before if before>0 else 0.0,"compression_explanatory":delta>=0}

def compute_qc_ensemble(R: Any,Rq: Any,methods: Iterable[str],declared:dict[str,tuple[float,float]]|None=None) -> dict[str,Any]:
    results=[]
    for method in methods:
        vals=(declared or {}).get(method,(None,None))
        results.append(compute_qc(R,Rq,method,*vals))
    norms=[r['normalised'] for r in results]
    return {"estimators":results,"median_normalised":float(np.median(norms)),"range":[float(min(norms)),float(max(norms))]}

def normalise(value: float, scale: float) -> float:
    if scale<=0: raise ValueError("Scale must be positive")
    return float(value)/float(scale)
