"""Optional Streamlit interface: pip install -e '.[app]' && streamlit run app.py"""
import streamlit as st, tempfile, pathlib, pandas as pd
from dpt_toolkit.workflow import run_workflow
st.set_page_config(page_title='DPT Toolkit',layout='wide')
st.title('Discovery Plane Theory — 30-Step Toolkit')
st.caption('Transparent research-question screening under declared conventions')
f=st.file_uploader('Upload a DPT project YAML',type=['yaml','yml'])
if f:
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/'project.yaml'; p.write_bytes(f.getvalue())
        try:
            report=run_workflow(p,pathlib.Path(td)/'out')
            st.success('30-step audit completed')
            st.dataframe(pd.DataFrame(report['coordinates']),use_container_width=True)
            st.image(str(pathlib.Path(td)/'out'/'discovery_plane.png'))
            st.subheader('Selected question(s)'); st.write(report['selected'])
            st.download_button('Download JSON report',(pathlib.Path(td)/'out'/'report.json').read_bytes(),'dpt-report.json')
        except Exception as e: st.exception(e)
else:
    st.info('Start with examples/energy_case/project.yaml or run: dpt init my-project')
