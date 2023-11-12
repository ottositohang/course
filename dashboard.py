import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import babel
sns.set(style='dark')

def create_daily_data_df(df):
    daily_con_df = df.resample(rule='D', on='datetime').agg({'No': 'nunique', 'AQI_calculated': 'mean'})
    daily_con_df = daily_con_df.reset_index()
    return daily_con_df

def create_daily_prop_df(df):
    daily_prop_df = df.resample(rule='D', on='datetime').agg({"PM2.5": 'mean', "PM10": 'mean', "SO2": 'mean', "NO2": 'mean', "CO": 'mean', "O3": 'mean'})
    daily_prop_df = daily_prop_df.reset_index()
    return daily_prop_df

def create_daily_frame_df(df):
    daily_frame_df = df.resample(rule='D', on='datetime').agg({"PM2.5": 'mean', "PM10": 'mean', "SO2": 'mean', 
                                                               "NO2": 'mean', "CO": 'mean', "O3": 'mean', 'AQI_calculated': 'mean'})
    return daily_frame_df

# Load cleaned data
aqi_df = pd.read_csv("aqi_df.csv")

datetime_columns = ["datetime"]
aqi_df.sort_values(by="datetime", inplace=True)
aqi_df.reset_index(inplace=True)
 
for column in datetime_columns:
    aqi_df[column] = pd.to_datetime(aqi_df[column])

min_date = aqi_df["datetime"].min()
max_date = aqi_df["datetime"].max()
 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = aqi_df[(aqi_df["datetime"] >= str(start_date)) & 
                (aqi_df["datetime"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_prop_df = create_daily_prop_df(main_df)
daily_con_df = create_daily_data_df(main_df)
daily_frame_df = create_daily_frame_df(main_df)

st.header('Dicoding ISPU Dashboard :sparkles:')

# plot jumlah ISPU harian
st.subheader('Daily ISPU')

col1, col2 = st.columns(2)
 
with col1:
    total_ISPU = daily_con_df.AQI_calculated.mean()
    st.metric('Rata-rata ISPU', value=total_ISPU)

st.subheader('Proporsi Pencemar')

# pie chart
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))

    pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    pollutant_colors = ["#F08583", "#60ABA8", "#B4E2C4", "#F6F3CC","#ECD8C1", "#806154"]

    total_concentrations = daily_prop_df[pollutants].mean()

    concentration_data = pd.DataFrame({
        "Pollutant": pollutants,
        "Concentration": total_concentrations
    })
    daily_prop_df = concentration_data

    ax.pie(total_concentrations, labels=pollutants,
            autopct='%1.1f%%', colors=pollutant_colors, pctdistance=0.85, 
            wedgeprops = {'width': 0.4})

    st.pyplot(fig)

with col2:
    df = daily_frame_df
    st.dataframe(df)

st.subheader('Hasil Seluruh Stasiun Pengukur')

# line chart
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_con_df['datetime'],
    daily_con_df['AQI_calculated'],
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


    

