from weatherbit.api import Api
import pandas as pd
import streamlit as st



st.title('A Seven-Day Weather Forecast App')
key = st.text_input('Enter key')
city = st.text_input('Enter City')
state = st.text_input('Enter City State', '')
country = st.text_input('Enter Country', 'US')
if st.button('Fetch'):
    api = Api(key)
    forecast = api.get_forecast(city='Port Harcourt', state='', country='NG')

    df = pd.DataFrame()
    for day in forecast.get_series(['temp', 'precip', 'weather','wind_spd' ,'datetime']):
        df['Date'] = day['datetime'].date()
        df['Temp (°C)'] =  day['temp']
        df['Wind Speed'] = day['wind_spd']
        df['Precip'] = day['precip']
        df['Weather'] = day['weather']['description']
    st.dataframe(df)




