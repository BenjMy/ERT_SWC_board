import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

from fit import fitArchie, fitArchie_leastsq


def scatterAuthorFit(sw, rhofit, fig, chart_placeholder):

    sigmafit = 1/rhofit * 1e3
    fig.add_trace(
        go.Scatter(
            x=sw,
            y=rhofit,
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False)
    )

    chart_placeholder.plotly_chart(fig, use_container_width=True)


def scatterAuthorMulti(df,
                        marker_type='Spatial ID', 
                        facet_type='Soil texture USDA',
                        loc=[]):

    # https://plotly.com/python/facet-plots/


    chart_placeholder = st.empty()

    fig = px.scatter(df, x='WC', y='EC/ER raw', color='Study ID',symbol=marker_type,
                 labels={ # replaces default labels by column name
                        "WC": 'WC (g/g)',  "EC/ER raw": 'EC (mS/m)'})
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    return fig, chart_placeholder



def scatter_groupby(df,grp,chart_placeholder=[]):

    if chart_placeholder is None:
        chart_placeholder = st.empty()

    group_by_list_eq = {'soil texture': 'Soil texture USDA',
                        'lab': 'Spatial ID'
                        }

    facet_col = group_by_list_eq[grp[0]]

    fig = px.scatter(df, x='WC', y='EC/ER raw', color='Study ID',symbol="Spatial ID",facet_col=facet_col,
                 labels={ # replaces default labels by column name
                        "WC": 'WC (g/g)',  "EC/ER raw": 'EC (mS/m)'})

    chart_placeholder.plotly_chart(fig, use_container_width=True)


    return fig, chart_placeholder




def home_plot(data_db):
    
    chart_placeholder = st.empty()

    a_mat = []
    b_mat = []
    lgd = []
    for author in data_db['Study ID'].unique():
        a_conf, b_conf, a, b = fitArchie_leastsq(data_db[data_db['Study ID']==author],chart_placeholder)
        a_mat.append(a)
        b_mat.append(b)
        lgd.append(author)
        

    archie_cols = {'a':a_mat, 'b':b_mat}
    archie_pd = pd.DataFrame(data=archie_cols)


    fig, ax = plt.subplots()
    cmap = plt.cm.jet

    for i, author in enumerate(data_db['Study ID'].unique()):
        plt.scatter(archie_pd['a'][i],archie_pd['b'][i], c=a_mat[i], cmap=cmap, label=lgd[i])
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    plt.title('Summary of Archie model fits')
    plt.legend(lgd)

    chart_placeholder.pyplot(fig)
