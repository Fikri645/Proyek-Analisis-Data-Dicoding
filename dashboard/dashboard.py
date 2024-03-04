import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='white')


hour_df = pd.read_csv('https://raw.githubusercontent.com/Fikri645/Proyek-Analisis-Data-Dicoding/main/data/cleaned/hour_df.csv')
day_df = pd.read_csv('https://raw.githubusercontent.com/Fikri645/Proyek-Analisis-Data-Dicoding/main/data/cleaned/day_df.csv')

hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)
hour_df["date"] = pd.to_datetime(hour_df["date"])
min_date = hour_df["date"].min()
max_date = hour_df["date"].max()

st.header('Proyek Analisis Data by Muhammad Fikri Wahidin')
st.subheader('Penggunaan Rental Sepeda Sepanjang Tahun 2011-2012')
st.write("Penggunaan Rental Sepeda Berdasarkan Musim")
st.bar_chart(hour_df.groupby('season')[['casual', 'registered']].sum())

st.write("Penggunaan Rental Sepeda Berdasarkan Bulan")
st.bar_chart(hour_df.groupby('month')[['casual', 'registered']].sum())


st.subheader("Pilih Rentang Waktu")
start_date, end_date = st.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)
main_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
            (hour_df["date"] <= str(end_date))]
main_day_df = day_df[(day_df["date"] >= str(start_date)) & 
            (day_df["date"] <= str(end_date))]

 
chart_temperature_season = {
    "mark": "point",
    "encoding": {
        "x": {
            "field": "temperature",
            "type": "quantitative",
        },
        "y": {
            "field": "total",
            "type": "quantitative",
        },
        "color": {"field": "season", "type": "nominal"},
        "shape": {"field": "season", "type": "nominal"},
    },
}   

main_hour_df['weather'] = main_hour_df['weather'].map({1: 'Clear', 2: 'Mist / Cloudy', 3: 'Light Snow / Light Rain', 4: 'Heavy Rain / Ice Pallets'})

temperature = f"{round(main_hour_df['temperature'].mean(), 2)}°C"
windspeed = f"{round(main_hour_df['windspeed'].mean(), 2)} km/h"
humidity = f"{round(main_hour_df['humidity'].mean(), 2)}%"


col1, col2, col3 = st.columns(3)
col1.metric("Temperature", temperature)
col2.metric("Wind", windspeed)
col3.metric("Humidity", humidity)


st.subheader("Penggunaan Rental Sepeda Berdasarkan Temperature")
col1, col2 = st.columns(2)

with col1:
    st.write("Penggunaan Rental Sepeda per Jam")
    st.vega_lite_chart(main_hour_df, chart_temperature_season, theme="streamlit", use_container_width=True)
with col2:
    st.write("Penggunaan Rental Sepeda per Hari")
    st.vega_lite_chart(main_day_df, chart_temperature_season, theme="streamlit", use_container_width=True)
st.subheader("Penggunaan Rental Sepeda Berdasarkan Cuaca")

st.write("Penggunaan Rental Sepeda Berdasarkan Cuaca")
st.bar_chart(main_hour_df, x='weather', y='total', use_container_width=True)

st.caption('Copyright (c) Muhammad Fikri Wahidin 2024')