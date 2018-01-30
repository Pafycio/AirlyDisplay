import requests
import attr

# TODO:
# Wyswietlacz na rasbi i2c
# Wyswietlanie info
# Godzina

# STATIC
URL = 'https://airapi.airly.eu/v1/mapPoint/measurements?latitude={}&longitude={}&apikey={}'
APIKEY = '474c2774e7d142548c5a8b0d121c0d15'


@attr.s(frozen=True)
class Weather(object):
    airQualityIndex = attr.ib(converter=int, default=0)
    humidity = attr.ib(converter=int, default=0)
    pm1 = attr.ib(converter=int, default=0)
    pm10 = attr.ib(converter=int, default=0)
    pm25 = attr.ib(converter=int, default=0)
    pollutionLevel = attr.ib(converter=int, default=0)
    pressure = attr.ib(converter=int, default=0)
    temperature = attr.ib(convert=int, default=0)

def getURL(latitude, longitude):
    return URL.format(latitude, longitude, APIKEY)


def getData():
    with requests.Session() as s:
        r = s.get(getURL('50.07874', '20.02901'))
        result = r.json()['currentMeasurements']
        weather = Weather(**result)
        print(weather)
        return weather