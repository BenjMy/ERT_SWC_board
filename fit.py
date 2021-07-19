import streamlit as st


def fitArchie():

	st.sidebar.markdown('$\\rho = a\\rho_{\\text{fl}}\\phi^{-m} S^{-n}$')
	a = st.sidebar.slider('a', 0, 130, 25)	
	rhof = st.sidebar.slider('rhof', 0, 130, 25)
	phi = st.sidebar.slider('phi', 0, 130, 25)
	S = st.sidebar.slider('S', 0, 130, 25)
	m = st.sidebar.slider('m', 0, 130, 25)
	n = st.sidebar.slider('n', 0, 130, 25)