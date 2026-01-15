import requests

URL = "https://opensky-network.org/api/states/all"

def get_flights():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.json()["states"]
