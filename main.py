from datetime import datetime
import pandas as pd
import streamlit as st
import pyowm
from pyowm.utils import timestamps






st.sidebar.title('Get Weather Information')
st.sidebar.info('Get your API key from OpenWeatherMap')
#key = st.sidebar.text_input('Enter your API key')
op = st.sidebar.selectbox('Select an option', ['current', 'forecast'])
if op == 'current':
    st.title('Today\'s Weather Information')
    city = st.text_input('Enter City Name')
    key = st.text_input('Enter key')
    if st.button('Get'):
        owm = pyowm.OWM(key)
        mgr = owm.weather_manager()
        obs = mgr.weather_at_place(city)
        weather = obs.weather
        temp = weather.temperature(unit='celsius')['temp']
        cloud = weather.clouds
        winds = weather.wind()['speed']
        sunrise = weather.sunrise_time(timeformat='iso')
        sunset = weather.sunset_time(timeformat='iso')
        st.write(f'Weather Information for {city.upper()}')
        st.write(f'Temperature: {temp}°C')
        st.write(f'Cloud Coverage: {cloud}%')
        st.write(f'Wind Speed: {winds}mph')
        st.write(f'Humidity: {weather.humidity}')
        st.write(f'Status: {weather.status} - {weather.detailed_status}')
        st.write(f'Sunrise Time: {sunrise}')
        st.write(f'Sunset Time: {sunset}')

else:
    st.title('Six-Day Weather Forecast')
    city = st.text_input('Enter City')
    key = st.text_input('Enter key')
    if st.button('Fetch'):
        owm = pyowm.OWM(key)
        mgr = owm.weather_manager()
        obs = mgr.forecast_at_place(city, '3h')

        forecast = obs.forecast
        df = pd.DataFrame()

        for weather in forecast:
            date = datetime.utcfromtimestamp(weather.reference_time())
            temp = weather.temperature('celsius')['temp']
            climate = weather.status
            sky = weather.detailed_status
            cloud = weather.clouds
            wind = weather.wind()['speed']
            humidity = weather.humidity

            df['Date'] = date
            df['Weather'] = climate
            df['Cloud (%)'] = cloud
            df['Temp (°C)'] = temp
            df['Wind (mph)'] = wind
            df['Humidity'] = humidity
            df['Sky'] = sky

        st.dataframe(df)






