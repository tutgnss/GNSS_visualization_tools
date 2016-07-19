# Tampere University of Technology
#
# DESCRIPTION
# makes connexion and initialisation of devices then run the chosen scenario, stores data and make rms computation
#
# AUTHOR
# Anne-Marie Tobie

import Spectracom
import config_parser
import data_processing
import time
from threading import Thread
import ublox

class Acquire_data(Thread):
    def __init__(self, nb):
        Thread.__init__(self)
        self.nb = nb

    def run(self):
        if self.nb == 1:
            Spectracom.SpectracomScenario(spectracomcnx).scenario_reading()
        if self.nb == 2:
            ubloxfile = open('ublox_raw_data.txt', 'wb')
            while True:
                ublox.read_data(ubloxcnx, ubloxfile)
            ubloxfile.close()
        if self.nb == 3:
            while True:
                ublox.UbloxCommand(ubloxcnx, 'HUI').poll()
                ublox.UbloxCommand(ubloxcnx, 'EPH').poll()
                ublox.UbloxCommand(ubloxcnx, 'RAW').poll()
                time.sleep(10)

if __name__ == "__main__":
    # connexion
    ubloxcnx = ublox.UbloxInit(com='COM4', command=None).init_ublox()
    spectracomcnx = Spectracom.SpectracomInit('USB0::0x14EB::0x0060::200448::INSTR').connect_spectracom()

    # set ublox parameters
    ublox.UbloxInit(ubloxcnx, 'Cold RST')
    ublox.UbloxCommand(ubloxcnx, command='NMEA').disable()
    ublox.UbloxCommand(ubloxcnx, command='EPH').enable()
    ublox.UbloxCommand(ubloxcnx, command='HUI').enable()
    ublox.UbloxCommand(ubloxcnx, command='RAW').enable()

    # Read scenario
    scenario = config_parser.read_scen()

    # Launch spectracom
    Spectracom.SpectracomCommand(spectracomcnx).control(control='start')

    # wait for the Spectracom to be really launch
    time.sleep(60)

    # set spectracom initial parameters
    Spectracom.SpectracomCommand(spectracomcnx).set_datetime( date='01-01-2001', hour='15:01:00.0')
    Spectracom.SpectracomCommand(spectracomcnx).set_position(float(scenario[0][0]), float(scenario[0][1]), float(scenario[0][2]))

    # read data comming from both the Spectracom and the Ublox at the same time while the scenario is running
    thread_1 = Acquire_data(1)
    thread_2 = Acquire_data(2)
    thread_3 = Acquire_data(3)
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_1.join()

    Spectracom.SpectracomCommand(spectracomcnx).control(control='stop')
    ublox.UbloxStoreData().miseenforme()

    # computation of the root mean square error
    #data_processing.computation()


