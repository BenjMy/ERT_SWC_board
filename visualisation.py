import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
from charts import (scatterAuthorFit, 
                    scatterAuthorMulti, 
                    scatter_groupby, 
                    home_plot
                    )
from fit import fitArchie, fitArchie_leastsq

import pybtex
from pybtex.database import parse_file

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

import io
import six
import pybtex.database.input.bibtex
import pybtex.plugin


def visualisation():



    # Title the app
    # -------------

    st.markdown(" ## 🚧  Work in progress 🚧  ")

    st.title('Pedophysical model of ER')

    st.success(" #### 📢 We believe in research community efforts and value your contribution!")
    st.info("""


    - The app displays data downloaded from CAGS-data at https://github.com/agrogeophy/datasets. 
    - Data are part of published studies with a DOI.
    - Data were digitized or submitted by authors. 
    - Metadata associated with the data allows to filter the contributions.


    """)


    with st.expander("Quick start"):

    #st.markdown('## Quick start')

        st.markdown('''
                       1. Start selecting authors contribution

                       2. Add filters

                       3. Choose a law to fit the data

                       4. Export the metadata''')

    st.markdown('- - -')


    # load excel file db
    # ------------------
    # return panda dataframe of the different tabs
    # data_db = main tab containing the data 
    # metadata_db = metadata
    @st.cache
    def load_data_db():
        #data_csv = pd.read_csv('https://docs.google.com/spreadsheets/d/1ywiYpcGq-0D46Dh57XysYl43Vaj0GkTfvfxd7bfU6MY/edit#gid=869071723')
        #data_csv = pd.read_csv('cags-ec-wc - data.csv')
        data_db = pd.read_excel('cags-ec-wc.xlsx','data')
        data_db = data_db[data_db['Study ID'].notna()]

        metadata_db = pd.read_excel('cags-ec-wc.xlsx','metadata')
        layer_db = pd.read_excel('cags-ec-wc.xlsx','layer')

        reference_db = pd.read_excel('cags-ec-wc.xlsx','reference')
        reference_db = reference_db[reference_db['DOI'].notna()]


        soil_db = pd.read_excel('cags-ec-wc.xlsx','soil_list')
        soil_db.dropna(inplace=True)

        
        return data_db, metadata_db, layer_db, reference_db, soil_db


    # Load db
    # --------------------------------------------------------------------
    data_db, metadata_db, layer_db, reference_db, soil_db = load_data_db()


    # prepare FILTERS
    # ---------------

    # Get Soil texture from excel db file
    # ------------------------------------------------------
    soilTexture = soil_db['Soil Texture']
    soilGroupWRB = soil_db['Soil group WRB']

    # By Authors
    # ------------------------------------------------------
    authorsList = data_db['Study ID'].unique()
    authorsList = list(authorsList)
    authorsList.insert(0, 'all')


    # By year
    # ------------------------------------------------------
    yearList = reference_db['Year'].unique().astype(int)


    # Default lists for fitting data with pedotransferModel
    # ------------------------------------------------------
    pedotransferModel = ['Archie', 'Archie modified']





    # prepare for merging
    # --------------------
    data_db.set_index('Study ID', inplace=True)
    layer_db.set_index('Study ID', inplace=True)

    # combine the two tables based on Study Id
    db = data_db.combine_first(layer_db)

    db.reset_index(level=0, inplace=True)
    data_db.reset_index(level=0, inplace=True)
    layer_db.reset_index(level=0, inplace=True)




    # add FILTERS widgets
    # -------------------
    with st.expander("Data metadata"):

        table_metadata = tb_meta()
        st.markdown(table_metadata, unsafe_allow_html=True)




    st.sidebar.markdown("## Select Data")
    chosenAuthor = st.sidebar.multiselect('Select author', authorsList) #multiselect
    soilTexture = st.sidebar.multiselect('Selec soil Texture', soilTexture) 
    yearChoice = st.sidebar.slider('Selec year', int(2000), int(max(yearList)), (2000, 2022)) 

    bare_soil = st.sidebar.checkbox('ONLY bare soil')

    if bare_soil:
         st.write('Great!')


    # add GROUPBY widgets
    # -------------------
    st.sidebar.markdown("## GroupBY")
    group_by_list = ['soil texture', 'lab']
    groupBY = st.sidebar.multiselect('Group data by', group_by_list) #multiselect



    # Analysis
    # ---------
    st.sidebar.markdown("## Analysis")


    fit_manual = st.sidebar.checkbox("Fit Data")
    fit_least_square = st.sidebar.checkbox("Fit least square")


    with st.expander("Fitting routine"):

        st.write('To obtain best-fit estimates of Archie parameters, astraight line is fitted for log10(S) and log10(/rho_{s}) using the least-squares criterion.')


    chosen_law = st.sidebar.selectbox('Select pedotransfer model', pedotransferModel) #multiselect

    #st.markdown('$\\rho = a\\rho_{\\text{fl}}\\phi^{-m} S^{-n}$')
    #l = list(chosenAuthor.values())


    # DISPLAY results
    # ---------------

    #col1, col2 = st.columns([3, 1])


    #home_plot(db)


    if chosenAuthor:

        if chosenAuthor[0] == 'all':
            df_filter_author = db.loc[db['Study ID'].unique(), : ]

        else:
            df_filter_author = db.loc[db['Study ID'].isin(chosenAuthor), : ]



        fig, chart_placeholder = scatterAuthorMulti(df_filter_author)

        if fit_manual:
            sw, rhofit = fitArchie(df_filter_author)
            scatterAuthorFit(sw, rhofit, fig, chart_placeholder)

        if fit_least_square:
            fitArchie_leastsq(df_filter_author, chart_placeholder)
            #scatterAuthorFit(sw, rhofit, fig, chart_placeholder)


        st.info('### Code and reference to reproduce')

        code = pedotransfer_code(pedotransferModel)

        st.code(code, language="python")

        st.write('References')

        bib2write = bib_refs()


        st.markdown(bib2write, unsafe_allow_html=True)

        st.markdown('- - -')
        col1, col2 = st.columns([2, 1])
        col1.subheader("Download data")
        col2.subheader("Link to the Catalog")

        list_details = []
        for author in chosenAuthor:


            df_xlsx = to_excel(df_filter_author)
            col1.download_button(label='📥 Download Current Result',
                                 data=df_xlsx ,
                                 file_name= 'df_test.xlsx',
                                 key= str(author))



            df_ref_author = reference_db.loc[reference_db['Study ID']==author]
            col2.markdown('* [' + str(author) + '](https://agrogeophy.github.io/catalog/contribution_details.html?id=' + str(int(df_ref_author['CAGS id'])) + ')\n')
        st.markdown('- - -')



    if groupBY:

        if chosenAuthor:
            scatter_groupby(df_filter_author,grp=groupBY,chart_placeholder=chart_placeholder)
        else:
            st.warning('Need to select data first')







def pedotransfer_code(pedotransferModel):

    if 'Archie' in pedotransferModel:

        code = '''rho = rhof * a * phi**(-m) * sw**(-n) '''

    return code



def bib_refs(bibfile='modelsrefs.bib', author=''):



    pybtex_style = pybtex.plugin.find_plugin('pybtex.style.formatting', 'plain')()
    pybtex_html_backend = pybtex.plugin.find_plugin('pybtex.backends', 'html')()
    pybtex_parser = pybtex.database.input.bibtex.Parser()


    my_bibtex = parse_file(bibfile).to_string('bibtex')

    data = pybtex_parser.parse_stream(six.StringIO(my_bibtex))
    data_formatted = pybtex_style.format_entries(six.itervalues(data.entries))
    output = io.StringIO()
    pybtex_html_backend.write_to_stream(data_formatted, output)
    html = output.getvalue()

    return html



def to_excel(df):

    output = BytesIO()
    with pd.ExcelWriter("path_to_file.xlsx") as writer:

        df.to_excel(writer, sheet_name="Sheet1")
    
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        #format1 = workbook.add_format({'num_format': '0.00'}) 
        #worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
    
    return processed_data


def tb_meta():

    tb = '''
                    <style type="text/css">
                    .tg  {border-collapse:collapse;border-spacing:0;}
                    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                      overflow:hidden;padding:10px 5px;word-break:normal;}
                    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
                      font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
                    .tg .tg-u1yq{background-color:#c0c0c0;font-weight:bold;text-align:center;vertical-align:top}
                    .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
                    .tg .tg-0lax{text-align:left;vertical-align:top}
                    </style>
                    <table class="tg">
                    <thead>
                      <tr>
                        <th class="tg-u1yq">Name</th>
                        <th class="tg-u1yq">Definition</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="tg-0pky">Author name</td>
                        <td class="tg-0pky"></td>
                      </tr>
                      <tr>
                        <td class="tg-0pky">Study DOI</td>
                        <td class="tg-0pky"></td>
                      </tr>
                      <tr>
                        <td class="tg-0pky">Crop type</td>
                        <td class="tg-0pky"></td>
                      </tr>
                      <tr>
                        <td class="tg-0pky">Drying/Wetting</td>
                        <td class="tg-0pky">Direction of varying water saturation</td>
                      </tr>
                      <tr>
                        <td class="tg-0lax">Pedophysical model</td>
                        <td class="tg-0lax">Pedophysical model used for fitting the data</td>
                      </tr>
                      <tr>
                        <td class="tg-0lax">Calibration type</td>
                        <td class="tg-0lax">Laboratory or litterature</td>
                      </tr>
                      <tr>
                        <td class="tg-0lax">Soil Texture</td>
                        <td class="tg-0lax"></td>
                      </tr>
                    </tbody>
                    </table>
             '''

    return tb
