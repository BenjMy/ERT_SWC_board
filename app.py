import streamlit as st
import pandas as pd
import numpy as np

import visualisation
import contribute

# -- Set page config
apptitle = 'ER=f(SWC)'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")


# Sidebar Navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a page:', 
    ['Visualisation', 'Contribute'])

if options == 'Visualisation':
    visualisation.visualisation()
elif options == 'Contribute':
    contribute.contribute()


# -- Allow data download
#download = {'Time':bp_cropped.times, 'Strain':bp_cropped.value}
#df = pd.DataFrame(download)
#csv = df.to_csv(index=False)
#b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
#href = f'<a href="data:file/csv;base64,{b64}">Download Data as CSV File</a>'
#st.markdown(href, unsafe_allow_html=True)



st.subheader("About this app")
st.markdown("""
This app displays data downloaded from CAGS-data at https://github.com/agrogeophy/datasets .
""")

st.write('## Source Code, Bugs, Feature Requests')
githublink = """<a href='https://github.com/agrogeophy/datasets' target="_blank"> https://github.com/agrogeophy/datasets</a>"""
st.write(f'\n\nCheck out the GitHub Repo at: {githublink}. If you find any bugs or have suggestions, please open a new issue and I will look into it.', unsafe_allow_html=True)


