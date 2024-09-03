import streamlit as st
import pandas as pd
import numpy as np
from enedis_dashboard1 import basic_indicators, indicators_matrix
from prediction_energy import prediction_energy


st.set_page_config(page_title="Enedis Dashboard", page_icon=":bar_chart:", layout='wide')

st.sidebar.header('Choose the Page: ')

sidebar = st.sidebar.selectbox('Select the Page', ['Basic Indicators', 'Indicators of ML Model Matrix', 
                                                   'Prediction Daily Energy Consumption'])

if sidebar == 'Basic Indicators':
    basic_indicators()
    
elif sidebar == 'Indicators of ML Model Matrix':
    indicators_matrix()
    
else:
    prediction_energy()