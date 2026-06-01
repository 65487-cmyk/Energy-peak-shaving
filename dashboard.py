
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Energy consumption", page_icon=":bar_chart:", layout="wide")
st.title("Peak shaving solar sizing")
st.markdown('<style>div.block-container{padding_top:1rem:}</style>',
             unsafe_allow_html=True)

#loading data used
df=pd.read_csv(r"C:\Users\vasey\OneDrive\Documents\solar project(syokimau)\final AEM data.csv")
df['Date']=pd.to_datetime(df['Date'])