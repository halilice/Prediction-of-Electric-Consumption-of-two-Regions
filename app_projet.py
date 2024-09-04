import streamlit as st
import pandas as pd
import numpy as np
from enedis_dashboard1 import basic_indicators, indicators_matrix
from prediction_energy import prediction_energy


st.set_page_config(page_title="Enedis Dashboard", page_icon=":bar_chart:", layout='wide')

st.sidebar.header('Choose the Page: ')

sidebar = st.sidebar.selectbox('Select the Page', ['Présentation', 'Basic Indicators', 'Indicators of ML Model Matrix', 
                                                   'Prediction Daily Energy Consumption'])

if sidebar == 'Présentation':
  list_pages = ['Accueil', 'Equipe', 'Objectif', 'Infos des Régions', 'Outils', 'Fin'] 
  pages = st.sidebar.radio('Sélectionnez la région', list_pages)
  if pages == 'Accueil':
    st.image('presentation/Accueil.png')
  elif pages == 'Equipe':
    st.image('presentation/equipe.png')
  elif pages == 'Objectif':
    st.image('presentation/objectif.png')
  elif pages == 'Infos des Régions':
    st.image('presentation/regions.png')
  elif pages == 'Outils':
    st.image('presentation/outil.png')
  else:
    st.image('presentation/page_fin.png')

elif sidebar == 'Basic Indicators':
    basic_indicators()
    
elif sidebar == 'Indicators of ML Model Matrix':
    indicators_matrix()
    
else:
    prediction_energy()
