__author__ = 'tobie'

import tools, math
from matplotlib import pyplot as plt

# Open files we need
spec =open('spectracom_data.txt', 'r')
ublox = open('ublox_data.txt', 'r')

# take back information we need ie [time, Lat, Long, Alt]
speclist = tools.data('spectracom_data.txt')
ubloxlist = tools.data('ublox_data.txt')
print(speclist)
print(ubloxlist)

def synchronisation(speclist, ubloxlist):
    # to compare information sent and received, they must be synchronized
    new_spec =[]
    new_ublox = []
    for i in range(len(speclist)):
        for j in range(len(ubloxlist)):
            if speclist[i][0][0:6] == ubloxlist[j][0][0:6]:
                new_spec.append(speclist[i])
                new_ublox.append(ubloxlist[j])
    return (new_spec, new_ublox)

new_spec = synchronisation(speclist, ubloxlist)[0]
new_ublox = synchronisation(speclist, ubloxlist)[1]
print(new_spec)
print(new_ublox)

## RMS 1D error

def RMS_1D_alt(new_spec, new_ublox):
    # altitude error
    alt_error = []
    for i in range(len(new_spec)):
        altv = new_spec[i][3]
        altm = new_ublox[i][3]
        alt_error.append(float(altm) - float(altv))
    return ('the altitude error is : %.15f meters' % math.sqrt(sum([nb * nb for nb in alt_error])/len(new_spec)), alt_error)

def RMS_1D_lat(new_spec, new_ublox):
    # latitude error
    lat_error = []
    for i in range(len(new_spec)):
        latv = new_spec[i][1]
        latm = new_ublox[i][1]
        lat_error.append(float(latm) - float(latv))
    return('the latitude error is : %.15f decimal degrees' % math.sqrt(sum([nb * nb for nb in lat_error])/len(new_spec)), lat_error)

def RMS_1D_long(new_spec, new_ublox):
    # longitude error
    long_error = []
    for i in range(len(new_spec)):
        longv = new_spec[i][2]
        longm = new_ublox[i][2]
        long_error.append(float(longm) - float(longv))
    return (('the longitude error is : %.15f decimal degrees' % math.sqrt(sum([nb * nb for nb in long_error])/len(new_spec))), long_error)

print(RMS_1D_alt(new_spec, new_ublox)[0])
print(RMS_1D_lat(new_spec, new_ublox)[0])
print(RMS_1D_long(new_spec, new_ublox)[0])

alt_error = RMS_1D_alt(new_spec, new_ublox)[1]
lat_error = RMS_1D_lat(new_spec, new_ublox)[1]
long_error = RMS_1D_long(new_spec, new_ublox)[1]
## RMS 2D error
def RMS_2D(lat_error, long_error, new_spec):
    # Compute the 2D error
    lat = [nb * nb for nb in lat_error]
    long = [nb * nb for nb in long_error]
    latlong = []
    for i in range(len(long)):
        latitude = lat[i]
        longitude = long[i]
        latlong.append(latitude+longitude)
    return('the 2D error is : %.15f decimal degrees' % math.sqrt(sum(latlong)/len(new_spec)))

print(RMS_2D(lat_error, long_error, new_spec))

## RMS 3D error
def RMS_3D(lat_error, long_error, alt_error, new_spec):
    # Compute the 3D error
    alt = [nb * nb for nb in alt_error]
    lat = [nb * nb for nb in lat_error]
    long = [nb * nb for nb in long_error]
    altlatlong = []
    for i in range(len(lat)):
        altitude = alt[i]
        latitude = lat[i]
        longitude = long[i]
        altlatlong.append(altitude + latitude + longitude)
    return ('the 3D error is : %.15f decimal degrees' % math.sqrt(sum(altlatlong)/len(new_spec)) )

print(RMS_3D(lat_error, long_error, alt_error, new_spec))


def precision(new_spec,new_ublox):

    plt.ion()

    for i in range(min(len(new_spec),len(new_ublox))):
        x = new_spec[i][2]
        y = new_spec[i][1]
        plt.scatter(x, y, color="black")
        z = new_ublox[i][2]
        t = new_ublox[i][1]
        plt.scatter(z, t, color="red")
   #     plt.pause(0.2)
    plt.ioff()
    plt.show()
    return

precision(new_spec, new_ublox)

spec.close()
ublox.close()
