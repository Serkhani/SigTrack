from PySide2.QtWidgets import (QWidget, QVBoxLayout,QLabel,QHBoxLayout,
                               QPushButton)
from PySide2.QtGui import QPixmap, QFont
from PySide2.QtCore import Qt 
from datetime import datetime
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")

        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.cityName = "Accra"
        self.api_key = 'd2ed8137acc17a02bcd284b4548d5b88'
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

        self.weather_label = QLabel()
        self.weather_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.weather_label)

        self.weather_icon_label = QLabel()
        self.layout.addWidget(self.weather_icon_label)

        temperature_layout = QHBoxLayout()
        self.layout.addLayout(temperature_layout)

        temperature_icon = QLabel()
        temperature_icon.setPixmap(QPixmap(":/qt_icons/temperature_icon.svg").scaled(30, 30))
        temperature_layout.addWidget(temperature_icon)

        self.temperature_label = QLabel()
        temperature_layout.addWidget(self.temperature_label)

        humidity_layout = QHBoxLayout()
        self.layout.addLayout(humidity_layout)

        humidity_icon = QLabel()
        humidity_icon.setPixmap(QPixmap(":/qt_icons/humidity_icon.svg").scaled(30, 30))
        humidity_layout.addWidget(humidity_icon)

        self.humidity_label = QLabel()
        humidity_layout.addWidget(self.humidity_label)

        wind_speed_layout = QHBoxLayout()
        self.layout.addLayout(wind_speed_layout)

        wind_icon = QLabel()
        wind_icon.setPixmap(QPixmap(":/qt_icons/wind_speed_icon.svg").scaled(30, 30))
        wind_speed_layout.addWidget(wind_icon)

        self.wind_speed_label = QLabel()
        wind_speed_layout.addWidget(self.wind_speed_label)

        pressure_layout = QHBoxLayout()
        self.layout.addLayout(pressure_layout)

        pressure_icon = QLabel()
        pressure_icon.setPixmap(QPixmap(":/qt_icons/air_pressure.svg").scaled(30, 30))
        pressure_layout.addWidget(pressure_icon)

        self.pressure_label = QLabel()
        pressure_layout.addWidget(self.pressure_label)

        sea_level_layout = QHBoxLayout()
        self.layout.addLayout(sea_level_layout)

        sea_level_icon = QLabel()
        sea_level_icon.setPixmap(QPixmap(":/qt_icons/sea-level.svg").scaled(30, 30))
        sea_level_layout.addWidget(sea_level_icon)

        self.sea_level_label = QLabel()
        sea_level_layout.addWidget(self.sea_level_label)

        ground_level_layout = QHBoxLayout()
        self.layout.addLayout(ground_level_layout)

        ground_level_icon = QLabel()
        ground_level_icon.setPixmap(QPixmap(":/qt_icons/sea-level.svg").scaled(30, 30))
        ground_level_layout.addWidget(ground_level_icon)

        self.ground_level_label = QLabel()
        ground_level_layout.addWidget(self.ground_level_label)

        visibility_layout = QHBoxLayout()
        self.layout.addLayout(visibility_layout)

        visibility_icon = QLabel()
        visibility_icon.setPixmap(QPixmap(":/qt_icons/visibility.svg").scaled(30, 30))
        visibility_layout.addWidget(visibility_icon)

        self.visibility_label = QLabel()
        visibility_layout.addWidget(self.visibility_label)

        gust_layout = QHBoxLayout()
        self.layout.addLayout(gust_layout)

        gust_icon = QLabel()
        gust_icon.setPixmap(QPixmap(":/qt_icons/gust.svg").scaled(30, 30))
        gust_layout.addWidget(gust_icon)

        self.gust_label = QLabel()
        gust_layout.addWidget(self.gust_label)

        clouds_layout = QHBoxLayout()
        self.layout.addLayout(clouds_layout)

        clouds_icon = QLabel()
        clouds_icon.setPixmap(QPixmap(":/qt_icons/weather_icon.svg").scaled(30, 30))
        clouds_layout.addWidget(clouds_icon)

        self.clouds_label = QLabel()
        clouds_layout.addWidget(self.clouds_label)

        country_layout = QHBoxLayout()
        self.layout.addLayout(country_layout)

        country_icon = QLabel()
        country_icon.setPixmap(QPixmap(":/qt_icons/country-flag.svg").scaled(30, 30))
        country_layout.addWidget(country_icon)

        self.country_label = QLabel()
        country_layout.addWidget(self.country_label)

        sunrise_layout = QHBoxLayout()
        self.layout.addLayout(sunrise_layout)

        sunrise_icon = QLabel()
        sunrise_icon.setPixmap(QPixmap(":/qt_icons/sunrise.svg").scaled(30, 30))
        sunrise_layout.addWidget(sunrise_icon)

        self.sunrise_label = QLabel()
        sunrise_layout.addWidget(self.sunrise_label)

        sunset_layout = QHBoxLayout()
        self.layout.addLayout(sunset_layout)

        sunset_icon = QLabel()
        sunset_icon.setPixmap(QPixmap(":/qt_icons/sunset.svg").scaled(30, 30))
        sunset_layout.addWidget(sunset_icon)

        self.sunset_label = QLabel()
        sunset_layout.addWidget(self.sunset_label)

        self.refresh_button = QPushButton("Refresh Weather")
        self.refresh_button.clicked.connect(self.refresh_weather)
        self.layout.addWidget(self.refresh_button)

        self.refresh_weather()

    def refresh_weather(self):
        self.refresh_button.setEnabled(False)
        try:
            url = f"{self.BASE_URL}?q={self.cityName}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            sea_level = data['main'].get('sea_level', 'N/A')
            ground_level = data['main'].get('grnd_level', 'N/A')
            visibility = data.get('visibility', 'N/A')
            gust = data['wind'].get('gust', 'N/A')
            clouds = data['clouds']['all']
            country = data['sys']['country']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']

            icon_name = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_name}.png"
            icon_data = requests.get(icon_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)

            weather_report = f"Weather: {weather_description}"
            self.weather_label.setText(weather_report)
            self.weather_icon_label.setPixmap(pixmap)

            self.temperature_label.setText(f"{temperature}°C")
            self.humidity_label.setText(f"{humidity}%")
            self.wind_speed_label.setText(f"{wind_speed} m/s")
            self.pressure_label.setText(f"{pressure} hPa")
            self.sea_level_label.setText(f"{sea_level} m")
            self.ground_level_label.setText(f"{ground_level} m")
            self.visibility_label.setText(f"{visibility} meters")
            self.gust_label.setText(f"{gust} m/s")
            self.clouds_label.setText(f"{clouds}%")
            self.country_label.setText(f"{country}")
            self.sunrise_label.setText(f"{datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')}")
            self.sunset_label.setText(f"{datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.refresh_button.setEnabled(True)

