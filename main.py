__author__ = 'tobie'

import connection
import Spectracom
import config_parser
import data_processing
import time
import pyvisa
from threading import Thread
import ublox


res = connection.check_connection()
if res != 'devices connected':
    raise ValueError('devices not connected')
print(res)

# read the scenario

Date = '05-06-2016'
Hour = '15:01:00.0'
Start = 10
Duration = '00:00:07'
Interval = 10

inst = pyvisa.ResourceManager().open_resource('USB0::0x14EB::0x0060::200448::INSTR')
ublox.reset(ublox.init_ublox('COM4'), 'Cold RST')
ublox.enable(ublox.init_ublox('COM4'), 'UBX')
ublox.enable(ublox.init_ublox('COM4'), 'NMEA')
ublox.enable(ublox.init_ublox('COM4'), 'EPH')
scenario = config_parser.read_scen()

# Set scenario to Spectracom and launch it

Spectracom.clear()
Spectracom.reset()
Spectracom.set_init(Date, Hour, float(scenario[0][0]), float(scenario[0][1]), float(scenario[0][2]), Start, Duration, Interval)
Spectracom.launch()

# wait for the Spectracom to be really launch

time.sleep(80)

# read data comming from both the Spectracom and the Ublox at the same time while the scenario is running


class Acquire_data(Thread):
    def __init__(self, nb):
        Thread.__init__(self)
        self.nb = nb

    def run(self):
        if self.nb == 1:
            Spectracom.scenario_reading()
        if self.nb == 2:
            savefile = open('ublox_data.nmea', 'wb')
            while thread_1.is_alive() == True:
                ublox.read_data(ublox.init_ublox('COM4'), savefile)
                ublox.poll(ublox.init_ublox('COM4'), 'EPH')
                print('ici')
            savefile.close()


thread_1 = Acquire_data(1)
thread_2 = Acquire_data(2)

thread_1.start()
thread_2.start()

thread_1.join()
Spectracom.stop()



# computation of the root mean square error

#data_processing.computation()