import geocoder
import config
import utils
import requests
import datetime

from translate import Translator

class Weather:

    def __init__(self, command, response) :
        self.os = config.OS_NAME
        self.command = command
        self.response = response
        self.language = 'en-EN'
        if config.OS_NAME == 'Alex' :
            self.language = 'vi-VI'
            

    def launch(self):
        city = geocoder.ip('me').city
        api_key = "9f8c52b27a25d36460e1062e930f58ea"
        call_url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + api_key + "&q=" + city + "&units=metric"
        data= requests.get(call_url)
        data = data.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            now = datetime.datetime.now()
            weather_description = Translator(to_lang=self.language).translate(wthr[0]["description"])
            utils.speak(self.response .format(day = now.day,month = now.month, year= now.year,hourrise = sunrise.hour, minrise = sunrise.minute,hourset = sunset.hour, 
                                    minset = sunset.minute, temp = current_temperature, pressure = current_pressure, 
                                    humidity = current_humidity, weather = weather_description))