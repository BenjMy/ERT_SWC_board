import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
from charts import scatterAuthor
from fit import fitArchie

def visualisation():

    @st.cache
    def load_data_db():
        #data_csv = pd.read_csv('https://docs.google.com/spreadsheets/d/1ywiYpcGq-0D46Dh57XysYl43Vaj0GkTfvfxd7bfU6MY/edit#gid=869071723')
        #data_csv = pd.read_csv('cags-ec-wc - data.csv')
        data_db = pd.read_excel('cags-ec-wc.xlsx','data')
        metadata_db = pd.read_excel('cags-ec-wc.xlsx','metadata')
        layer_db = pd.read_excel('cags-ec-wc.xlsx','layer')
        
        return data_db, metadata_db, layer_db

    data_db, metadata_db, layer_db = load_data_db()

    # -- Default lists
    petroLawList = ['Archie']
    #textureClassList = ['H1','L1', 'V1']

    authorsList = data_db['Study ID'].unique()

    # Title the app
    st.title('ER=f(SWC) app')
    st.header('Author quickview')


    st.sidebar.markdown("## Select Data")
    chosen_author = st.sidebar.selectbox('Select author', authorsList) #multiselect

    st.sidebar.markdown("## Analysis")
    fit=st.sidebar.checkbox('Fit Data?')



    chosen_law = st.sidebar.selectbox('Select petrophysical relationship', petroLawList) #multiselect

    #st.markdown('$\\rho = a\\rho_{\\text{fl}}\\phi^{-m} S^{-n}$')

    st.write('study id:', chosen_author)

    # indiv chart 
    indiv_chart_fig = scatterAuthor(data_db, chosen_author)

    if fit:
        fitArchie()

    df_data = data_db.loc[data_db['Study ID'] == chosen_author]
    df_layer = layer_db.loc[layer_db['Study ID'] == chosen_author]
    df_metadata = metadata_db.loc[metadata_db['Study ID'] == chosen_author]

    json_meta = df_metadata.apply(lambda x: list(x.dropna()), axis=0).to_json()
    json_layer = df_layer.apply(lambda x: list(x.dropna()), axis=0).to_json()

    data = {'survey metadata' : json_meta, 'soil metadata' : json_layer }
    json_detail = json.dumps(data)

    with st.beta_expander("See metadata"):
        st.json(json_detail)



    st.table(df_data)


    st.header('Comparative quickview')
    # all contrib interactive chart 
    st.write('To implement - an interactive graph with all contribution + filters')
    #allInteractiveChart = scatterAll(data_db)