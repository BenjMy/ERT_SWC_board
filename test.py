import streamlit as st
import pandas as pd


@st.cache
def get_data():
    return pd.read_csv('https://datahub.io/core/gdp/r/gdp.csv')


st.text_input('Enter some text')
st.file_uploader('File uploader')
