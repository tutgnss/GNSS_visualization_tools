# Tampere University of Technology
#
# DESCRIPTION
# Read data from ublox
#
# AUTHOR
# Anne-Marie Tobie

import tools
#import connection
import serial
import time


def init_ublox(com):
    # sets initial values into the device
    baud_rate = 9600
    data_bits = 8
    parity = 'N'
    stop_bit = 1
    timeout = 1
    device = serial.Serial(com, timeout=timeout, stopbits=stop_bit, write_timeout=None,
                           bytesize=data_bits, rtscts=False, xonxoff=False, parity=parity,
                           baudrate=baud_rate, inter_byte_timeout=None, dsrdtr=False)
    return device


def reset(device, command):
    # Permits to make a cold, warm or a hot start reset
    if command == 'Cold RST':
        reset = b'\xB5\x62\x06\x04\x04\x00\xFF\xA1\x02\x00\xB0\x47'
        device.write(reset)
        find_message(device)
    if command == 'Warm RST':
        reset = b'\xB5\x62\x06\x04\x04\x00\x01\x00\x02\x00\x11\x6C'
        device.write(reset)
        find_message(device)
    if command == 'Hot RST':
        reset = b'\xB5\x62\x06\x04\x04\x00\x00\x00\x02\x00\x10\x68'
        device.write(reset)
        find_message(device)


def enable(device, command):
    # set ephemerides, ionosphere and pseudo range message available
    if command == 'EPH':
        eph_on = b'\xB5\x62\x06\x01\x02\x00\x0B\x31\x45\x78'
        device.write(eph_on)
        find_message(device)
    if command == 'HUI':
        hui_on = b'\xB5\x62\x06\x01\x02\x00\x0B\x02\x16\x49'
        device.write(hui_on)
        find_message(device)
    if command == 'RAW':
        raw_on = b'\xB5\x62\x06\x01\x02\x00\x02\x10\x1B\x45'
        device.write(raw_on)
        find_message(device)


def get(device, command):
    # read ephemerides and ionosphere message
    if command == 'EPH':
        eph_get = b'\xB5\x62\x0B\x31\x00\x00\x3C\xBF'
        device.write(eph_get)
        find_message(device)
    if command == 'HUI':
        hui_get = b'\xB5\x62\x0B\x02\x00\x00\x0D\x32'
        device.write(hui_get)
        find_message(device)
    if command == 'HUI':
        raw_get = b'\xB5\x62\x02\x10\x00\x00\x12\x38'
        device.write(raw_get)
        find_message(device)


def find_message(device):
    #
    msgsent = time.time()
    wait = 1
    while time.time() < wait + msgsent:
        line = device.readline()
        print(line)
        if line[0:4] == b'\xb5b\x05\x01':
            print('ack received')
        elif line[0:4] == b'\xb5b\x05\x00':
            print('nak received')
        else:
            print('JE FAIS CE QUE JE VEUX')

reset(init_ublox('COM4'), 'Warm RST')
enable(init_ublox('COM4'), 'EPH')
get(init_ublox('COM4'), 'EPH')


def read_data(device, savefile):
    for j in range(7):  # la valeur du range depend du nb de msg GPGSV a modifier! ici pour # msg GPGSV
        info = device.readline()
        savefile.write(info)
# def read_data(duration):
# read information of ublox and save them into a file
#    ser = connection.connect_ublox()
#    duree = tools.Tools.get_sec(duration)
#    savefile = open('ublox_data.nmea', 'wb')
#    i = 0
#    while i <= duree:
#        for j in range(7):  # la valeur du range depend du nb de msg GPGSV a modifier! ici pour # msg GPGSV
#            info = ser.readline()
#            savefile.write(info)
#        i += 1
#        print('ublox', i)
#    savefile.close()

# filename = 'ublox_data.nmea'

# done = tools.data('ublox_data.nmea')
# print(done)
