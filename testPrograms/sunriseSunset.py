import time
from datetime import datetime, date as dt, date
# import time_functions as tf
import openmeteo_requests
import requests_cache
from retry_requests import retry
import csv
import os

def createSaveFile(): # if the csv doesn't already exist, create it
    try:
        newCSV = open("savedData/savedSunriseSunset.csv", "x")
        newCSV.close()
        print("save file created")
        return
    except FileExistsError:
        print("save file already exists")
        return

def deleteOldCache():
    today = date.today()
    formattedToday = today.strftime("%Y-%m-%d")
    # formattedToday = "2025-07-20"
    # todayTimestamp = today.timestamp()
    with open("savedData/savedSunriseSunset.csv", 'r', newline='') as infile, \
         open("savedData/temp.csv", 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['date', 'sunriseTime', 'sunsetTime']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # next(reader, default) # skips header row
        # writer.writeheader()
        for row in reader:
            rowDate = row["date"]
            try:
                rowDateObj = datetime.strptime(rowDate, "%Y-%m-%d").date()
                formattedTodayObj = datetime.strptime(formattedToday, "%Y-%m-%d").date()
                if rowDateObj >= formattedTodayObj:
                    writer.writerow(row)
                    print("wrote the row :3")
                else:
                    print("did NOT write the row")
            except ValueError:
                print(f"Invalid date format in row: {rowDate}")

    with open('savedData/temp.csv', 'r', newline='') as infile, \
         open('savedData/savedSunriseSunset.csv', 'w', newline='') as outfile:
        reader = csv.reader(infile)
        fieldnames = ['date', 'sunriseTime', 'sunsetTime']
        writer = csv.writer(outfile)
        
        writer.writerow(['date', 'sunriseTime', 'sunsetTime'])
        for row in reader:
            print(row[0])
            writer.writerow(row)

    fileToRemove = "savedData/temp.csv"
    try:
        os.remove(fileToRemove)
        print(f"deleted {fileToRemove}")
    except FileNotFoundError:
        print(f"{fileToRemove} not found")
    except Exception as exception:
        print(f"an error occured: {exception}")        

    # with open("savedData/savedSunriseSunset.csv", mode="w", newline="") as file:
    #     writer = csv.writer(file)
    #     for row in writer:
    #         if row[0] == formattedToday:
    #             row = ""

def sunriseSunset():

    createSaveFile()
    deleteOldCache()


    today = date.today()
    formattedToday = today.strftime("%Y-%m-%d")

    timestamps = {}
    rowFound = False

    with open('savedData/savedSunriseSunset.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == formattedToday:
                timestamps = row
                rowFound = True
                break

        # if row matching the date isn't found
        if not rowFound:
            csvRows = getSunriseSunsetData()
            appendCsv(csvRows)
            
def appendCsv(rows):
    with open('savedData/savedSunriseSunset.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

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
    return csvRows
    # print(dailyDays)
    # print(whatDayIsIt)
    # print(dailySunset)
    # print(dailySunrise)
    # print(daily)

                

startTime = time.time()
sunriseSunset()
endTime = time.time()

elapsedTime = endTime - startTime
print(f'ran in {elapsedTime} s')