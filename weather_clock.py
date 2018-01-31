import requests
import attr
from datetime import datetime, timedelta

# STATIC
URL = 'https://airapi.airly.eu/v1/mapPoint/measurements?latitude={}&longitude={}&apikey={}'


@attr.s(frozen=True)
class Weather(object):
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


class RequestHandler(object):
    def __init__(self, apikey):
        """
        :param apikey: you can get your key there https://developer.airly.eu/
        :var request_delay: delay between GET in minutes
        :var next_req: time when we should update data
        :var result: GET result in Weather object 
        """
        self.apikey = apikey
        self.request_delay = 5
        self.next_req = datetime.now()
        self.result = None

    def getURL(self, latitude, longitude):
        return URL.format(latitude, longitude, self.apikey)

    def getResult(self, latitude, longitude):
        now = datetime.now()
        if now >= self.next_req:
            self.next_req = now + timedelta(minutes=self.request_delay)
            self.result = self.getCurrentWeather(latitude, longitude)

        return self.result

    def getCurrentWeather(self, latitude, longitude):
        with requests.Session() as s:
            r = s.get(self.getURL(latitude, longitude))
            self.result = r.json()
            current = self.result['currentMeasurements']
            return Weather(**current)

    def getForecastWeather(self, latitude, longitude):
        with requests.Session() as s:
            r = s.get(self.getURL(latitude, longitude))
            self.result = r.json()
            forecast = self.result['forecast']['measurements']
            return Weather(**forecast)
