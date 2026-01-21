import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import openpyxl

# Set page config
st.set_page_config(page_title="Visualisasi Curah Hujan Bandung", page_icon="🌧️", layout="wide")

# Title
st.title("🌧️ Visualisasi Curah Hujan Bandung")
st.markdown("Dashboard untuk menganalisis data curah hujan di Bandung")

# Load data
#@st.cache_data
def load_data():
    df = pd.read_excel('curah_hujan_bandung.xlsx')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df


df = load_data()

# Sidebar
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", df['Tanggal'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df['Tanggal'].max())

# Filter data
mask = (df['Tanggal'] >= pd.to_datetime(start_date)) & (df['Tanggal'] <= pd.to_datetime(end_date))
filtered_df = df[mask]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Grafik Curah Hujan Harian")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='Tanggal', y='Curah Hujan (mm)', ax=ax)
    plt.xticks(rotation=45)
    plt.title('Curah Hujan Harian di Bandung')
    plt.xlabel('Tanggal')
    plt.ylabel('Curah Hujan (mm)')
    st.pyplot(fig)

with col2:
    st.subheader("Statistik")
    st.metric("Total Hari", len(filtered_df))
    st.metric("Rata-rata Curah Hujan", f"{filtered_df['Curah Hujan (mm)'].mean():.2f} mm")
    st.metric("Maksimal Curah Hujan", f"{filtered_df['Curah Hujan (mm)'].max():.2f} mm")

# Distribusi Intensitas
st.subheader("Distribusi Intensitas Curah Hujan")
fig2, ax2 = plt.subplots(figsize=(10, 6))
intensitas_counts = filtered_df['Intensitas'].value_counts()
sns.barplot(x=intensitas_counts.index, y=intensitas_counts.values, ax=ax2)
plt.title('Distribusi Intensitas Curah Hujan')
plt.xlabel('Intensitas')
plt.ylabel('Jumlah Hari')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Data table
st.subheader("Data Curah Hujan")
st.dataframe(filtered_df, use_container_width=True)

# Download button
st.download_button(
    label="Download Data sebagai CSV",
    data=filtered_df.to_csv(index=False),
    file_name="curah_hujan_filtered.csv",
    mime="text/csv"
)



