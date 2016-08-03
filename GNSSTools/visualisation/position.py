# Tampere University of Technology
#
# DESCRIPTION
# Defines a function for extraction of the position
#
# AUTHOR
# Yannick DEFRANCE



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

def position(filename):
    # Extract latitude, longitude, altitude and time from NMEA file and return gpgga
    # gpgga = [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m]
    read = open(filename, 'r')
    gpgga = []
    a = 1
    b = 1
    for line in read.readlines():
        if line[0:6] == '$GPGGA':
            split = line.split(',')
            if (split[2] != '' or split[4] != ''):
                if split[3] == 'S':
                    a =-1
                if split[5] == 'W':
                    b = -1
                gpgga.append([split[1], a*dm_to_dd(float(split[2])/100),
                              b*dm_to_dd(float(split[4])/100), split[9]])
    read.close()
    return gpgga



