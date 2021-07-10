
import pandas as pd
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

url_0501021L0 = "https://openprescribing.net/api/1.0/spending_by_ccg/?code=0501021L0&format=json"
response_0501021L0 = urllib.request.urlopen(url_0501021L0)
data_0501021L0 = json.loads(response_0501021L0.read())
flat_data_0501021L0= pd.json_normalize(data_0501021L0)
flat_data_0501021L0 = flat_data_0501021L0.groupby(['row_name', 'row_id', 'date']).sum()
flat_data_0501021L0 = flat_data_0501021L0.drop(columns=['items', 'quantity'])
flat_data_0501021L0.rename(columns={'actual_cost': 'Cefalexin'}, inplace=True)
flat_data_0501021L0
#API Query End

join_1 = flat_data_0501013B0.join(flat_data_0501030I0, lsuffix='row_id', rsuffix='row_id')
all_amoxicillin_merged = join_1.join(flat_data_0501021L0, lsuffix='row_id', rsuffix='row_id')
all_amoxicillin_merged.fillna(0, inplace=True)
#all_amoxicillin_merged['Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin(£)']= all_amoxicillin_merged.iloc[:, -3:].sum(axis=1)
all_amoxicillin = all_amoxicillin_merged.reset_index()
all_amoxicillin.rename(columns={'row_name': 'Clinical Commissioning Group (CCG)', 'row_id': 'ODS code', 'date': 'Date'}, inplace=True)
all_amoxicillin_plot = all_amoxicillin.groupby(['Date']).sum()
all_amoxicillin_plot = all_amoxicillin_plot.reset_index()


pd.options.plotting.backend = "plotly"
fig = px.bar(all_amoxicillin_plot, x='Date', y= ["Amoxicillin", "Doxycycline Hyclate", 'Cefalexin'],
labels={"value": "Cost (£)", "variable": "Antibiotic"},  
title= "Total cost of Amoxicillin, Doxycycline Hyclate, and Cefalexin (£) per month")
fig.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    autosize=True,
    margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
)

# Asthetics of the plot
fig.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    autosize=True,
    margin=dict(l=50, r=50, b=50, t=50, pad=4, autoexpand=True),
    # height=1000,
    # hovermode="x",
)

# Add title and dynamic range selector to x axis
#fig.update_xaxes(
    #title_text="Date",
    #rangeselector=dict(
        #buttons=list(
           # [
                #dict(count=6, label="6m", step="month", stepmode="backward"),
               # dict(count=1, label="1y", step="year", stepmode="backward"),
                #dict(step="all"),
            #]
        #)
   # ),
#)

# Write out to file (.html)
config = {"displayModeBar": False, "displaylogo": False}
plotly_obj = plotly.offline.plot(
    fig, include_plotlyjs=False, output_type="div", config=config
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