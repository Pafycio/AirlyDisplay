from os import system
import requests
import attr
from datetime import datetime, timedelta

# STATIC


@attr.s(frozen=True)
class AirlyWeather(object):
    airQualityIndex = attr.ib(converter=int, default=-1)
    humidity = attr.ib(converter=int, default=-1)
    pm1 = attr.ib(converter=int, default=-1)
    pm10 = attr.ib(converter=int, default=-1)
    pm25 = attr.ib(converter=int, default=-1)
    pollutionLevel = attr.ib(converter=int, default=-1)
    pressure = attr.ib(converter=int, default=-1)
    temperature = attr.ib(convert=int, default=-99)
    windDirection = attr.ib(convert=int, default=0)
    windSpeed = attr.ib(convert=int, default=0)


@attr.s(frozen=True)
class OpenWeather(object):
    temp_max = attr.ib(default=-1)
    temp_min = attr.ib(default=-1)
    temp = attr.ib(default=-1)
    humidity = attr.ib(default=-1)
    pressure = attr.ib(default=-1)


class Handler(object):
    def __init__(self, apikey, url, request_delay):
        """
        :param apikey: you can get your key there https://developer.airly.eu/
        :var request_delay: delay between GET in minutes
        :var next_req: time when we should update data
        :var result: GET result in Weather object
        """
        self.apikey = apikey
        self.URL = url
        self.request_delay = request_delay

        self._next_req = datetime.now()
        self.result = None
        self.status = None
        self.connected = False

    def isUpdateTime(self):
        now = datetime.now()
        if now >= self._next_req:
            self._next_req = now + timedelta(minutes=self.request_delay)
            return True
        return False

    def getURL(self, latitude, longitude):
        return self.URL.format(latitude, longitude, self.apikey)

    def executeRequest(self, latitude, longitude):
        with requests.Session() as s:
            r = s.get(self.getURL(latitude, longitude))
            self.status = r.status_code
            self.result = r.json()

    def updateResult(self, latitude, longitude):
        if self.isUpdateTime() and self.isConnected():
            self.executeRequest(latitude, longitude)

    def getCurrentWeather(self, latitude, longitude):
        raise NotImplemented('Not implemented !')

    def isConnected(self):
        connection = system('ping -c 1 google.com')

        if connection:
            self.connected = True
        else:
            self.connected = False

        return self.connected


class AirlyHandler(Handler):
    def __init__(self, apikey):
        super().__init__(apikey,
                         'https://airapi.airly.eu/v1/mapPoint/measurements?latitude={}&longitude={}&apikey={}',
                         5)

    def getCurrentWeather(self, latitude, longitude):
        self.updateResult(latitude, longitude)
        if self.status == 200:
            current = self.result['currentMeasurements']
            return AirlyWeather(**current)
        return AirlyWeather()


class OpenWeatherHandler(Handler):
    def __init__(self, apikey):
        super().__init__(apikey,
                         'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&apikey={}&units=metric',
                         1)

    def getCurrentWeather(self, latitude, longitude):
        self.updateResult(latitude, longitude)
        if self.status == 200:
            current = self.result['main']
            return OpenWeather(**current)
        return OpenWeather()
