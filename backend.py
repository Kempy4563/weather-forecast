import requests

API_KEY = "6ff8ff21eb30ff5c8581dbc331b8f893"

https://api.openweathermap.org/data/2.5/forecast?q={place}&units=metric&appid={API_KEY}

def get_data(place, forecast_days):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]

    return filtered_data


#get data is only triggered when used directly and not imported anywhere else


if __name__ =="__main__":
    print(get_data(place="Manchester", forecast_days=1,))




