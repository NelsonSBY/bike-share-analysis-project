import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import plotly.express as px

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mapping Musim dan Cuaca
day_df["season"] = day_df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
day_df["weathersit"] = day_df["weathersit"].map({1: "Clear", 2: "Mist", 3: "Rain"})

# Set page configuration
st.set_page_config(page_title="Dashboard Analisis Penyewaan Sepeda", layout="wide")
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("### Analisis Data Penyewaan Sepeda")

# Sidebar
st.sidebar.header("INFORMASI")
st.sidebar.write("**Nama:** Nelson Lau")
st.sidebar.write("**Email:** integralvektor@gmail.com")
st.sidebar.image("SEPEDA.jpg", use_container_width=True)

# Filter berdasarkan tanggal
st.sidebar.header("Filter Berdasarkan Rentang Tanggal")
start_date = pd.to_datetime(st.sidebar.date_input("Mulai Tanggal", pd.to_datetime("2011-01-01")))
end_date = pd.to_datetime(st.sidebar.date_input("Selesai Tanggal", pd.to_datetime("2012-12-31")))

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

day_df_filtered = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]
hour_df_filtered = hour_df[(hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)]

# Menampilkan total penyewaan berdasarkan rentang waktu yang dipilih
total_penyewaan_filtered = day_df_filtered["cnt"].sum()
st.markdown(f"## Total Penyewaan : **{total_penyewaan_filtered:,}**")

# Visualisasi: Jumlah Pengguna Sepeda Berdasarkan Musim
st.subheader("Jumlah Pengguna Sepeda Berdasarkan Musim")
musim_agg = day_df_filtered.groupby("season")["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="cnt", data=musim_agg, color="#4169E1", ax=ax)
ax.set_xlabel("Kondisi Musim")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Musim")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
st.pyplot(fig)

# Visualisasi: Jumlah Pengguna Sepeda Berdasarkan Cuaca
st.subheader("Jumlah Pengguna Sepeda Berdasarkan Cuaca")
warna_cuaca = ["#4169E1", "#4169E1", "#4169E1"]
cuaca_agg = day_df_filtered.groupby("weathersit")["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(28, 10))
sns.barplot(x="weathersit", y="cnt", data=cuaca_agg, palette=warna_cuaca, ax=ax)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Cuaca", fontsize=25)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=15)
ax.set_xlabel("Kondisi Cuaca", fontsize=15)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Visualisasi: Jumlah Penyewaan Sepeda Berdasarkan Suhu
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Suhu")
fig = px.scatter(hour_df_filtered, x="temp", y="cnt", title="Jumlah Penyewaan Sepeda Berdasarkan Suhu", labels={"temp": "Suhu", "cnt": "Jumlah Penyewaan Sepeda"})
st.plotly_chart(fig)

# Visualisasi: Penyewaan Sepeda Terbanyak & Tersedikit Berdasarkan Jam
st.subheader("Penyewaan Sepeda Terbanyak & Tersedikit Berdasarkan Jam")
jam_agg = hour_df_filtered.groupby("hr")["cnt"].sum().reset_index()
teratas3_hour = jam_agg.nlargest(3, 'cnt')
terbawah3_hour = jam_agg.nsmallest(3, 'cnt')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
warna_jam = ["#4169E1", "#4169E1", "#4169E1"]

sns.barplot(x="hr", y="cnt", data=teratas3_hour, palette=warna_jam, ax=ax[0])
ax[0].set_ylabel("Total Penyewaan Sepeda", fontsize=12)
ax[0].set_xlabel("Jam")
ax[0].set_title("Penyewaan Sepeda Terbanyak Berdasarkan Jam")
ax[0].tick_params(axis='y', labelsize=12)
ax[0].tick_params(axis='x', labelsize=12)

sns.barplot(x="hr", y="cnt", data=terbawah3_hour, palette=warna_jam, ax=ax[1])
ax[1].set_ylabel("Total Penyewaan Sepeda", fontsize=12)
ax[1].set_xlabel("Jam")
ax[1].set_title("Penyewaan Sepeda Tersedikit Berdasarkan Jam")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=12)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("🚴 **Dashboard dibuat oleh Nelson Lau**")