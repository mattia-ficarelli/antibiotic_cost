
import pandas as pd
import requests
from datetime import datetime
import urllib.request
import json
import plotly
import plotly.express as px


# Generate Data

#API Query Start
url_0501013B0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501013B0&format=json"
response_0501013B0 = urllib.request.urlopen(url_0501013B0)
data_0501013B0 = json.loads(response_0501013B0.read())
flat_data_0501013B0 = pd.json_normalize(data_0501013B0)
flat_data_0501013B0 = flat_data_0501013B0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501013B0 = flat_data_0501013B0.drop(columns=['items', 'quantity'])
flat_data_0501013B0 .rename(columns={'actual_cost': 'Amoxicillin'}, inplace=True)

url_0501030I0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501030I0&format=json"
response_0501030I0 = urllib.request.urlopen(url_0501030I0)
data_0501030I0 = json.loads(response_0501030I0.read())
flat_data_0501030I0 = pd.json_normalize(data_0501030I0)
flat_data_0501030I0 = flat_data_0501030I0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501030I0 = flat_data_0501030I0.drop(columns=['items', 'quantity'])
flat_data_0501030I0.rename(columns={'actual_cost': 'Doxycycline Hyclate'}, inplace=True)
flat_data_0501030I0

url_0501021L0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501021L0&format=json"
response_0501021L0 = urllib.request.urlopen(url_0501021L0)
data_0501021L0 = json.loads(response_0501021L0.read())
flat_data_0501021L0= pd.json_normalize(data_0501021L0)
flat_data_0501021L0 = flat_data_0501021L0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501021L0 = flat_data_0501021L0.drop(columns=['items', 'quantity'])
flat_data_0501021L0.rename(columns={'actual_cost': 'Cefalexin'}, inplace=True)
flat_data_0501021L0
#API Query End

#Processing Plot 1
join_1 = flat_data_0501013B0.join(flat_data_0501030I0, lsuffix='row_id', rsuffix='row_id')
all_antibiotics_merged = join_1.join(flat_data_0501021L0, lsuffix='row_id', rsuffix='row_id')
all_antibiotics_merged.fillna(0, inplace=True)
all_antibiotics_merged['Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£)']= all_antibiotics_merged.iloc[:, -3:].sum(axis=1)
all_antibiotics = all_antibiotics_merged.reset_index()
all_antibiotics.rename(columns={'row_name': 'Clinical Commissioning Group (CCG)', 'row_id': 'CCG code', 'date': 'Date'}, inplace=True)
all_antibiotics_plot = all_antibiotics.groupby(['Date']).sum()
all_antibiotics_plot = all_antibiotics_plot.reset_index()
all_antibiotics_plot = all_antibiotics_plot.round(1)
#end

#Plot 1
pd.options.plotting.backend = "plotly"
fig = px.bar(all_antibiotics_plot, x='Date', y= ["Amoxicillin", "Doxycycline Hyclate", 'Cefalexin'],
color_discrete_sequence=["#003087", "#0072CE", "#41B6E6"],
labels={"value": "Cost (£)", "variable": "Antibiotic"},  
title= "Total cost of Amoxicillin, Doxycycline Hyclate, and Cefalexin (£) per month")
fig.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    autosize=True,
    margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
)
#End

#CCG pop from NHS digital 
csv_url = "https://files.digital.nhs.uk/40/2232E5/gp-reg-pat-prac-all.csv"
req = requests.get(csv_url)
url_content = req.content
csv_file = open('downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
df1 = pd.read_csv('downloaded.csv')
CCG_pop = df1.groupby(['CCG_CODE']).sum().reset_index()
CCG_pop.rename(columns={'CCG_CODE': 'CCG code', 'NUMBER_OF_PATIENTS': 'Number of patients registered at GP practices'}, inplace=True)
#end

#Processing Plot 2 
current_year = datetime.now().year
current_year_str = str(current_year)
all_antibiotics["Date"] = pd.to_datetime(all_antibiotics["Date"]).apply(lambda x: x.strftime("%Y"))
all_antibiotics_current_year = all_antibiotics.loc[all_antibiotics['Date'] == current_year_str]
df1 = all_antibiotics_current_year.groupby(["CCG code", "Clinical Commissioning Group (CCG)"]).sum()
df2 = df1.drop(columns=['Amoxicillin', 'Doxycycline Hyclate', 'Cefalexin'])
df3 = df2.reset_index()
df4 = df3.join(CCG_pop, rsuffix='CCG code')
df5 = df4.drop(columns=['CCG codeCCG code'])
df5["Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£) per 1000 GP registered patients"] = df5["Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£)"]/(df5["Number of patients registered at GP practices"]/1000)
df5.round(2)
df6 = df5.sort_values(by='Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£) per 1000 GP registered patients' , ascending=True)
#end

#Plot 2 
pd.options.plotting.backend = "plotly"
fig_2 = px.bar(df6, x='Clinical Commissioning Group (CCG)', y= "Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£) per 1000 GP registered patients",
title= "Total cost of Amoxicillin, Doxycycline Hyclate, and Cefalexin (£) per 1000 GP registered patients in %s" %current_year_str, color_discrete_sequence = ['#003087']*len(df6))
fig_2.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    autosize=True,
    margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
)
#end

# Write out to file (.html)
config = {"displayModeBar": False, "displaylogo": False}
plotly_obj = plotly.offline.plot(
    fig, fig_2, include_plotlyjs=False, output_type="div", config=config
)
with open("_includes/plotly_obj.html", "w") as file:
    file.write(plotly_obj)

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