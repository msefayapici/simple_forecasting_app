"""
Main logic applied here
"""
import pandas as pd
import numpy as np
import streamlit as st
import time

from datetime import timedelta

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file)
    st.write(dataframe)


if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
else:
    print("upload a file to begin")

# method 1 : Simple Moving Average
period = st.radio(
        'Choose Period',
        ("Day", "Week", "Month", "Year"))

enable_seasonality = st.radio(
        'Enable Seasonality?',
        (True, False))

st.text_input("MA range", key="ma_range", placeholder="7")

ma_range = int(st.session_state.ma_range)

last_date = data['Date'].max()
forecast_df = pd.DataFrame()

if period == "Day":
    forecast_df['Date'] = [last_date + timedelta(days=x)
                           for x in range(1, ma_range + 1)]
    forecast_df['Value'] = np.nan

    result_data = pd.concat([data, forecast_df]).reset_index(drop=True)
    result_data['Forecast'] = result_data['Value'].shift(
        ma_range).rolling(ma_range).mean()

    # Seasonality
    if enable_seasonality:
        result_data['DayOfTheWeek'] = result_data['Date'].dt.day_name()

        seasonality_table = result_data.groupby('DayOfTheWeek')['Value'].sum().reset_index()
        print(seasonality_table.head())
        seasonality_table['TotalValue'] = seasonality_table.Value.sum()
        seasonality_table['SeasonalityIndex'] = (
            seasonality_table['Value'] / seasonality_table['TotalValue']) * 7

        seasonality_table = seasonality_table[['DayOfTheWeek', 'SeasonalityIndex']]
        result_data = pd.merge(result_data, seasonality_table, on='DayOfTheWeek', how='left')
        result_data['ForecastWithSeasonality'] = result_data['Forecast'] * result_data['SeasonalityIndex']
    #result_data.iloc[-42:].plot(x='Date',y=['Value', 'Forecast', 'ForecastWithSeasonality'])

        st.line_chart(result_data.iloc[-42:] ,y=['Value','Forecast','ForecastWithSeasonality'], x='Date')
    else:
        st.line_chart(result_data.iloc[-42:] ,y=['Value','Forecast'], x='Date')
