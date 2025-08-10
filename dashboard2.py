import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Dashboard Penyewaan Sepeda")

# Membaca kedua dataset secara terpisah
url_1 = "https://raw.githubusercontent.com/khadavi971/Proyek-analisis-data/main/day_edited.csv"
url_2 = "https://raw.githubusercontent.com/khadavi971/Proyek-analisis-data/main/hour_edited.csv"

# Pilih dataset yang ingin digunakan
dataset_option = st.sidebar.selectbox(
    "Pilih Dataset:",
    options=["Data per Jam", "Data per Hari"]
)

# Pilih dataset berdasarkan pilihan pengguna
if dataset_option == "Data per Jam":
    data = pd.read_csv(url_2)
else:
    data = pd.read_csv(url_1)

# Pastikan dataset memiliki kolom yang diperlukan
required_columns = {'season', 'weathersit', 'cnt'}
if dataset_option == "Data per Jam":
    required_columns.add('hr')

if required_columns.issubset(data.columns):
    # Sidebar untuk filter
    st.sidebar.header("Filter Data")
    
    # Filter musim
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    selected_season = st.sidebar.multiselect(
        "Pilih Musim:",
        options=list(season_mapping.keys()),
        default=list(season_mapping.keys()),
        format_func=lambda x: season_mapping[x]
    )

    # Filter cuaca
    weather_mapping = {
        1: "Clear/Few Clouds",
        2: "Mist/Cloudy",
        3: "Light Snow/Light Rain",
        4: "Heavy Rain/Snow"
    }
    selected_weather = st.sidebar.multiselect(
        "Pilih Kondisi Cuaca:",
        options=list(weather_mapping.keys()),
        default=list(weather_mapping.keys()),
        format_func=lambda x: weather_mapping[x]
    )

    # Filter data berdasarkan pilihan pengguna
    filtered_data = data[
        (data['season'].isin(selected_season)) &
        (data['weathersit'].isin(selected_weather))
    ]

    # Visualisasi 1: Rata-rata penyewaan berdasarkan jam (jika data per jam)
    if 'hr' in filtered_data.columns:
        avg_rentals_hour = filtered_data.groupby('hr')['cnt'].mean()

        st.subheader("Rata-rata Penyewaan Berdasarkan Jam")
        plt.figure(figsize=(10, 5))
        avg_rentals_hour.plot(kind='line', marker='o', color='blue')
        plt.title('Rata-rata Penyewaan Berdasarkan Jam')
        plt.xlabel('Jam')
        plt.ylabel('Rata-rata Penyewaan')
        plt.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(plt)

    # Visualisasi 2: Rata-rata penyewaan per musim
    avg_rentals_season = filtered_data.groupby('season')['cnt'].mean()

    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    plt.figure(figsize=(8, 5))
    avg_rentals_season.plot (kind= 'bar', color= ['green', 'orange', 'red', 'blue'])
    plt.title('Rata-rata Penyewaan Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Penyewaan')
    plt.xticks(rotation = 0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

    # Visualisasi 3: Rata-rata penyewaan per kondisi cuaca
    avg_rentals_weather = filtered_data.groupby('weathersit')['cnt'].mean()
    st.subheader("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
    plt.figure(figsize=(8, 5))
    avg_rentals_weather.plot(kind='bar', 
                            color=['skyblue', 'gray', 'orange', 'darkblue'])
    plt.title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Penyewaan')
    plt.xticks(ticks=range(len(avg_rentals_weather.index)), 
           labels=avg_rentals_weather.index,
           rotation=0
           )
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

    # Visualisasi 4: Rata-rata penyewaan di hari libur
    avg_rentals_holiday =  filtered_data.groupby('holiday')['cnt'].mean()
    plt.figure(figsize=(4, 5))
    avg_rentals_holiday.plot (kind= 'bar', color=['black', 'red'])
    plt.title('Rata-rata Penyewaan Berdasarkan Hari Libur', fontsize=12)
    plt.xlabel('Kategori Hari', fontsize=10)
    plt.ylabel('Rata-rata Penyewaan', fontsize=10)
    plt.xticks (rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)
else:
    st.error("Dataset tidak memiliki kolom yang diperlukan. Harap periksa dataset Anda.")
