from debug import *
from config import *
from utils import *
import json
import urllib.request
import time as Time
from time import strftime
from time import strptime
import datetime
from weather import *
from weatherHours import *


class JsonWeather:
    global HIGH_RAIN
    weathers = [None, None, None]

    def __init__(self, url):
        try:
            with urllib.request.urlopen(url) as url:
                date = strftime("%d-%m-%Y", Time.gmtime())
                today = datetime.datetime.today()
                tomorrow = today + datetime.timedelta(1)
                '''day = date.split("-")[0]
                month = date.split("-")[1]
                year = date.split("-")[2]
                dt = "" '''
                data = json.loads(url.read().decode())
                temp_min = None
                temp_max = None
                humidity = None
                weather = None
                description = None
                cloud_perc = None
                wind_speed = None
                self.weathers[0] = None
                self.weathers[1] = None
                self.weathers[2] = None
                self.weathers[0] = Weather(is_today=True)
                self.weathers[1] = Weather(is_today=False)
                self.weathers[2] = Weather(is_today=True)

                for t in data["list"]:
                    temp_min_tmp = t["main"]["temp_min"]
                    temp_max_tmp = t["main"]["temp_max"]
                    humidity_tmp = t["main"]["humidity"]
                    weather_tmp = t["weather"][0]["main"].lower()
                    description = t["weather"][0]["description"].lower()
                    cloud_perc_tmp = t["clouds"]["all"]
                    wind_speed_tmp = t["wind"]["speed"]
                    dt_tmp = datetime.datetime.strptime(t["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    if temp_min is None:
                        temp_min = t["main"]["temp_min"]
                        temp_max = t["main"]["temp_max"]
                        humidity = t["main"]["humidity"]
                        weather = t["weather"][0]["main"].lower()
                        cloud_perc = t["clouds"]["all"]
                        wind_speed = t["wind"]["speed"]
                        # NOW current weather
                        self.weathers[2].temp_min = t["main"]["temp_min"]
                        self.weathers[2].temp_max = t["main"]["temp_max"]
                        self.weathers[2].humidity = t["main"]["humidity"]
                        self.weathers[2].weather = weather
                        self.weathers[2].cloud_perc = t["clouds"]["all"]
                        self.weathers[2].wind_speed = t["wind"]["speed"]
                        if weather_tmp.find("rain") > -1:
                            tmp = self.weathers[2].rain_hours.copy()
                            self.weathers[2].rain_hours.clear()
                            vol = 0
                            rain_high = False
                            if 'rain' in t and '3h' in t["rain"]:
                                vol = t["rain"]["3h"]
                                if float(t["rain"]["3h"]) > HIGH_RAIN:
                                    rain_high = True
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, vol))
                            self.weathers[2].rain_hours = tmp.copy()
                        elif weather_tmp.find("snow") > -1:
                            tmp = self.weathers[2].snow_hours.copy()
                            self.weathers[2].snow_hours.clear()
                            vol = 0
                            if 'snow' in t and '3h' in t["snow"]:
                                vol = t["snow"]["3h"]
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, vol))
                            self.weathers[2].snow_hours = tmp.copy()
                    delta = dt_tmp - today
                    #print(dt_tmp, today)
                    if dt_tmp.day == today.day and dt_tmp.month == today.month:
                        # print("today")
                        # print(delta.days, temp_min, temp_max, humidity, weather, cloud_perc, wind_speed, t["dt_txt"])
                        #print("today", self.weathers[1].rain_hours)

                        if weather_tmp.find("rain") > -1:
                            tmp = self.weathers[0].rain_hours.copy()
                            self.weathers[0].rain_hours.clear()
                            vol = 0
                            rain_high = False
                            if 'rain' in t and '3h' in t["rain"]:
                                vol = t["rain"]["3h"]
                                if float(t["rain"]["3h"]) > HIGH_RAIN:
                                    rain_high = True
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, vol))
                            self.weathers[0].rain_hours = tmp.copy()
                        elif weather_tmp.find("snow") > -1:
                            tmp = self.weathers[0].snow_hours.copy()
                            self.weathers[0].snow_hours.clear()
                            vol = 0
                            if 'snow' in t and '3h' in t["snow"]:
                                vol = t["snow"]["3h"]
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, vol))
                            self.weathers[0].snow_hours = tmp.copy()

                        if 'rain' in t and '3h' in t["rain"]:
                            self.weathers[0].rain_volume.append(t["rain"]["3h"])
                            if float(t["rain"]["3h"]) > HIGH_RAIN:
                                self.weathers[0].rain_high = True
                        if 'snow' in t and '3h' in t["snow"]:
                            self.weathers[0].snow_volume.append(t["snow"]["3h"])

                        if temp_min_tmp < temp_min or self.weathers[0].temp_min is None:
                            self.weathers[0].temp_min = temp_min_tmp
                        if temp_max_tmp > temp_max or self.weathers[0].temp_max is None:
                            self.weathers[0].temp_max = temp_max_tmp
                        if humidity_tmp > humidity or self.weathers[0].humidity is None:
                            self.weathers[0].humidity = humidity_tmp
                        if cloud_perc_tmp > cloud_perc or self.weathers[0].cloud_perc is None:
                            self.weathers[0].cloud_perc = cloud_perc_tmp
                        if wind_speed_tmp > wind_speed or self.weathers[0].wind_speed is None:
                            self.weathers[0].wind_speed = wind_speed_tmp
                        if weather_tmp == "snow" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "thunderstorm" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "rain" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "shower rain" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "mist" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "broken clouds" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "scattered clouds" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "few clouds" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                        elif weather_tmp == "clear sky" or self.weathers[0].weather is None:
                            self.weathers[0].weather = weather_tmp
                    elif dt_tmp.day == tomorrow.day and dt_tmp.month == tomorrow.month:
                        # print("tomorrow")
                        if weather_tmp.find("rain") > -1:
                            tmp = self.weathers[1].rain_hours.copy()
                            self.weathers[1].rain_hours.clear()
                            vol = 0
                            rain_high = False
                            if 'rain' in t and '3h' in t["rain"]:
                                vol = t["rain"]["3h"]
                                if float(t["rain"]["3h"]) > HIGH_RAIN:
                                    rain_high = True
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, vol))
                            self.weathers[1].rain_hours = tmp.copy()

                        if weather_tmp.find("snow") > -1:
                            tmp = self.weathers[1].snow_hours.copy()
                            self.weathers[1].snow_hours.clear()
                            vol = 0
                            if 'snow' in t and '3h' in t["snow"]:
                                vol = t["snow"]["3h"]
                            tmp.append(WeatherHours(t["dt_txt"].split(" ")[1][:-3], description, 0, vol))
                            self.weathers[1].snow_hours = tmp.copy()

                        if 'rain' in t and '3h' in t["rain"]:
                            self.weathers[1].rain_volume.append(t["rain"]["3h"])
                            if float(t["rain"]["3h"]) > HIGH_RAIN:
                                self.weathers[1].rain_high = True

                        if 'snow' in t and '3h' in t["snow"]:
                            self.weathers[1].snow_volume.append(t["snow"]["3h"])

                        if temp_min_tmp < temp_min or self.weathers[1].temp_min is None:
                            self.weathers[1].temp_min = temp_min_tmp
                        if temp_max_tmp > temp_max or self.weathers[1].temp_max is None:
                            self.weathers[1].temp_max = temp_max_tmp
                        if humidity_tmp > humidity or self.weathers[1].humidity is None:
                            self.weathers[1].humidity = humidity_tmp
                        if cloud_perc_tmp > cloud_perc or self.weathers[1].cloud_perc is None:
                            self.weathers[1].cloud_perc = cloud_perc_tmp
                        if wind_speed_tmp > wind_speed or self.weathers[1].wind_speed is None:
                            self.weathers[1].wind_speed = wind_speed_tmp
                        if weather_tmp == "snow" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "thunderstorm" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "rain" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "shower rain" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "mist" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "broken clouds" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "scattered clouds" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "few clouds" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
                        elif weather_tmp == "clear sky" or self.weathers[1].weather is None:
                            self.weathers[1].weather = weather_tmp
        except Exception as e:
            # print(e)
            weathers = [None, None, None]

    def get_weathers(self):
        return self.weathers

