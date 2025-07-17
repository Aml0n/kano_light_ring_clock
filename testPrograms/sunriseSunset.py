import time
from datetime import datetime, date as dt, date
# import time_functions as tf
import openmeteo_requests
import requests_cache
from retry_requests import retry
import csv

def sunriseSunset():

    today = date.today().timestamp()
    formattedToday = today.strftime("%Y-%m-%d")

    timestamps = {}
    rowFound = False

    with open('savedData/savedSunriseSunset.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == formattedToday:
                timestamps = row
                rowFound = True
        # if row matching the date
        if not rowFound:
            print("uh oh")
        
def getSunriseSunsetData():
    cacheSession = requests_cache.CachedSession('.cache', expire_after = 3600)
    retrySession = retry(cacheSession, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retrySession)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": 34.060583399368205,
	"longitude": -118.24431504690445,
	"daily": ["sunset", "sunrise"],
	"timezone": "America/Los_Angeles"
    }   

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0] 
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    
    daily = response.Daily()
    dailySunset = daily.Variables(0).ValuesInt64AsNumpy()
    dailySunrise = daily.Variables(1).ValuesInt64AsNumpy()
    
    dailyDays = []
    for timestamp in dailySunset:
        dateObj = dt.fromtimestamp(timestamp)
        dailyDays.append(dateObj.strftime("%Y-%m-%d"))

    csvRows = []
    for itemNum in range(len(dailySunset)):
        csvRows.append([dailyDays[itemNum], int(dailySunrise[itemNum]), int(dailySunset[itemNum])])
    print(csvRows)
    # print(dailyDays)
    # print(whatDayIsIt)
    # print(dailySunset)
    # print(dailySunrise)
    # print(daily)

                

startTime = time.time()
callOpenMeteo()
endTime = time.time()

elapsedTime = endTime - startTime
print(f'ran in {elapsedTime} s')