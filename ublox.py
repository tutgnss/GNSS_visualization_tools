__author__ = 'tobie'

import tools, connection


def read_data(Duration):
    # read information of ublox and save them into a file
    ser = connection.connect_ublox()
    duree = tools.Tools.get_sec(Duration)
    savefile = open('ublox_data.nmea', 'wb')
    i=0
    while i<=duree:
        for j in range(7): # la valeur du range depend du nb de msg GPGSV a modifier! ici pour # msg GPGSV
            info = ser.readline()
            savefile.write(info)
        i=i+1
        print('ublox', i)
    savefile.close()

filename = 'ublox_data.nmea'

#done = tools.data(filename)
#print(done)

