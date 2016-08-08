# Tampere University of Technology
#
# DESCRIPTION
# Parent class
#
# AUTHOR
# Anne-Marie Tobie

import GNSSTools.tools as tools
import urllib.request
import json


class Device:

    def __init__(self, datafile):
        self.datafile = datafile

    def open(self):
        pass

    def close(self):
        pass

    def fileopen(self):
        try:
            f = urllib.request.urlopen(self.datafile)
        except:
            try:
                f = open(self.datafile, 'r')
            except ValueError:
                print("Can't open this")
        return f

    def nmea_gga_store(self):
        # Read file and take only the information GGA (global positioning system fix data) data
        # Return:
        # gga: dictionnary of GGA data parsing this way:
        #   {
        #        "0": {
        #           "lat": LAT in DD,
        #           "long": LONG in DD,
        #           "alt": ALT in m,
        #           "time": time in HHMMSS.DD
        #       },
        #        "1": {...
        #       }
        #   }
        read = self.fileopen()
        gga = {}
        a = 1
        b = 1
        i = 0
        for line in read.readlines():
            if line[3:6] == 'GGA':
                split = line.split(',')
                if split[2] != '' or split[4] != '':
                    if split[3] == 'S':
                        a = -1
                    if split[5] == 'W':
                        b = -1
                    gga[i] = {'time': split[1], 'lat': a*tools.dm_to_dd(float(split[2])/100),
                              'long': b*tools.dm_to_dd(float(split[4])/100), 'alt': split[9]}
                i += 1
        read.close()
        return json.dumps(gga, indent=4)

    def nmea_rmc_store(self):
        # Read data collected and store into matrix RMC data
        # Return:
        # rmc: {
        #    "0": {
        #        "E/W": EW - character - East/West indicator,
        #        "Course Over Ground": course_over_ground - degrees - numeric - Course over ground,
        #        "time": time - hhmmss.ss - UTC time,
        #        "N/S": NS - character - North/South indicator,
        #        "long":  long - dddmm.mmmmm - Longitude (degrees & minutes),
        #        "lat": lat - ddmm.mmmmm - Latitude (degrees & minutes),
        #        "Speed Over Ground": speed_ovr_ground - knots - numeric - Speed over ground
        #    },
        #    "1": {...
        #    }
        #}
        file = self.fileopen()
        rmc = {}
        i = 0
        for line in file:
            if line[3:6] == 'RMC':
                data = line.split(',')
                if (data[3] and data[5]) != '':
                    time = data[1]
                    lat = tools.dm_to_dd(float(data[3])/100)
                    ns = data[4]
                    long = tools.dm_to_dd(float(data[5])/100)
                    ew = data[6]
                    speed_over_ground = data[7]
                    course_over_ground = data[8]
                    rmc[i] = {'time': time, 'lat': lat, 'N/S': ns, 'long': long, 'E/W': ew,
                              'Speed Over Ground': speed_over_ground,
                              'Course Over Ground': course_over_ground}
                    i += 1
        file.close()
        return json.dumps(rmc, indent=4)

    def nmea_gsv_store(self):
        # Read data collected and store into matrix GSV data
        # Return:
        # gsv: {
        # "0": {
        #        "0": {
        #            "Sat ID": numeric - Satellite ID,
        #            "azimuth": deg - numeric - Azimuth, (range 0-359),
        #            "C/N0":  cno - dBHz - numeric - Signal strength (C/N0, range 0-99), blank when not tracking,
        #            "elevation": deg - numeric - Elevation (range 0-90)
        #        },
        #        "1": {...
        #        }
        #   }
        # }
        file = self.fileopen()
        gsv = {}
        k = 0

        def collect(nsat):
            j = 0
            for i in range(nsat):
                sv = data[4 + 4*i]
                elev = data[5 + 4*i]
                az = data[6 + 4*i]
                if data[7 + 4*i][0:1] != '*':
                    cno = data[7 + 4*i][0:2]
                else:
                    cno = ''
                satif = {'Sat ID': sv, 'elevation': elev, 'azimuth': az, 'C/N0': cno}
                first[j + a] = satif
                j += 1
            return first

        for line in file:
            if line[3:6] == 'GSV' and len(line) > 17:
                data = line.split(',')
                if ((int(data[1]) > 1) and (data[1] != data[2])) or int(data[3]) % 4 == 0:
                    nsat = 4
                else:
                    nsat = int(data[3]) % 4
                if data[2] == '1':
                    a = 0
                    first = {}
                    collect(nsat)
                    if data[2] == data[1]:
                        gsv[k] = first
                        k += 1
                    a += 4
                elif data[2] != data[1]:
                    collect(nsat)
                    a += 4
                else:
                    collect(nsat)
                    gsv[k] = first
                    k += 1
        file.close()
        return json.dumps(gsv, indent=4)
