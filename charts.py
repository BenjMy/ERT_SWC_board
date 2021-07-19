import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
import plotly.express as px

def scatterAuthor(data_db, chosen_author):

    df= data_db.loc[data_db['Study ID'] == chosen_author]
    #fig, ax = plt.subplots()
    #df.plot(x ='WC', y='EC/ER raw', kind='scatter', xlabel='WC (g/g)', ylabel='EC (mS/m)',ax=ax)  
    #st.pyplot(fig)


    fig = px.scatter(x=df['WC'], y=df['EC/ER raw'])
    st.plotly_chart(fig, use_container_width=True)


#def scatterAll(data_db, chosen_author):
    
    #authorsId = data_db.loc[data_db['Study ID'].unique()
    # to implement