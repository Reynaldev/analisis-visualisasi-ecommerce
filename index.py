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

def make_map():
    geoloc_df = pd.read_csv('/home/archie/Machine-Learning/Datasets/E-Commerce_Public_Dataset/geolocation_dataset.csv')
    customer_df = pd.read_csv('/home/archie/Machine-Learning/Datasets/E-Commerce_Public_Dataset/customers_dataset.csv')
    # Buat visualisasi persebaran pembeli menggunakan Folium

    geometry = geopandas.points_from_xy(customer_full_df.geolocation_lng, customer_full_df.geolocation_lat)
    geo_df = geopandas.GeoDataFrame(customer_full_df, geometry=geometry)

    world = geopandas.read_file(geodatasets.get_path("naturalearth.land"))

    map = folium.Map(location=[15, 30], tiles="Cartodb dark_matter", zoom_start=2)

    plugins.FastMarkerCluster([[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]).add_to(map)

    map

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