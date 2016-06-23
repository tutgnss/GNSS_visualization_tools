__author__ = 'tobie'

import pyvisa
import serial

def connect_spectracom():
    # Make the connection with the spectracom and ask for the ID to make sure it has worked
    # argument of inst obtained with GSG StudioView with the command "connect"
    try:
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource ('USB0::0x14EB::0x0060::200448::INSTR')
        inst.query('*IDN?')
        return('connected')
    except:
        return('no connection available for Spectracom')
#print(connect_spectracom())

def connect_ublox():
    # Make the connection with the ublox and return its configuration
    # careful with the number of port it can be found in "device manager"
    try:
        receiver = serial.Serial('COM6', 9600)
        return (receiver)
    except:
        return ('no connection available for Ublox')
#print(connect_ublox())


## establish the connection with both of the devices
def check_connection():
    try:
        connect_spectracom()
        connect_ublox()
        if connect_ublox()!= 'no connection available for Ublox' and connect_spectracom()== 'connected':
            return('devices connected')
        else:
            return('one of the devices is not connected')
    except:
        return('fail to connect')
#print(check_connection())