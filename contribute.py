import streamlit as st
import pandas as pd
import numpy as np


def contribute():

	st.markdown("## Fill the following form")

	with st.form(key='my_form'):
		uploadedfile = st.file_uploader(' ', type=['.csv'])
		text_input = st.text_input(label='Enter some text')
		submit_button = st.form_submit_button(label='Submit')