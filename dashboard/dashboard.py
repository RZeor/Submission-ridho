import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

df_day = pd.read_csv("df_day.csv")
df_hour = pd.read_csv("df_hour.csv")

def create_season_rental_df(df):
    # Grouping data
    season_rental = df_day.groupby("season")["count_cr"].agg(["sum"]).reset_index()
    return season_rental

def create_hour_rental_df(df):
    # Grouping data
    hour_rental = df_hour.groupby('kategori_waktu')["count_cr"].agg(["sum"]).reset_index()
    return hour_rental

def create_registered_df(df):
    # Mengelompokkan berdasarkan tanggal dan menjumlahkan nilai 'registered'
    registered_df = df.groupby(by='dateday').agg({'registered': 'sum'}).reset_index()
    return registered_df

def create_casual_df(df):
    # Mengelompokkan berdasarkan tanggal dan menjumlahkan nilai 'casual'
    casual_df = df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
    return casual_df

def create_total_df(df):
    # Mengelompokkan berdasarkan tanggal dan menjumlahkan nilai 'count_cr'  
    total_df = df.groupby(by='dateday').agg({'count_cr': 'sum'}).reset_index()
    return total_df

max_date = df_day['dateday'].max()
min_date = df_day['dateday'].min()

with st.sidebar:
    
    st.image("https://raw.githubusercontent.com/RZeor/projek_akhir/main/black.png")
    
    st.text('Ini merupakan sidebar')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day["dateday"] >= str(start_date)) & 
                (df_day["dateday"] <= str(end_date))]
    
season_rental = create_season_rental_df(main_df)
hour_rental = create_hour_rental_df(main_df)
registered_df = create_registered_df(main_df)
casual_df = create_casual_df(main_df)
total_df = create_total_df(main_df)

st.header("BIKER DASHBOARD 🚲")

#CUSTOMER
col1, col2, col3 = st.columns(3)

with col1:
    registered = registered_df.registered.sum()
    st.metric(label="Total Registered", value=registered)
    
with col2:
    casual = casual_df.casual.sum()
    st.metric(label="Total Casual", value=casual)
    
with col3:
    total = total_df.count_cr.sum()
    st.metric(label="Total Users", value=total)

#SEASON RENTAL
with st.container():
    
    st.subheader("Season Rental bike")
    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    #penentuan color
    colors = ['#FFD700', "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    #berdasarkan musim
    sns.barplot(data=season_rental.melt(id_vars="season"), x="season", y="value", palette=colors)
    ax.set_title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """
        Musim dengan jumlah penyewaan sepeda terbanyak adalah musim gugur (Fall) dengan total 1.061.129 penyewaan.
        
        Urutan jumlah penyewaan berdasarkan musim:
        - Fall (Gugur): 1.061.129 penyewaan
        - Summer (Musim Panas): 918.589 penyewaan
        - Winter (Musim Dingin): 841.613 penyewaan
        - Spring (Musim Semi): 471.348 penyewaan

        """
    )    
    
st.write('')

# comparison of registered and casual users    
with st.container():
    
    st.subheader('Comparison of registered and casual users')
    
    fig, ax = plt.subplots(figsize=(5, 100))
    
    # Menghitung total pengguna registered dan casual
    total_registered = df_hour['registered'].sum()
    total_casual = df_hour['casual'].sum()

    # Data untuk pie chart
    labels = ['Registered', 'Casual']
    sizes = [total_registered, total_casual]
    colors = ['#FFD700',"#D3D3D3" ]

    # Membuat pie chart
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title("Perbandingan Pengguna Registered dan Casual")
    st.pyplot(fig)
    
with st.expander("See explanation"):
    st.write(
        """
        Pengguna registered (terdaftar) jauh lebih banyak dibandingkan 
        pengguna casual (tidak terdaftar) dalam penyewaan sepeda, 
        sekitar 81.2% pengguna adalah registered , 
        sementara hanya 18.8% adalah casual users

        """
    )

st.write('')

# HOUR RENTAL
with st.container():
    
    st.subheader("Hour Rental bike")
    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    #penentuan color
    colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", '#FFD700']

    #berdasarkan musim
    sns.barplot(data=hour_rental.melt(id_vars="kategori_waktu"), x="kategori_waktu", y="value", palette=colors)
    ax.set_title('Pengaruh waktu terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """
        Jumlah penyewaan sepeda paling banyak terjadi pada sore hari dengan total 1.057.529 penyewaan.

        Urutan jumlah penyewaan berdasarkan kategori waktu:
        - Sore (Evening): 1.057.529 penyewaan
        - Pagi (Morning): 774.688 penyewaan
        - Malam (Night): 764.157 penyewaan
        - Siang (Afternoon): 696.305 penyewaan
        """
    )    
    
st.write('')

# Bike Rental Trends over Time
with st.container():
    
    st.subheader('Bike Rental Trends over Time')
    
    fig, ax = plt.subplots(figsize=(30, 10))
    
    # Membuat plot tren penyewaan sepeda dari waktu ke waktu
    plt.plot(
        df_day['dateday'], 
        df_day['count_cr'],
        label='Jumlah Penyewaan Sepeda', 
        color='#b8b814', 
        linewidth=2
    )
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_title('Tren Penyewaan Sepeda dari Waktu ke Waktu')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """
        Tren penyewaan sepeda menunjukkan pola yang bervariasi sepanjang tahun. Penyewaan cenderung 
        meningkat pada bulan 2012-04 sampai 2012-10 setelah itu mengalami penurunan
        """
    )    