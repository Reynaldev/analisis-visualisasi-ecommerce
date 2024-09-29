import folium
import geopandas
import numpy as np
import pandas as pd
import seaborn as sns
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from folium import plugins

st.title('Analisis dan Visualisasi Data Menggunakan Matplotlib, Folium, Seaborn, dan GeoPandas')

st.subheader('Peringkat Produk Berdasarkan Rating atau Penjualannya')

tab1, tab2 = st.tabs(['Ratings', 'Sales'])

with tab1:
    st.image('./assets/prod-avg-ratings.png')

with tab2:
    st.image('./assets/prod-total-sales.png')

st.subheader('Grafik RFM')

st.image('./assets/rfm.png')

st.subheader('Grafik Histogram')

st.image('./assets/histplot.png')

st.caption('Copyright &copy; Reynaldev {}'.format(dt.datetime.now().strftime('%Y')))