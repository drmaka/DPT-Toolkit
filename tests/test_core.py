from dpt_toolkit.core import compute_dc,compute_qc
from dpt_toolkit.analysis import frontier,classify,distance_error_bound

def test_energy_values():
    dc=compute_dc(dict(time=3,concept=3,search=3,experiment=3,compute=3,coordination=3))
    assert dc['normalised']==.75
    qc=compute_qc([],[],method='units',L_R=40,L_Rq=8)
    assert qc['raw']==32 and qc['normalised']==.8

def test_frontier():
    r=[{'id':'q1','dc':.2,'qc':.1},{'id':'q2','dc':.5,'qc':.4},{'id':'q3','dc':.75,'qc':.8},{'id':'q4','dc':1,'qc':.5}]
    assert [x['id'] for x in frontier(r)]==['q1','q2','q3']
    assert classify(.75,.8)=='IV'
    assert round(distance_error_bound(.05,.05),4)==.1414
