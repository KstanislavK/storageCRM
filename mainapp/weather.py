import requests

CITY_NAME = 'Moscow'
API_KEY = '6a06fb4cd4988c4ceae31c228db05cdc'
LANG = 'ru'
UNITS = 'metric'

URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&units={UNITS}&appid={API_KEY}&lang={LANG}"

data = requests.get(URL).json()
weather_data = {
    "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png",
    "temp": f"{data['main']['temp']}&deg;С",
    "conditions": data['weather'][0]['description']
}

print(weather_data)
