import streamlit as st
import pandas as pd
import numpy as np


def contribute():


	st.success('''
			 The ER=f(SWC) app is part of the Catalog of Agrogeophysical studies, 
		     please consider submitting your contribution as a whole to the Catalog
		     '''
		     )

	st.markdown("## Data preparation")

	st.info(" We opted for a couple yaml and csv file as data container")

	st.markdown('1. Formulate a yaml metadata file using the template here')

	st.markdown('https://github.com/BenjMy/skeppa')

	st.markdown("## Fill the following form")

	st.warning("All data must have a DOI")

	with st.form(key='my_form'):
		uploadedfile = st.file_uploader('metadata file', type=['.yaml'])
		uploadedfile = st.file_uploader(' ', type=['.csv'])
		surname = st.text_input(label='Surname')
		name = st.text_input(label='Name')
		email = st.text_input(label='Email')
		submit_button = st.form_submit_button(label='Submit')