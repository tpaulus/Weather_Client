#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com
import lib.requests as requests

class WebAPI:
    def __init__(self):
        return
    def getLocation(self,state,city,token):
        d = requests.get('http://api.wunderground.com/api/'+ str(token) +'/forecast/q/'+ str(state) + '/'+ str(city) +'.json')
        json = d.json()
        return json

    def high(self,json,units):
        high = str(json['forecast']['simpleforecast']['forecastday'][0]['high'][units])
        return high

    def low(self,json,units):
        low = str(json ['forecast']['simpleforecast']['forecastday'][0]['low'][units])
        return low

    def windSpeed(self,json,units):
        windSpeed = str(json ['forecast']['simpleforecast']['forecastday'][0]['avewind'][units])
        return windSpeed

    def winDir(self,json):
        windDir = str(json ['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir'])
        return windDir

    def conditions(self,json):
        conditions = str(json ['forecast']['simpleforecast']['forecastday'][0]['conditions'])
        return conditions

    def rain(self,json):
        rain = str(json ['forecast']['txt_forecast']['forecastday'][0]['pop'])
        return rain

    def humidity(self,json):
        humidity = str(json ['forecast']['simpleforecast']['forecastday'][0]['avehumidity'])
        return humidity

    def Display1(self,high,low,windSpeed,units_Speed,windDir,lang):
        if lang == 'eng':
            string = 'Temp H:' + high + ' L:' + low + '\nWind ' + windSpeed + units_Speed + ' ' + windDir
            return string
        else:
            return 0
#       Not Yet Supported

    def Display2(self,rain,humidity,lang):
        if lang == 'eng':
            string = rain + '% Rain\n' + humidity + '% Humidity'
            return string
        else:
            return 0
#        Not Yet Supported

    def Display3(self,text):
#        Work in Progress!!
        return text

    def USCode(self,short):
        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }
        full = states.get(short)
        return full

