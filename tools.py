__author__ = 'tobie'

import math

class Tools:
    def get_sec(self):
        #convert a date in DD:HH:MM into sec
        d, h, m = [int(i) for i in self.split(':')]
        return d*3600*24 + h*3600 + m*60

    def dms_to_dd(self):
        # convert degrees, minutes, seconds to decimal degrees
        deg = math.modf(self)[1]
        min = math.modf((self - deg)*100)[1]
        sec = math.modf(self*100)[0]
        dd = float(deg) + float(min)/60 + float(sec)/3600
        return (dd)


def data(filename):
    # take only the information GPGGA (global positionning system fix data)
    # gpgga = [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m]
    read = open(filename, 'r')
    gpgga = []
    for line in read.readlines():
        if line[0:6] == '$GPGGA':
            split = line.split(',')
            if (split[2] != '' or split[4] != ''):
                gpgga.append([split[1], Tools.dms_to_dd(float(split[2])/100),
                              Tools.dms_to_dd(float(split[4])/100), split[9]])
    read.close()
    return gpgga

#print('spectracom : ', data('spectracom_data.txt'))
#print('ublox : ', data('ublox_data.txt'))