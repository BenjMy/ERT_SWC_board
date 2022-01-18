import streamlit as st
from PIL import Image

import pandas as pd
import numpy as np

import visualisation
import contribute
import tryit

import pybtex
from pybtex.database import parse_file
import io
import six
import pybtex.database.input.bibtex
import pybtex.plugin



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



# -- Set page config


apptitle = 'Electrical Resistivity = f( Soil Water Content)'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")




# Sidebar Navigation
logo_CAGS = Image.open('img/CAGS.png')
st.sidebar.image(logo_CAGS, caption= "Catalog of Agrogeophysical Surveys")
#st.sidebar.markdown("![Catalog of Agrogeophysical Surveys](upload:img/CAGS.png)(https://agrogeophy.github.io/catalog/)")


st.sidebar.title('Navigation')
options = st.sidebar.radio('Select a page:', 
    ['Visualisation', 'Contribute', 'Try it'])


if options == 'Visualisation':
    visualisation.visualisation()
elif options == 'Contribute':
    contribute.contribute()
elif options == 'Try it':
    tryit.tryit()




st.write("""
## We welcome any feedback and ideas!
Let us know by submitting 
issues on Github https://agrogeophy.github.io/catalog/issues
or send us a message on our
Slack chatroom https://agrogeophy.slack.com/.
"""
)

st.markdown("""
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4058524.svg)](https://doi.org/10.5281/zenodo.4058524) [<img src="https://img.shields.io/badge/Slack-agrogeophy-1.svg?logo=slack">](https://agrogeophy.slack.com)""", unsafe_allow_html=True

)



st.write('#### References')
bib2write = bib_refs('apprefs.bib')
st.markdown(bib2write, unsafe_allow_html=True)



