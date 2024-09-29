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
from streamlit_folium import st_folium

def main():
    # Prepare data

    order_df = pd.read_csv('data/orders_dataset.csv')
    geoloc_df = pd.read_csv('data/geolocation_dataset.csv')
    product_df = pd.read_csv('data/products_dataset.csv')
    customer_df = pd.read_csv('data/customers_dataset.csv')
    order_items_df = pd.read_csv('data/order_items_dataset.csv')
    order_reviews_df = pd.read_csv('data/order_reviews_dataset.csv')

    # Menghilangkan kolom yang tidak diperlukan
    order_df.drop(
        columns=[
            'order_approved_at', 
            'order_delivered_carrier_date', 
            'order_delivered_customer_date', 
            'order_estimated_delivery_date'
        ],
        inplace=True
    )

    order_df['order_purchase_timestamp'] = pd.to_datetime(order_df['order_purchase_timestamp'])

    # Menghilangkan beberapa kolom yang tidak dibutuhkan
    order_reviews_df.drop(
        columns=[
            'review_comment_title',       
            'review_comment_message',     
            'review_creation_date',           
            'review_answer_timestamp',
        ],
        inplace=True
    )

    # Mengubah missing value pada "product_df"
    product_df.product_category_name.fillna('unknown_category', inplace=True)

    # Menghapus beberapa kolom yang tidak dibutuhkan
    product_df.drop(
        columns=[
            'product_description_lenght',
            'product_name_lenght',
            'product_photos_qty',
            'product_weight_g',
            'product_length_cm',
            'product_height_cm',
            'product_width_cm'
        ],
        inplace=True
    )

    # Bersihkan "order_items_df"
    order_items_df.drop(columns=['seller_id', 'shipping_limit_date'], inplace=True)

    # Bersihkan "geoloc_df"
    geoloc_df.drop_duplicates(['geolocation_lat', 'geolocation_lng'], inplace=True)

    # EDA order_items_df
    order_items_df['total_price'] = order_items_df['price'] + order_items_df['freight_value']
    order_items_df.drop(columns=['price', 'freight_value'], inplace=True)

    # Gabungkan "order_items_df" dan "order_reviews_df"
    order_details_df = pd.merge(
        left=order_items_df,
        right=order_reviews_df,
        how='left',
        left_on='order_id',
        right_on='order_id',
    )

    # Gabungkan "order_details_df" dan "order_df"
    order_status_df = pd.merge(
        left=order_details_df,
        right=order_df,
        how='left',
        left_on='order_id',
        right_on='order_id'
    )

    # Gabungkan "order_details_df" dan "product_df"
    order_full_df = pd.merge(
        left=order_status_df,
        right=product_df,
        how='left',
        left_on='product_id',
        right_on='product_id',
    )

    # Gabungkan "customer_df" dan "geoloc_df"
    customer_full_df = pd.merge(
        left=customer_df,
        right=geoloc_df,
        how='inner',
        left_on='customer_zip_code_prefix',
        right_on='geolocation_zip_code_prefix',
    ).drop_duplicates(
        ['customer_id', 'customer_unique_id']
    ).drop(columns=[
        'customer_zip_code_prefix', 
        'customer_city', 
        'customer_state'
    ])

    # Bersihkan memory
    del order_df, order_details_df, order_reviews_df, order_status_df, order_items_df, product_df, customer_df, geoloc_df

    product_avg_df = order_full_df.groupby('product_category_name').agg({
        'review_score': 'mean',
    })
    
    product_sum_df = order_full_df[order_full_df.order_status == 'delivered'].groupby('product_category_name').agg({
        'product_category_name': 'count'
    })

    product_sum_df.rename(
        columns={
            'product_category_name': 'number_of_sales'
        },
        inplace=True
    )

    geometry = geopandas.points_from_xy(customer_full_df.geolocation_lng, customer_full_df.geolocation_lat)
    geo_df = geopandas.GeoDataFrame(customer_full_df, geometry=geometry)

    map = folium.Map(location=[15, 30], tiles="Cartodb dark_matter", zoom_start=2)

    plugins.FastMarkerCluster([[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry]).add_to(map)

    # Main UI

    st.title('Analisis dan Visualisasi Data Menggunakan Matplotlib, Folium, Seaborn, dan GeoPandas')

    st.markdown(
        '''
        > Versi Google Colab: [Google Colab](https://colab.research.google.com/drive/1bsj6vyZ8Ur4rwDHK0-XIqB7VTv7cjAw-?usp=sharing)
        >
        > Github: [Reynaldev](https://github.com/Reynaldev/analisis-visualisasi-ecommerce)
        '''
    )

    st_folium(map, width=750)

    st.header('Grafik RFM')

    rfm_df = order_full_df.groupby('customer_id', as_index=False).agg({
        'order_id': 'nunique',
        'order_purchase_timestamp': 'max',
        'total_price': 'sum',
    })

    rfm_df.columns = ['customer_id', 'frequency', 'max_order_timestamp', 'monetary']

    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date
    recent_date = order_full_df['order_purchase_timestamp'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)

    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(12, 12))
 
    colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
    
    sns.barplot(
        x="recency", 
        y="customer_id", 
        data=rfm_df.sort_values(by="recency", ascending=False).head(5), 
        palette=colors, 
        ax=ax[0],
        hue='customer_id',
    )

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=15)
    ax[0].tick_params(axis ='x', labelsize=15)
    ax[0].grid(True, axis='x')
    
    sns.barplot(
        x="frequency", 
        y="customer_id", 
        data=rfm_df.sort_values(by="frequency", ascending=False).head(5), 
        palette=colors, 
        ax=ax[1],
        hue='customer_id',
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=15)
    ax[1].tick_params(axis='x', labelsize=15)
    ax[1].grid(True, axis='x')
    
    sns.barplot(
        x="monetary", 
        y="customer_id", 
        data=rfm_df.sort_values(by="monetary", ascending=False).head(5), 
        palette=colors, 
        ax=ax[2],
        hue='customer_id',
    )
    ax[2].set_ylabel(None)
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=15)
    ax[2].tick_params(axis='x', labelsize=15)
    ax[2].grid(True, axis='x')

    st.pyplot(fig)

    st.header('Grafik Histogram')

    fig, ax = plt.subplots(figsize=(24, 8))

    sns.histplot(rfm_df, x='recency', ax=ax)

    ax.set_ylabel('Monetary')
    ax.set_xlabel('Recency')
    ax.set_title("Money Spent Each Visits", loc="center", fontsize=15)
    ax.tick_params(axis ='x', labelsize=15)
    ax.tick_params(axis ='y', labelsize=15)
    ax.grid(True, axis='y')

    st.pyplot(fig)

    st.header('Peringkat Produk Berdasarkan Rating atau Penjualannya')

    tab1, tab2 = st.tabs(['Ratings', 'Sales'])

    with tab1:
        fig, ax = plt.subplots(figsize=(16, 24))

        sns.barplot(
            x='review_score', 
            y='product_category_name', 
            data=product_avg_df.sort_values('review_score', ascending=False),
            ax=ax,
            orient='y'
        )

        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_xticks(np.arange(1, 6))
        ax.set_title('Average Ratings', loc='center', fontsize=15)
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        ax.grid(True, axis='x')

        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(24, 24), layout='constrained')

        sns.barplot(
            x='number_of_sales', 
            y='product_category_name', 
            data=product_sum_df.sort_values('number_of_sales', ascending=False), 
            ax=ax,
            orient='y',
        )

        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title('Product Category by Number of Sales', loc='center', fontsize=15)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        ax.grid(True, axis='x')

        st.pyplot(fig)

    st.caption('Copyright &copy; Reynaldev {}'.format(dt.datetime.now().strftime('%Y')))

if __name__ == "__main__":
    main()