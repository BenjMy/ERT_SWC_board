import streamlit as st
import pandas as pd
from bokeh.plotting import figure, output_file, show
import matplotlib.pyplot as plt



def load_data_db():
    #data_csv = pd.read_csv('https://docs.google.com/spreadsheets/d/1ywiYpcGq-0D46Dh57XysYl43Vaj0GkTfvfxd7bfU6MY/edit#gid=869071723')
    #data_csv = pd.read_csv('cags-ec-wc - data.csv')
    data_db = pd.read_excel('cags-ec-wc.xlsx','data')
    metadata_db = pd.read_excel('cags-ec-wc.xlsx','metadata')
    layer_db = pd.read_excel('cags-ec-wc.xlsx','layer')
    
    return data_db, metadata_db, layer_db

data_db, metadata_db, layer_db = load_data_db()

metadata_db
layer_db

data_db['Study ID'].unique()

fig, ax = plt.subplots()

df= data_db.loc[data_db['Study ID'] == 'Amidu et al_2007']
df.plot(x ='WC', y='EC/ER raw', kind='scatter', xlabel='WC (g/g)', ylabel='EC (mS/m)')	

