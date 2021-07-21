import urllib.request
from urllib.request import urlopen
import requests
import folium
import json
import copy
import pandas as pd
import plotly
import plotly.express as px
from datetime import datetime


#Plot 1 start
##API Query Start
###Amoxicillin(0501013B0) cost data
url_0501013B0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501013B0&format=json"
response_0501013B0 = urllib.request.urlopen(url_0501013B0)
data_0501013B0 = json.loads(response_0501013B0.read())
flat_data_0501013B0 = pd.json_normalize(data_0501013B0)
flat_data_0501013B0 = flat_data_0501013B0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501013B0 = flat_data_0501013B0.drop(columns=['items', 'quantity'])
flat_data_0501013B0 .rename(columns={'actual_cost': 'Amoxicillin'}, inplace=True)

###Doxycycline Hyclate(0501030I0) cost data
url_0501030I0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501030I0&format=json"
response_0501030I0 = urllib.request.urlopen(url_0501030I0)
data_0501030I0 = json.loads(response_0501030I0.read())
flat_data_0501030I0 = pd.json_normalize(data_0501030I0)
flat_data_0501030I0 = flat_data_0501030I0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501030I0 = flat_data_0501030I0.drop(columns=['items', 'quantity'])
flat_data_0501030I0.rename(columns={'actual_cost': 'Doxycycline Hyclate'}, inplace=True)

###Cefalexin(0501021L0) cost data
url_0501021L0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501021L0&format=json"
response_0501021L0 = urllib.request.urlopen(url_0501021L0)
data_0501021L0 = json.loads(response_0501021L0.read())
flat_data_0501021L0= pd.json_normalize(data_0501021L0)
flat_data_0501021L0 = flat_data_0501021L0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501021L0 = flat_data_0501021L0.drop(columns=['items', 'quantity'])
flat_data_0501021L0.rename(columns={'actual_cost': 'Cefalexin'}, inplace=True)
flat_data_0501021L0
##API Query End

##Data processing for plot 1
join_1 = flat_data_0501013B0.join(flat_data_0501030I0, lsuffix='row_id', rsuffix='row_id')
all_antibiotics_merged = join_1.join(flat_data_0501021L0, lsuffix='row_id', rsuffix='row_id')
all_antibiotics_merged.fillna(0, inplace=True)
all_antibiotics_merged['Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£)']= all_antibiotics_merged.iloc[:, -3:].sum(axis=1)
all_antibiotics = all_antibiotics_merged.reset_index()
all_antibiotics.rename(columns={'row_name': 'Clinical Commissioning Group (CCG)', 'row_id': 'CCG code', 'date': 'Date'}, inplace=True)
all_antibiotics_plot = all_antibiotics.groupby(['Date']).sum()
all_antibiotics_plot = all_antibiotics_plot.reset_index()
all_antibiotics_plot = all_antibiotics_plot.round(2)
##Data processing end

##Save data for plot 1 to csv
fig_1_data = all_antibiotics_plot.copy()
fig_1_data.rename(columns={
"Amoxicillin": "Cost (£) of Amozicillin",
"Doxycycline Hyclate": "Cost (£) of Doxycycline Hyclate", 
"Cefalexin": "Cost (£) of Cefalexin",
"Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£)": "Cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin"}, 
inplace=True)
fig_1_data.index.name = 'Unique ID'
fig_1_data.to_csv("assets/data/cost_antibiotics_per_month.csv", index=False)
##Save data end

##Visualization Plot 1
pd.options.plotting.backend = "plotly"
fig = px.bar(all_antibiotics_plot, x='Date', y= ["Amoxicillin", "Doxycycline Hyclate", 'Cefalexin'],
color_discrete_sequence=["#003087", "#0072CE", "#41B6E6"],
labels={"value": "Cost (£)", "variable": "Antibiotic"},  
title= "Cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per month")
fig.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    autosize=True,
    margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
)
##Visualization Plot 1 end

##Write out to file (.html) Plot 1
config = {"displayModeBar": False, "displaylogo": False}
plotly_obj = plotly.offline.plot(
    fig, include_plotlyjs=False, output_type="div", config=config
)
with open("_includes/plotly_obj.html", "w") as file:
    file.write(plotly_obj)
##Write out to file (.html) Plot 1 end
#Plot 1 end

#Plot 2 start
#Plot 2 end

# Grab timestamp
data_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Write out to file (.html)
html_str = (
    '<p><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill-rule="evenodd" d="M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM8 0a8 8 0 100 16A8 8 0 008 0zm.5 4.75a.75.75 0 00-1.5 0v3.5a.75.75 0 00.471.696l2.5 1a.75.75 0 00.557-1.392L8.5 7.742V4.75z"></path></svg> Latest Data: '
    + data_updated
    + "</p>"
)
with open("_includes/update.html", "w") as file:
    file.write(html_str)