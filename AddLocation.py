#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com
import os

app_info_folder = '/etc/WeatherUnderground'
data = app_info_folder + '/locations.conf'

try:
    print 'Welcome to the Add Location Tool'
    if raw_input("To continue enter 'y'\n") == 'y':
        info = open(data)
        State = raw_input('Enter The name of the State your desired location is in, using the abbreviation -CA\n')
        City = raw_input('Now, Enter the name of the City\n')
        print '\nThank You!'
        State = State.replace('\n', '').upper()
        City = City.replace('\n', '').replace(' ','_')
        if raw_input("Is this Information Correct? Type 'y'\n") == 'y':
            if not os.path.exists(app_info_folder):
                os.makedirs(app_info_folder)
            info = open(data, 'a')
            info.write(',' + State + ':' + City)
            info.close()

        else:
            info.close()
            quit('No Locations Added')

    else:
        quit('No Locations Added')


except IOError:
    quit('Unable to Access Locations, run Main app First!')