import datetime as dt
import streamlit as st
import streamlit.components.v1 as components

st.title('Analisis dan Visualisasi Data Menggunakan Matplotlib, Folium, Seaborn, dan GeoPandas')

st.markdown(
    '''
    > Versi Google Colab: [Google Colab](https://colab.research.google.com/drive/1bsj6vyZ8Ur4rwDHK0-XIqB7VTv7cjAw-?usp=sharing)
    > Githu: [Reynaldev](https://github.com/Reynaldev/analisis-visualisasi-ecommerce)
    '''
)

st.header('Peringkat Produk Berdasarkan Rating atau Penjualannya')

tab1, tab2 = st.tabs(['Ratings', 'Sales'])

with tab1:
    st.image('dashboard/assets/prod-avg-ratings.png')

with tab2:
    st.image('dashboard/assets/prod-total-sales.png')

st.header('Grafik RFM')

st.image('dashboard/assets/rfm.png')

st.header('Grafik Histogram')

st.image('dashboard/assets/histplot.png')

st.header('Peta Persebaran Pembeli')

map_html = ""
with open('map.html', 'r') as file:
    for line in file:
        map_html += line

components.html(map_html, height=500, scrolling=True)

st.caption('Copyright &copy; Reynaldev {}'.format(dt.datetime.now().strftime('%Y')))