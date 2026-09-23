import os
from datetime import datetime, timedelta, timezone
import requests
from django.shortcuts import render
from .models import SearchHistory

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY")


def degrees_to_compass(deg):

    if deg is None:
        return None
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(deg / 45) % 8
    return directions[index]


def unix_to_local_time(unix_ts, tz_offset_seconds):

    if unix_ts is None:
        return None
    dt = datetime.fromtimestamp(unix_ts, tz=timezone.utc) + timedelta(seconds=tz_offset_seconds)
    return dt.strftime('%H:%M')


def aqi_category(us_aqi):

    if us_aqi is None:
        return None, None
    if us_aqi <= 50:
        return "Good", "#4caf50"
    if us_aqi <= 100:
        return "Moderate", "#ffca28"
    if us_aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#ff9800"
    if us_aqi <= 200:
        return "Unhealthy", "#e53935"
    if us_aqi <= 300:
        return "Very Unhealthy", "#8e24aa"
    return "Hazardous", "#7e0023"


def index(request):
    weather = None
    error = None
    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]

    if request.method == "POST":
        city = request.POST.get('city', '').strip()
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                resp = requests.get(url, timeout=5)
                data = resp.json()

                if resp.status_code == 200:
                    tz_offset = data.get('timezone', 0)
                    wind_deg = data.get('wind', {}).get('deg')
                    lat = data.get('coord', {}).get('lat')
                    lon = data.get('coord', {}).get('lon')

                    uv_index = None
                    if lat is not None and lon is not None:
                        uv_url = (
                            f"https://api.open-meteo.com/v1/forecast"
                            f"?latitude={lat}&longitude={lon}&current=uv_index"
                        )
                        try:
                            uv_response = requests.get(uv_url, timeout=15)
                            uv_data = uv_response.json()
                            uv_index = uv_data["current"]["uv_index"]
                        except (requests.RequestException, KeyError, ValueError) as e:
                            print("UV index fetch failed for", city, "->", repr(e))
                            uv_index = None

                    us_aqi = None
                    if lat is not None and lon is not None:
                        aqi_url = (
                            "https://air-quality-api.open-meteo.com/v1/air-quality"
                            f"?latitude={lat}&longitude={lon}&current=us_aqi"
                        )
                        try:
                            aqi_response = requests.get(aqi_url, timeout=15)
                            aqi_data = aqi_response.json()
                            us_aqi = aqi_data["current"]["us_aqi"]
                        except (requests.RequestException, KeyError, ValueError):
                            us_aqi = None
                    aqi_label, aqi_color = aqi_category(us_aqi)


                    map_url = None
                    if lat is not None and lon is not None:
                        delta = 0.08
                        map_url = (
                            "https://www.openstreetmap.org/export/embed.html"
                            f"?bbox={lon - delta},{lat - delta},{lon + delta},{lat + delta}"
                            f"&marker={lat},{lon}"
                        )

                    weather = {
                        'city': f"{data['name']}, {data['sys']['country']}",
                        'temperature': data['main']['temp'],
                        'feels_like': data['main'].get('feels_like'),
                        'temp_min': data['main'].get('temp_min'),
                        'temp_max': data['main'].get('temp_max'),
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'cloudiness': data.get('clouds', {}).get('all'),
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon'],
                        'wind_speed': data.get('wind', {}).get('speed'),
                        'wind_direction': degrees_to_compass(wind_deg),
                        'visibility': data.get('visibility'),
                        'sunrise': unix_to_local_time(data['sys'].get('sunrise'), tz_offset),
                        'sunset': unix_to_local_time(data['sys'].get('sunset'), tz_offset),
                        'latitude': lat,
                        'longitude': lon,
                        'map_url': map_url,
                        'uv_index': uv_index,
                        'aqi': us_aqi,
                        'aqi_label': aqi_label,
                        'aqi_color': aqi_color,
                    }

                    SearchHistory.objects.create(
                        city_name=data['name'],
                        temperature=data['main']['temp'],
                        feels_like=data['main'].get('feels_like'),
                        temp_min=data['main'].get('temp_min'),
                        temp_max=data['main'].get('temp_max'),
                        humidity=data['main']['humidity'],
                        pressure=data['main']['pressure'],
                        cloudiness=data.get('clouds', {}).get('all'),
                        description=data['weather'][0]['description'].title(),
                        wind_speed=data.get('wind', {}).get('speed'),
                        wind_direction=degrees_to_compass(wind_deg),
                        visibility=data.get('visibility'),
                        sunrise=weather['sunrise'],
                        sunset=weather['sunset'],
                        latitude=lat,
                        longitude=lon,
                        uv_index=uv_index,
                        aqi=us_aqi,
                        aqi_category=aqi_label,
                    )

                    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
                else:
                    error = data.get("message", "Could not fetch weather data.")
            except requests.RequestException:
                error = "Network error. Please try again."
        else:
            error = "Please enter a city name."

    return render(request, "index.html", {
        'weather': weather,
        'error': error,
        'recent_searches': recent_searches
    })

