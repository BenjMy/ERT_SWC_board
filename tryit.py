import streamlit as st
import pandas as pd
import numpy as np


def tryit():

	st.markdown("## Upload your data")

	with st.form(key='my_form'):
		uploadedfile = st.file_uploader(' ', type=['.csv'])
		submit_button = st.form_submit_button(label='Submit')