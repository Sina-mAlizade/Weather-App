🌤️ Weather App

A simple and responsive weather application built with *Django* that provides detailed weather information for different cities.

✨ Features

- 🌡️ Current temperature
- 🌡️ Feels like temperature
- ⬇️ Minimum temperature
- ⬆️ Maximum temperature
- ☁️ Weather condition
- 💧 Humidity
- 🌬️ Wind speed and direction
- 📊 Atmospheric pressure
- 👁️ Visibility
- ☁️ Cloudiness
- ☀️ UV Index
- 🌅 Sunrise and sunset
- 🌫️ Air Quality
- 🗺️ Location on map
- 🔍 Search weather by city

🛠️ Technologies

- Python
- Django
- HTML
- CSS
- OpenWeather API
- Open-Meteo API

🚀 Installation
1. Clone the repository
git clone https://github.com/Sina-mAlizade/Weather-App.git


3. Enter the project directory

cd Weather-App-main


3. Create a virtual environment

python -m venv .venv


4. Activate the virtual environment
Windows:

.venv\Scripts\activate


5. Install the required packages

pip install -r requirements.txt


🔑 API Key

This project uses the *OpenWeather API* to retrieve weather information.
For security reasons, the API key is not included in this repository.
Before running the project, you need to add your own API key.
Open the following file:

main/views.py

Go to *line 7* and replace:

YOUR_API_KEY

with your own OpenWeather API key.

▶️ Run the Project

After adding your API key, run the Django development server:

python manage.py runserver



Made with ❤️ using Django and Python.
