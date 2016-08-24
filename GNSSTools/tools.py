# Tampere University of Technology
#
# DESCRIPTION
# Creates the matrix that contains the scenario's parameters,
# Defines function to compute heading
# Defines functions to synchronize lists, compute Root Mean Square Error 1D, 2D and 3D
#
# AUTHOR
# Anne-Marie Tobie

import math
import configparser


def get_sec(date):
    # Converts a date into sec
    # Input:
    # date: date in this format DD:HH:MM:SS
    # Return:
    # the value of the date in seconds
    d, h, m, s = [int(i) for i in date.split(':')]
    return d*3600*24 + h*3600 + m*60 + s


def dm_to_dd(position):
    # Converts degrees, minutes to decimal degrees
    # Input:
    # position: position given in DD.MMMM format
    # Return:
    # dd: position converts into decimal degrees
    deg = math.modf(position)[1]
    minu = ((position - deg)*100)
    dd = float(deg) + float(minu)/60
    return dd


def read_scen(filename):
    # Creates the matrix scenario from a test.ini file
    # Input:
    # filename: file test.ini
    # Return:
    # scenario: It's a matrix with nb_sections boxes, each of them contain nb_options boxes
    #           scenario = [[LAT, LONG, ALT, Duration, Heading, Speed, Acceleration, Rate heading,
    #           Turn rate, turn radius, C/N0, Propagation, antenna, tropospheric model, Ionospheric model,
    #           Keep altitude, signal type, ...][LAT, LONG, ...]]
    config = configparser.ConfigParser()
    config.read(filename)
    nb_sections = len(config.sections())
    nb_option = []
    for i in range(nb_sections):
        section = config.sections()[i]
        nb_option.append(len(config.options(section)))

    scenario = [[[] for _ in range(max(nb_option))] for _ in range(nb_sections)]
    for i in range(nb_sections):
        section = config.sections()[i]
        for j in range(nb_option[i]):
            option = config.options(section)
            scenario[i][j] = config.get(section, option[j])
    return scenario


def heading_compute(lat1, lat2, long1, long2):
    # Compute the heading that has to be followed
    # Input:
    # lat1: latitude of the departure position
    # lat2: latitude of the arrival position
    # long1: longitude of the departure position
    # long2: longitude of the arrival position
    # Return:
    # heading: heading to be followed from the departure position to reach the arrival one
    angle = abs(math.atan((long1-long2)/(lat1-lat2))*180/math.pi)
    if long2 >= long1:
        if lat2 >= lat1:
            heading = angle
        else:
            heading = 180 - angle
    else:
        if lat2 >= lat1:
            heading = 360 - angle
        else:
            heading = 180 + angle
    return heading


def synchronisation(list1, list2):
    # Compare the time input of each list and synchronise them
    # Input:
    # list1 and list2 have this shape:
    # [[time in HHMMSS.DD, LAT in DM, LONG in DM, ALT in m, N/S, E/W][...]]
    # Return:
    # 2 lists where list1[i][0] = list2[i][0]
    new_list1 = []
    new_list2 = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i][0][0:6] == list2[j][0][0:6]:
                new_list1.append(list1[i])
                new_list2.append(list2[j])
    return new_list1, new_list2


# RMS 1D error

def haversine(lat1, long1, lat2, long2):
    a = (math.sin(((lat2-lat1)*(math.pi/180))/2))**2 + math.cos(lat1) * math.cos(lat2) *\
                                                       (math.sin(((long2-long1)*(math.pi/180))/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = 6378137 * c
    return d

def rms_1d_alt(new_list1, new_list2):
    # Compute the root mean square error in altitude
    # Input:
    # 2 lists synchronised in time which have this shape
    # [[time in HHMMSS.DD, LAT in DM, LONG in DM, ALT in m, N/S, E/W][...]]
    # Return:
    # rms1dalt: RMS error on altitude data
    # alt_error: list of difference of altitude between lists at each time
    alt_error = []
    for i in range(len(new_list1)):
        altv = new_list1[i][3]
        altm = new_list2[i][3]
        alt_error.append(float(altm) - float(altv))
    rms1dalt = math.sqrt(sum([nb * nb for nb in alt_error])/len(new_list1))
    return rms1dalt, alt_error


def rms_1d_lat(new_list1, new_list2):
    # Compute the root mean square error in latitude
    # Input:
    # 2 lists synchronised in time which have this shape
    # [[time in HHMMSS.DD, LAT in DM, LONG in DM, ALT in m, N/S, E/W][...]]
    # Return:
    # rms1dlat: RMS error on latitude data
    # lat_error: list of difference of latitude between lists at each time
    lat_error = []
    for i in range(len(new_list1)):
        latv = new_list1[i][1]
        latm = new_list2[i][1]
        #lat_error.append(float(latm) - float(latv))
        lat_error.append(haversine(float(latm), 0, float(latv), 0))
    rms1dlat = math.sqrt(sum([nb * nb for nb in lat_error])/len(new_list1))
    return rms1dlat, lat_error


def rms_1d_long(new_list1, new_list2):
    # Compute the root mean square error in longitude
    # Input:
    # 2 lists synchronised in time which have this shape
    # [[time in HHMMSS.DD, LAT in DM, LONG in DM, ALT in m, N/S, E/W][...]]
    # Return:
    # rms1dlong: RMS error on longitude data
    # long_error: list of difference of longitude between lists at each time
    long_error = []
    for i in range(len(new_list1)):
        longv = new_list1[i][2]
        longm = new_list2[i][2]
        #long_error.append(float(longm) - float(longv))  # for DD computation
        long_error.append(haversine(0, float(longm), 0,float(longv)))  # for
    rms1dlong = math.sqrt(sum([nb * nb for nb in long_error])/len(new_list1))
    return rms1dlong, long_error


# RMS 2D error


def rms_2d(new_list1, new_list2):
    # argument for DD computation lat_error, long_error
    # Compute the root mean square 2D error (in latitude and longitude)
    # Input:
    # lat_error: list of difference of latitude between lists at each time
    # long_error: list of difference of longitude between lists at each time
    # Return:
    # rms2d: RMS 2D error

    # result in DD
    #lat = [nb * nb for nb in lat_error]
    #long = [nb * nb for nb in long_error]
    #latlong = []
    #for i in range(len(long)):
    #    latitude = lat[i]
    #    longitude = long[i]
    #    latlong.append(latitude+longitude)
    #rms2d = math.sqrt(sum(latlong)/len(lat_error))

    # result in meters
    latlong = []
    for i in range(len(new_list1)):
        latv = new_list1[i][1]
        latm = new_list2[i][1]
        longv = new_list1[i][2]
        longm = new_list2[i][2]
        latlong.append(haversine(float(latm), float(longm), float(latv), float(longv)))
    rms2d = math.sqrt(sum([nb * nb for nb in latlong])/len(new_list1))
    return rms2d


# RMS 3D error


def rms_3d(lat_error, long_error, alt_error):
    # Compute the root mean square 3D error (in latitude, longitude and altitude)
    # Input:
    #       alt_error: list of difference of altitude between lists at each time
    #       lat_error: list of difference of latitude between lists at each time
    #       long_error: list of difference of longitude between lists at each time
    # Return:
    #       rms3d: RMS 3D error
    alt = [nb * nb for nb in alt_error]
    lat = [nb * nb for nb in lat_error]
    long = [nb * nb for nb in long_error]
    altlatlong = []
    for i in range(len(lat)):
        altitude = alt[i]
        latitude = lat[i]
        longitude = long[i]
        altlatlong.append(altitude + latitude + longitude)
    rms3d = math.sqrt(sum(altlatlong)/len(lat_error))
    return rms3d


def data(filename):
    # take only the information GPGGA (global positionning system fix data)
    # Input:
    # file with nmea gga data
    # Return:
    # gpgga = [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m, N/S, E/W]
    read = open(filename, 'r')
    gpgga = []
    a = 1
    b = 1
    for line in read.readlines():
        if line[3:6] == 'GGA':
            split = line.split(',')
            if split[2] != '' or split[4] != '':
                if split[3] == 'S':
                    a = -1
                if split[5] == 'W':
                    b = -1
                gpgga.append([split[1], a*dm_to_dd(float(split[2])/100),
                              b*dm_to_dd(float(split[4])/100), split[9]])
    read.close()
    return gpgga


def computation(file1='datatxt/spectracom_data.nmea', file2='datatxt/ublox_processed_data.txt'):
    # Go through all RMS computation process (open file, data processing to get the proper shape,
    # synchronisation, RMS computations
    # Input:
    # file1 and file2 are file containing data including GGA data
    # Return:
    # rms1dalt: RMS error on altitude data
    # rms1dlat: RMS error on latitude data
    # rms1dlong: RMS error on longitude data
    # rms2d: RMS 2D error
    # rms3d: RMS 3D error
    # Raises:
    # ValueError: if data are not available!

    # Open files
    filename1 = open(file1, 'r')
    filename2 = open(file2, 'r')
    # data processing [time, Lat, Long, Alt]
    list1 = data(file1)
    list2 = data(file2)
    if list1 != [] and list2 != []:
        # time synchronisation
        new_list1 = synchronisation(list1, list2)[0]
        new_list2 = synchronisation(list1, list2)[1]
        # RMS 1D
        rms1dalt = rms_1d_alt(new_list1, new_list2)[0]
        rms1dlat = rms_1d_lat(new_list1, new_list2)[0]
        rms1dlong = rms_1d_long(new_list1, new_list2)[0]
        alt_error = rms_1d_alt(new_list1, new_list2)[1]
        lat_error = rms_1d_lat(new_list1, new_list2)[1]
        long_error = rms_1d_long(new_list1, new_list2)[1]
        # RMS 2D
        rms2d = rms_2d(new_list1, new_list2)  # result in meters
        # rms2d = rms_2d(lat_error, long_error)  # result in DD
        # RMS 3D
        rms3d = rms_3d(lat_error, long_error, alt_error)
        # close files
        filename1.close()
        filename2.close()
    else:
        raise ValueError('Not enough data available')
    return rms1dalt, rms1dlat, rms1dlong, rms2d, rms3d


def r4(message):
    # Decode IEEE 754 Single Precision message
    # Input: message to decode
    # Return: message decoded
    binary = '{0:032b}'.format(int(message, 16), 2)
    sign = int(binary[0], 2)
    exponent = int(binary[1:9], 2) - 127
    rawmantisse = binary[9:32]
    mantisse = 1
    for i in range(23):
        mantisse += int(rawmantisse[i], 2) * (2**-(i+1))
    value = pow(-1, sign) * mantisse * pow(2, exponent)
    return value


def r8(message):
    # Decode IEEE 754 Double Precision message
    # Input: message to decode
    # Return: message decoded
    binary = '{0:064b}'.format(int(message, 16), 2)
    sign = int(binary[0], 2)
    exponent = int(binary[1:12], 2) - 1023
    rawmantisse = binary[12:64]
    mantisse = 1
    for i in range(52):
        mantisse += int(rawmantisse[i], 2) * (2**-(i+1))
    value = pow(-1, sign) * mantisse * pow(2, exponent)
    return value
