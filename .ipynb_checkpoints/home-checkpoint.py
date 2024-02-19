#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#Bibliotecas
import pandas as pd
import streamlit as st
import folium
from PIL import Image
from streamlit_folium import folium_static

#Importar dataset
df = pd.read_csv('dataset/zomato.csv')

#@title Limpeza do DataFrame

# 1.Preenchimento do nome dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
  return COUNTRIES[country_id]

df['Country Name'] = [COUNTRIES[country_id] for country_id in df['Country Code']]

# 2.Criação do Tipo de Categoria de Comida

def create_price_tye(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

df['Price Type'] = [create_price_tye(price_range) for price_range in df['Price range']]

# 3. Criação do nome das Cores
COLORS = {
  "3F7E00": "darkgreen",
  "5BA829": "green",
  "9ACD32": "lightgreen",
  "CDD614": "orange",
  "FFBA00": "red",
  "CBCBC8": "darkred",
  "FF7800": "darkred",
}
def color_name(color_code):
  return COLORS[color_code]

df['Color name'] = [color_name(color_code) for color_code in df['Rating color']]

# 4. Renomear as colunas do DataFrame
"""
def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df
"""

#df = rename_columns(df)

# 5. Categorizar tipos de culinária
df['Cuisines'] = df.loc[:, 'Cuisines'].astype(str).apply(lambda x: x.split(",")[0])

####Necesspario eliminação de casos onde não ocorreram votos a fim de eliminar outliers
print(df.head())