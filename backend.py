import requests

API_KEY = "6ff8ff21eb30ff5c8581dbc331b8f893"


def get_data(place, forecast_days=None, kind=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

#get data is only triggered when used directly and not imported anywhere else
if __name__ =="__main__":
    print(get_data(place="Tokyo"))




