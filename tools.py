__author__ = 'tobie'

import math

class Tools:
    def get_sec(self):
        #convert a date in DD:HH:MM into sec
        d, h, m = [int(i) for i in self.split(':')]
        return d*3600*24 + h*3600 + m*60

    def dm_to_dd(self):
        # convert degrees, minutes, seconds to decimal degrees
        deg = math.modf(self)[1]
        min = ((self - deg)*100)
        dd = float(deg) + float(min)/60
        return (dd)

def data(filename):
    # take only the information GPGGA (global positionning system fix data)
    # gpgga = [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m, N/S, E/W]
    read = open(filename, 'r')
    gpgga = []
    a=1
    b=1
    for line in read.readlines():
        if line[0:6] == '$GPGGA':
            split = line.split(',')
            if (split[2] != '' or split[4] != ''):
                if split[3] == 'S':
                    a =-1
                if split[5] == 'W':
                    b = -1
                gpgga.append([split[1], a*Tools.dm_to_dd(float(split[2])/100),
                              b*Tools.dm_to_dd(float(split[4])/100), split[9]])
    read.close()
    return gpgga

#print('spectracom : ', data('spectracom_data.nmea'))
#print('ublox : ', data('ublox_data.nmea'))