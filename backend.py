import requests
from datetime import datetime, timedelta

API_KEY = "6ff8ff21eb30ff5c8581dbc331b8f893"

def get_data(place, forecast_days):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]

    #get city dictionary
    city = data["city"]

    #get place coordinates
    co_ord = city["coord"]
    long = co_ord['lon']
    lat = co_ord['lat']
    offset = city["timezone"]

    return filtered_data, offset, long, lat


def get_current_weather(lon, lat):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    coord_data = data

    return coord_data

#Can only triggered when used directly from this file
if __name__ =="__main__":
    #print(get_data(place="zurich", forecast_days=1,))
    #print(get_time(7200))
    get_current_weather(8.55, 47.3667)


