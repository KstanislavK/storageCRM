import requests


def get_dollar_price(request):
    course = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    data = {
        'd_value_now': course['Valute']['USD']['Value'],
        'd_value_prev': course['Valute']['USD']['Previous'],
        'yu_value_now': course['Valute']['CNY']['Value'],
        'yu_value_prev': course['Valute']['CNY']['Previous'],
        'kr_value_now': course['Valute']['KRW']['Value'],
        'kr_value_prev': course['Valute']['KRW']['Previous']
    }
    return data


def get_weather(request):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&units=metric&appid=6a06fb4cd4988c4ceae31c228db05cdc&lang=ru"

    weather_data = requests.get(url).json()
    data = {
        "icon": f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}.png",
        "temp": f"{weather_data['main']['temp']}",
        "conditions": weather_data['weather'][0]['description']
    }
    return data
