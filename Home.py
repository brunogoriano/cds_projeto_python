#Libraries
#from haversine import haversine
#import plotly.express as px
import plotly.graph_objects as go

#Bibliotecas
import pandas as pd
import streamlit as st
#import folium
from PIL import Image
#from streamlit_folium import folium_static

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

# 5. Categorizar tipos de culinária
df['Cuisines'] = df.loc[:, 'Cuisines'].astype(str).apply(lambda x: x.split(",")[0])


#===============================================================
# Streamlit | Configs
#===============================================================
   
st.set_page_config(
    page_title="Projeto Fome Zero | Análises Gerenciais",
    page_icon="📈",
    layout="wide"
)

#===============================================================
# Barra Lateral
#===============================================================

#image_path = 'analytics.png'
#image = Image.open(image_path)
#st.sidebar.image(image, width=120)

st.sidebar.markdown('# Projeto Fome Zero')
st.sidebar.markdown('## Filtros')
st.sidebar.caption(' Escolha os Paises que Deseja visualizar os Restaurantes')

#Filtro País
paises = df['Country Name'].drop_duplicates().sort_values()
principaisPaises = df.groupby(['Country Name'])['Country Name'].count().reset_index(name='count').sort_values(['count'], ascending=False).head(7)
principaisPaises = principaisPaises['Country Name'].sort_values()

country_options = st.sidebar.multiselect(
    'Seleciona os países para visualizar',
    paises, principaisPaises)

df = df.loc[df['Country Name'].isin(country_options), :] 

#===============================================================
# Layout no Streamlit
#===============================================================

st.header('Projeto Fome Zero!')
st.markdown("""---""")

st.markdown('#### Temos as seguintes marcas em nossa plataforma:')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
  #Qtde de países únicos registrados
  st.metric(
    label="#PAÍSES",
    value=df['Country Name'].nunique()
  )

with col2:
  #Qtde de cidades únicas registrados
  st.metric(
    label="#CIDADES",
    value=df['City'].nunique()
  )

with col3:
  #Qtde de restaurantes únicos registrafos
  qtde_rest = df['Restaurant Name'].nunique()
  resultado = '{0:,}'.format(qtde_rest).replace(',','.') 

  st.metric(
    label="#RESTAURANTES",
    value=resultado
  )

with col4:
  #Qtde de restaurantes únicos registrafos
  st.metric(
    label="#COZINHAS",
    value=df['Cuisines'].nunique()
  )

with col5:
  #Qtde de restaurantes únicos registrafos
  qtde_votos = df['Votes'].sum()

  if qtde_votos >= 1000000:
    qtde_votos = qtde_votos / 1000000
    unidade = ' M'
  elif qtde_votos >= 1000:
    qtde_votos = qtde_votos / 1000
    unidade = ' K'
  else:
    qtde_votos

  resultado = '{0:.1f}'.format(qtde_votos).replace(',','.') + unidade
    
  st.metric(
    label="#AVALIAÇÕES",
    value=resultado
  )



#df_group = df.loc[:, ['Country Name', 'Restaurant Name', 'Votes']].groupby('Country Name').agg(Qtde=('Restaurant Name', 'count'), Votes=('Votes', 'sum')).reset_index()
#df_group.loc[(df_group['Rating'] == df_group['Rating'].min()), ['Cuisines', 'Restaurant Name', 'Votes', 'Rating']]
#df.groupby(['Country Name'])['Country Name'].count().reset_index(name='count').sort_values(['count'], ascending=False).head(7)