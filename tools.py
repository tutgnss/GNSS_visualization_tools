# Tampere University of Technology
#
# DESCRIPTION
# Defines some randoms functions
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
    # the value of the date in secondes
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


def data(filename):
    # Read file and take only the information GGA (global positioning system fix data) data
    # Input:
    # filename: file containing NMEA data
    # Return:
    # gga: list of GGA data parsing this way:
    #      gga = [[time in HHMMSS.DD, LAT in DM, LONG in DM, ALT in m, N/S, E/W][...]]
    read = open(filename, 'r')
    gga = []
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
                gga.append([split[1], a*dm_to_dd(float(split[2])/100),
                            b*dm_to_dd(float(split[4])/100), split[9]])
    read.close()
    return gga


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
