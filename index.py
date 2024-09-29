import datetime as dt
import streamlit as st
import streamlit.components.v1 as components

st.title('Analisis dan Visualisasi Data Menggunakan Matplotlib, Folium, Seaborn, dan GeoPandas')

st.markdown('> Versi Google Colab: [](https://colab.research.google.com/drive/1bsj6vyZ8Ur4rwDHK0-XIqB7VTv7cjAw-?usp=sharing)')

st.header('Peringkat Produk Berdasarkan Rating atau Penjualannya')

tab1, tab2 = st.tabs(['Ratings', 'Sales'])

with tab1:
    st.image('./assets/prod-avg-ratings.png')

with tab2:
    st.image('./assets/prod-total-sales.png')

st.header('Grafik RFM')

st.image('./assets/rfm.png')

st.header('Grafik Histogram')

st.image('./assets/histplot.png')

st.header('Grafik Persebaran Pembeli')

map_html = ""
with open('./map.html', 'r') as file:
    for line in file:
        map_html += line

components.html(map_html, height=500, scrolling=True)

st.caption('Copyright &copy; Reynaldev {}'.format(dt.datetime.now().strftime('%Y')))