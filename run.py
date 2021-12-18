import urllib.request
from urllib.request import urlopen
from urllib import request as urlreq
import requests
import regex as re
import folium
import json
import pandas as pd
import plotly 
import plotly.express as px
import geopandas as gpd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

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
labels={"value": "Cost (£)", "variable": "Antibiotic:"})
fig.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    font = dict(family = "Arial", size = 16),
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
##CCG population data 
month_year_variable = datetime.now().strftime('%B-%Y').lower()
url = "https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice/%s" %month_year_variable 
response = urllib.request.urlopen(url)
soup = BeautifulSoup(response.read(), "lxml")
data = soup.select_one("a[href*='gp-reg-pat-prac-all.csv']")
if data != None: 
    csv_url = data['href']
    req = requests.get(csv_url)
    url_content = req.content
    csv_file = open('assets/data/ccg_pop.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()
else:
    last_month = datetime.now() - relativedelta(months=1)
    last_month_year_variable = last_month.strftime('%B-%Y').lower()
    url = "https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice/%s" %last_month_year_variable
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read(), "lxml")
    data = soup.select_one("a[href*='gp-reg-pat-prac-all.csv']")
    csv_url = data['href']
    req = requests.get(csv_url)
    url_content = req.content
    csv_file = open('assets/data/ccg_pop.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()
df1 = pd.read_csv('assets/data/ccg_pop.csv')
CCG_pop = df1.groupby(['CCG_CODE']).sum().reset_index()
CCG_pop.rename(columns={'CCG_CODE': 'CCG code', 'NUMBER_OF_PATIENTS': 'Number of patients registered at GP practices'}, inplace=True) 
##CCG population data end

##GeoJSON download
with urlopen('https://openprescribing.net/api/1.0/org_location/?org_type=ccg') as response:
    data_ccg_geojson = json.load(response)
##GeoJSON download end

##Data processing for plot 2
current_year = datetime.now().year
current_year_str = str(current_year)
all_antibiotics["Date"] = pd.to_datetime(all_antibiotics["Date"]).apply(lambda x: x.strftime("%Y"))
all_antibiotics_current_year = all_antibiotics.loc[all_antibiotics['Date'] == current_year_str]
df1 = all_antibiotics_current_year.groupby(["CCG code", "Clinical Commissioning Group (CCG)"]).sum()
df2 = df1.drop(columns=['Amoxicillin', 'Doxycycline Hyclate', 'Cefalexin'])
df3 = df2.reset_index()
df4 = df3.join(CCG_pop, rsuffix='CCG code')
df5 = df4.drop(columns=['CCG codeCCG code'])
df5.rename(columns = {"Total cost of Amoxicillin, Doxycycline Hyclate, Cefalexin (£)": "Cost (£) of Amoxicillin, Doxycycline Hyclate,and Cefalexin in %s" %current_year_str}, inplace=True)
df5["Cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per 1000 GP registered patients in %s" %current_year_str] = df5["Cost (£) of Amoxicillin, Doxycycline Hyclate,and Cefalexin in %s" %current_year_str]/(df5["Number of patients registered at GP practices"]/1000)
df6 = df5.reset_index(drop = True)
df7 = df6.rename(columns = {'CCG code': 'ODS CCG code'})
df7 = df7.round(2)
df7.index.name = 'Unique ID'
final_df = df7.copy()
##Data processing for plot 2 end

##Define function to download shapefiles/data from ONS Geoportal
def geo_json_download(input_num):
    full_url = url_start + data_url + '%s' %input_num  + url_end_base
    with urlopen(full_url) as response:
        geodf_map = gpd.read_file(response)
    return geodf_map
##Define function to download shapefiles/data from ONS Geoportal end

##Ingest CCG boundary GeoJSON from ONS Geoportal
current_year = datetime.now().strftime('%Y')
last_year = str(datetime.now().year -1)
url_start = "https://ons-inspire.esriuk.com"
search_url = url_start + "/arcgis/rest/services/Health_Boundaries/"
url_end_base = '/query?where=1%3D1&outFields=*&outSR=4326&f=json'
string_filter_base = "Clinical_Commissioning_Groups_[A-Za-z]+_"
try:
  response = urlreq.urlopen(search_url)
  soup = BeautifulSoup(response.read(), "lxml")
  data_url = soup.find_all('a', href=re.compile(string_filter_base + current_year))
  if not data_url:
    data_url = soup.find_all('a', href=re.compile(string_filter_base + last_year))
  data_url = data_url[-1].get('href')
  try:
    input_num = '/0'
    df_map = geo_json_download(input_num)
  except:
    input_num = '/1'
    df_map = geo_json_download(input_num)
except:
    print('HTTP error')
##Ingest CCG boundary GeoJSON from ONS Geoportal end 

##Ingest CCG ONS to ODS code mapping table from ONS Geoportal
url_start_cde_map = "https://services1.arcgis.com"
search_url_cde_map = url_start_cde_map + "/ESMARspQHYMw9BZ9/arcgis/rest/services/"
string_filter_cde_map_base = "CCG_[A-Za-z]+_"
string_filter_cde_map_end = '_EN_NC'
url_2_cde_map = '/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
try:
  response_cde_map = urlreq.urlopen(search_url_cde_map)
  soup_cde_map = BeautifulSoup(response_cde_map.read(), "lxml")
  data_url_cde_map = soup_cde_map.find_all('a', href=re.compile(string_filter_cde_map_base + current_year + string_filter_cde_map_end))
  if not data_url_cde_map:
    data_url_cde_map = soup_cde_map.find_all('a', href=re.compile(string_filter_cde_map_base + last_year + string_filter_cde_map_end))  
  data_url_cde_map = data_url_cde_map[-1].get('href')
  full_url_cde_map = url_start_cde_map + data_url_cde_map + url_2_cde_map
  with urlopen(full_url_cde_map) as response:
    ccg_code_map_json = json.load(response)
    ccg_code_map_df = pd.json_normalize(ccg_code_map_json['features'])
except:
    print('HTTP error')
##Ingest CCG ONS to ODS code mapping table from ONS Geoportal end 

##Prepare CCG geopandas dataframe
column_mapping = {df_map.columns[0]: 'Index', df_map.columns[1]: 'ONS CCG code', df_map.columns[2]: 'CCG name'}
df_map_1 = df_map.rename(columns=column_mapping)
df_map_2 = df_map_1.set_index('Index')
##Prepare CCG geopandas dataframe end 

##Prepare ODS to ONS code mapping dataframe
column_ons_code = ccg_code_map_json['fields'][0]['name'].lower()
column_ods_code = ccg_code_map_json['fields'][1]['name'].lower()
ccg_code_map_df_1 = ccg_code_map_df.iloc[:,:2]
ccg_code_map_df_1.columns = ccg_code_map_df_1.columns.str.lower()
ccg_code_map_df_1.rename(columns={'attributes.%s' %column_ons_code :'ONS CCG code', 'attributes.%s' %column_ods_code: 'ODS CCG code'}, inplace=True)
##Prepare ODS to ONS code mapping dataframe end 

##Join geometery and code mapping table, select relevant columns and output formatted GeoJSON
final_map_df = ccg_code_map_df_1.merge(df_map_2, how = 'outer', on = 'ONS CCG code')
final_map_df = final_map_df.rename(columns  = {"ODS CCG code" : "code"})
final_map_df_1 = final_map_df[["code", "CCG name", "geometry"]]
gdf = gpd.GeoDataFrame(final_map_df_1)
gdf.to_file("assets/data/ccg_geojson.geojson", driver="GeoJSON") 
f = open("assets/data/ccg_geojson.geojson")
data_ccg_geojson =  json.load(f)
##Join geometery and code mapping table, select relevant columns and output formatted GeoJSON end 

##GeoJSON processing for data on hover
tooltip_text = { x: y for x, y in zip(final_df['ODS CCG code'], final_df['Cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per 1000 GP registered patients in %s' %current_year_str])}
tooltip_text_2 = { x: y for x, y in zip(final_df['ODS CCG code'], final_df['Number of patients registered at GP practices'].apply(str))}

for idx,x in enumerate(data_ccg_geojson['features']):
    this_tooltip_text = tooltip_text[x['properties']['code']]
    data_ccg_geojson['features'][idx]['properties']['Cost (£) per 1000 GP registered population'] = this_tooltip_text

for idx,x in enumerate(data_ccg_geojson['features']):
    this_tooltip_text_2 = tooltip_text_2[x['properties']['code']]
    data_ccg_geojson['features'][idx]['properties']['GP registered population'] = this_tooltip_text_2
##GeoJSON processing for data on hover end

##Save data for plot 2 to csv
fig_2_data = df6.copy()
fig_2_data.to_csv("assets/data/cost_antibiotics_ccg_current_year.csv", index=False)
##Save data for plot 2 to end

##Visualization Plot 2
frame = folium.Figure(width=700, height=500)
fig_2 = folium.Map(
    location=[53, 1],
    tiles="cartodbpositron",
    zoom_start=7).add_to(frame)
folium.Choropleth(
    geo_data = data_ccg_geojson,
   name="choropleth",
    data= final_df,
    columns=["ODS CCG code", "Cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per 1000 GP registered patients in %s" %current_year_str],
    key_on="feature.properties.code",
    fill_color= "BuPu",
    fill_opacity=1,
    line_opacity=0.5,
   legend_name="Prescribing cost (£) per 1000 GP registered population in %s" %current_year_str,
    highlight = True
).add_to(fig_2)
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                           'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.5, 
                                 'weight': 0.1}
data_on_hover = folium.features.GeoJson(data = data_ccg_geojson, style_function=style_function, control=False, highlight_function=highlight_function, tooltip=folium.features.GeoJsonTooltip(
    fields=['CCG name', 'code', 'GP registered population', 'Cost (£) per 1000 GP registered population'],
    aliases=['CCG name: ', 'CCG code: ', 'GP registered population: ', 'Cost (£) per 1000 GP registered population: '],
    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")))
fig_2.add_child(data_on_hover)
fig_2.keep_in_front(data_on_hover)
folium.LayerControl().add_to(fig_2)
##Visualization Plot 2 end

##Write out to file (.html) Plot 2
fig_2.save("assets/folium/folium_obj.html", "w")
##Write out to file (.html) Plot 2 end
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