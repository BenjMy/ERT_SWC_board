import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

from uncertainties import ufloat






def load_data_db():
    #data_csv = pd.read_csv('https://docs.google.com/spreadsheets/d/1ywiYpcGq-0D46Dh57XysYl43Vaj0GkTfvfxd7bfU6MY/edit#gid=869071723')
    #data_csv = pd.read_csv('cags-ec-wc - data.csv')
    data_db = pd.read_excel('cags-ec-wc.xlsx','data')
    metadata_db = pd.read_excel('cags-ec-wc.xlsx','metadata')
    layer_db = pd.read_excel('cags-ec-wc.xlsx','layer')
    reference_db = pd.read_excel('cags-ec-wc.xlsx','reference')
    reference_db = reference_db[reference_db['DOI'].notna()]
    
    return data_db, metadata_db, layer_db, reference_db

data_db, metadata_db, layer_db, reference_db = load_data_db()
# data_db.set_index('Study ID', inplace=True)

data_db = data_db[data_db['Study ID'].notna()]



layer_db.set_index('Study ID', inplace=True)
dbjoin = data_db.combine_first(layer_db)

dbjoin.reset_index(level=0, inplace=True)

#%%

# dbjoin = dbjoin.merge(metadata_db, on='Study ID',  how='outer')
import numpy as np
from scipy.optimize import curve_fit

def objective(x, a, b):
	return a * x + b


def fitArchie_leastsq(df):
	'''
	... note:
		Assuming constant material and fluid properties (e.g.,m,n, and sigma_f), 
		Archie's law can be re-written in terms of the electrical resistivity at saturation (i.e.,S=1)

	'''


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


	a_conf = ufloat(popt[0], sigma_ab[0])
	b_conf = ufloat(popt[1], sigma_ab[1])

	bound_upper = objective(rho_log, *(popt + sigma_ab))
	bound_lower = objective(rho_log, *(popt - sigma_ab))
	# plotting the confidence intervals
	plt.fill_between(10**rho_log, 10**bound_lower, 10**bound_upper,
	                 color = 'black', alpha = 0.15)
    
	return a_conf, b_conf, a, b




fitArchie_leastsq(data_db[data_db['Study ID']=='Celano et al_2011'])



#%%

# Summary of Archie model fits

a_mat = []
b_mat = []
lgd = []
for author in data_db['Study ID'].unique():
    a_conf, b_conf, a, b = fitArchie_leastsq(data_db[data_db['Study ID']==author])
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

#%%
metadata_db
layer_db

autorslist = data_db['Study ID'].unique()
autorslist = list(autorslist)
autorslist.append('all')

dict_authors = {0:"Celano et al_2011",
                1:"Jayawickreme et al_2010"
                }

l = list(dict_authors.values())


# df= dbjoin.loc[dbjoin['Study ID'].isin(l), : ]

# fig = px.scatter(df, x='WC', y='EC/ER raw', color='Study ID',symbol="Spatial ID",facet_col="Soil texture USDA",
#                  labels={ # replaces default labels by column name
#                         "WC": 'WC (g/g)',  "EC/ER raw": 'EC (mS/m)'})

# fig.show()

#st.plotly_chart(fig, use_container_width=True)


import pandas as pd
pd.options.plotting.backend = "plotly"

df = pd.DataFrame(dict(a=[1,3,2], b=[3,2,1]))
fig = df.plot()
fig.show()


import plotly.express as px

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", color="sex", symbol="smoker", facet_col="time",
          labels={"sex": "Gender", "smoker": "Smokes"})
fig.show()