from datetime import datetime
import pandas as pd
import streamlit as st
import pyowm
from pyowm.utils import timestamps



def main():
    st.sidebar.title('Get Weather Information')
    st.sidebar.info('Get your API key from OpenWeatherMap')
    op = st.sidebar.selectbox('Select an option', ['current', 'forecast'])
    if op == 'current':
        weather_today()
    else:
        weather_forecast()


key = st.sidebar.text_input('Enter API key')

@st.cache_resource
def get_weather(city):
    owm = pyowm.OWM(key)
    mgr = owm.weather_manager()
    obs = mgr.weather_at_place(city)
    return obs.weather


def weather_today():
    st.title('Today\'s Weather Information')
    city = st.text_input('Enter City Name')
    if st.button('Get'):
        weather = get_weather(city)
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




def forecast_weather(city):
    try:
       owm = pyowm.OWM(key)
       mgr = owm.weather_manager()
       obs = mgr.forecast_at_place(city, '3h')
       return obs
    except:
        st.error('An unknown error occurred!')



def weather_forecast():
    st.title('Six-Day Weather Forecast')
    city = st.text_input('Enter City')
#    forecast = forecast_weather(city)

    if st.button('Fetch'):
        obs = forecast_weather(city)
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





if __name__ == '__main__':
    main()
