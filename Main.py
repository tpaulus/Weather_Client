#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

from lib.Char_Plate.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import WUndergroundAPI
import time
import smbus
import os

locations = {}

app_info_folder = '/etc/WeatherUnderground'
LocationData = app_info_folder + '/locations.conf'
parameters = app_info_folder + '/parameters.conf'

lcd = Adafruit_CharLCDPlate(busnum = 1)
API = WUndergroundAPI.WebAPI()
lcd.clear()
lcd.backlight(lcd.ON)

try:
    info = open(LocationData)
    data = info.readlines()
    length = int(str(data).count(',')) + 1
    l1 = data[0].split(',')
    for x in range (0,length):
        l2 = l1[x].split(':')
        locations[str(x)+'s'] = l2[0]
        locations[str(x)+'c'] = l2[1]
    info.close()

except IOError:
    lcd.message('Welcome\nNew User!')
    print 'Adding New Location...'
    State = raw_input('Enter The name of the State your desired location is in, using the abbreviation -CA\n')
    City = raw_input('Now, Enter the name of the City\n')
    print '\nThank You!'
    State = State.replace('\n', '').upper()
    City = City.replace('\n', '').capitalize()
    if not os.path.exists(app_info_folder):
        os.makedirs(app_info_folder)
    info = open(LocationData, 'w')
    info.write(State + ':' + City)
    locations = {'0' + 's': State, '0' + 'c': City}
    info.close()

try:
    pram = open(parameters,'r')
    token = str(pram.readline()).replace('\n','')
    units_Temp = str(pram.readline()).replace('\n','')
    units_Speed = str(pram.readline()).replace('\n','')
    language = str(pram.readline()).replace('\n','')

    pram.close()

except IOError:
    pram = open(parameters,'w')
    token = raw_input('Please Enter Your WUnderground API Key:\n').replace('\n','')
    pram.write(token+'\n'+'fahrenheit'+'\n'+'mph'+'\n'+'eng')
    units_Temp = 'fahrenheit'
    units_Speed = 'mph'
    language =  'eng'
    pram.close()
#    set defaults if no file exists

locationCount = len(locations)/2
if locationCount == 0:
    quit('Error - No Locations!')

location = 0

displayCount = 3

update = True
display = 0
stateChange = False
json = ''
wait = 0
#Local Functions are below, all others at in WUndergroundAPI.py
#The following functions need to be preformed locally to avoid LCD conflicts


def init():
    lcd.clear()
    lcd.backlight(lcd.ON)
    lcd.message('Weather Client\nfor Raspberry Pi')
    time.sleep(1)
    lcd.clear()
    lcd.message('Version 1.0\nTom Paulus 2013')
    time.sleep(1)
    lcd.clear()

def locationChanger(origin,locations,location):
    lcd.clear()
    done = False
    blankScreen = True

    if origin == 'right':
        location = (location + 1)%locationCount

    if origin == 'left':
        location = (location -1)%locationCount
#       Make first button Change

    while not done:
        if blankScreen:
            lcd.clear()
            stateRAW = locations.get(str(location)+'s')
            stateFull = API.USCode(stateRAW)
            cityRAW = locations.get(str(location)+'c')
            cityFull = cityRAW.replace('_', ' ')
            locationStr =  cityRAW + '\n' + stateFull
            lcd.message(locationStr)
            blankScreen = False
            time.sleep(.2)
#       print selected location
        if lcd.buttonPressed(lcd.LEFT):
            location = (location -1)%locationCount
            lcd.clear()
            blankScreen = True
#       move left one location,-1, if at beginning, go to last location
        if lcd.buttonPressed(lcd.RIGHT):
            location = (location + 1)%locationCount
            lcd.clear()
            blankScreen = True
#       move right one location,+1, if at end, go to beginning location
        if lcd.buttonPressed(lcd.SELECT):
            lcd.clear()
            lcd.message('Location\nSelected')
            done = True
            blankScreen = True
            return location

        time.sleep(.1)

def wait(button):
    while not lcd.buttonPressed(button):
        time.sleep(.1)

init()      #Welcome Message
while True:

    if update:
        lcd.clear()
        lcd.message('Please Wait\nFetching Data')
        json = API.getLocation(locations.get(str(location)+'s'),locations.get(str(location)+'c'),token)
        update = False
        display = 0

    if display == 0:
        lcd.clear()
        high = API.high(json,units_Temp)
        low = API.low(json,units_Temp)
        windSpeed = API.windSpeed(json,units_Speed)
        windDir = API.winDir(json)
        string1 = API.Display1(high,low,windSpeed,units_Speed,windDir,language)
        lcd.message(string1)

    if display == 1:
        lcd.clear()
        rain = API.rain(json)
        humidity = API.humidity(json)
        string2 = API.Display2(rain,humidity,language)
        lcd.message(string2)

    if display == 2:
        lcd.clear()
        lcd.message('More Data\nComing Soon!')

    while True:
        if lcd.buttonPressed(lcd.DOWN):
            display = (display + 1)%displayCount
            break

        if lcd.buttonPressed(lcd.UP):
            display = (display -1)%displayCount
            break


        if lcd.buttonPressed(lcd.LEFT):
            location = locationChanger('left',locations,location)
            update = True
            break
#            Jump to location Menu Function

        if lcd.buttonPressed(lcd.RIGHT):
            location = locationChanger('right',locations,location)
            update = True
            break
#            Jump to location Menu Function
    if not update:
        wait = wait + .5
    else:
        wait = 0
    if wait > 5:
        update = True
    time.sleep(.25)

