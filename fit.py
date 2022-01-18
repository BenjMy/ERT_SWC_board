import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat




def fitArchie(df):

	sw= df['WC'].to_numpy().astype(float)

	st.sidebar.markdown('$\\rho = a\\rho_{\\text{fl}}\\phi^{-m} S^{-n}$')
	a = st.sidebar.slider('a', 0, 2, 1)	
	rhof = st.sidebar.slider('rhof', 0, 130, 25)
	phi = st.sidebar.slider('phi', 0.0, 1.0, 0.2)
	m = st.sidebar.slider('m', 0, 2, 2)
	n = st.sidebar.slider('n', 0, 2, 2)



	rho = rhof * a * phi**(-m) * sw**(-n)

	return sw, rho


def Archie_obj(x,y, rhof, a, phi, m, n):

	rho = rhof * a * phi**(-m) * y**(-n)

	return rho



def objective(x, a, b):
	return a * x + b



def fitArchie_leastsq(df,placeholder):
	'''
	... note:
		Assuming constant material and fluid properties (e.g.,m,n, and sigma_f), 
		Archie's law can be re-written in terms of the electrical resistivity at saturation (i.e.,S=1)

	'''

	#chart_placeholder = st.empty()


	fig, ax = plt.subplots()

	sw = df['WC'].to_numpy().astype(float)
	sigma = df['EC'].to_numpy().astype(float)

	sw_log = np.log10(sw)
	sigma_log = np.log10(sigma)

	rho_log = 1/sigma_log


	popt, pcov = curve_fit(objective, rho_log, sw_log)
	sigma_ab = np.sqrt(np.diagonal(pcov))

	a, b = popt
	# use optimal parameters to calculate new values

	x_new = rho_log
	y_new = objective(x_new, a, b)


	plt.plot(10**rho_log, 10**y_new, 'g--',
         label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
	plt.plot(10**rho_log, 10**sw_log, 'b.',
         label='raw: a=%5.3f, b=%5.3f' % tuple(popt))

	text_res = "Best fit parameters:\na = {}\nb = {}".format(a, b)
	print(text_res)

	a_conf = ufloat(popt[0], sigma_ab[0])
	b_conf = ufloat(popt[1], sigma_ab[1])

	bound_upper = objective(rho_log, *(popt + sigma_ab))
	bound_lower = objective(rho_log, *(popt - sigma_ab))
	# plotting the confidence intervals
	plt.fill_between(10**rho_log, 10**bound_lower, 10**bound_upper,
	                 color = 'black', alpha = 0.15)


	placeholder.pyplot(fig)


	return a_conf, b_conf, a, b
