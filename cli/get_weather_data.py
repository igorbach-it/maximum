#!/usr/bin/env python3
import sys, json, urllib.parse, urllib.request

API_TMPL = "https://wttr.in/{place}?format=j1"

def run(place: str) -> str:
    url = API_TMPL.format(place=urllib.parse.quote(place))
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    cur = data["current_condition"][0]
    area = data["nearest_area"][0]
    city = area["areaName"][0]["value"]
    region = area["region"][0]["value"]
    country = area["country"][0]["value"]
    return (f"{city}, {region}, {country}\n"
            f"Now: {cur['temp_C']}°C (feels {cur['FeelsLikeC']}°C), "
            f"{cur['weatherDesc'][0]['value']}; "
            f"Wind {cur['windspeedKmph']} km/h, Humidity {cur['humidity']}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli/get_weather_data.py <City>")
        sys.exit(1)
    try:
        print(run(" ".join(sys.argv[1:])))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)
