# Tampere University of Technology
#
# DESCRIPTION
# Computes 1D 2D and 3D RMS error
#
# AUTHOR
# Anne-Marie Tobie

import tools
import math


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
        lat_error.append(float(latm) - float(latv))
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
        long_error.append(float(longm) - float(longv))
    rms1dlong = math.sqrt(sum([nb * nb for nb in long_error])/len(new_list1))
    return rms1dlong, long_error


# RMS 2D error


def rms_2d(lat_error, long_error):
    # Compute the root mean square 2D error (in latitude and longitude)
    # Input:
    # lat_error: list of difference of latitude between lists at each time
    # long_error: list of difference of longitude between lists at each time
    # Return:
    # rms2d: RMS 2D error
    lat = [nb * nb for nb in lat_error]
    long = [nb * nb for nb in long_error]
    latlong = []
    for i in range(len(long)):
        latitude = lat[i]
        longitude = long[i]
        latlong.append(latitude+longitude)
    rms2d = math.sqrt(sum(latlong)/len(lat_error))
    return rms2d


# RMS 3D error


def rms_3d(lat_error, long_error, alt_error):
    # Compute the root mean square 3D error (in latitude, longitude and altitude)
    # Input:
    # alt_error: list of difference of altitude between lists at each time
    # lat_error: list of difference of latitude between lists at each time
    # long_error: list of difference of longitude between lists at each time
    # Return:
    # rms3d: RMS 3D error
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


def computation(file1='data/spectracom_data.nmea', file2='data/ublox_processed_data.txt'):
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
    list1 = tools.data(file1)
    list2 = tools.data(file2)
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
        rms2d = rms_2d(lat_error, long_error)
        # RMS 3D
        rms3d = rms_3d(lat_error, long_error, alt_error)
        # close files
        filename1.close()
        filename2.close()
    else:
        raise ValueError('Not enough data available')
    return rms1dalt, rms1dlat, rms1dlong, rms2d, rms3d
