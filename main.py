from weatherbit.api import Api
import pandas as pd
import streamlit as st


st.title('A Seven-Day Weather Forecast App')
key = st.text_input('Enter key')
api = Api(key)


@st.cache_resource
def weather_forecast(city, state, country):
    api = Api(key)
    forecast = api.get_forecast(city=city, state=state, country=country)
    return forecast

left, right = st.columns(2)
city = left.text_input('Enter City')
state = right.text_input('Enter City State')
country = st.text_input('Enter Country')
op = st.selectbox('Make a choice', ['DataFrame', 'BarChart', 'LineChart'])
if st.button('Fetch'):
    forecast = weather_forecast(city, state, country)
    dates = []
    precips = []
    weather = []
    wind = []
    temp = []
    for day in forecast.get_series(['temp', 'precip', 'weather','wind_spd' ,'datetime']):
        dates.append(day['datetime'].date())
        temp.append(day['temp'])
        precips.append(day['precip'])
        weather.append(day['weather']['description'])
        wind.append(day['wind_spd'])
    df = pd.DataFrame({'Date': dates, 'Temp': temp, 'Precip': precips, 'Wind Speed': wind, 'Weather': weather})
    if op == 'DataFrame':
        st.dataframe(df)
    elif op == 'BarChart':
        st.bar_chart(df.Temp)
    else:
        st.line_chart(df.Temp)


