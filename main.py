# Tampere University of Technology
#
# DESCRIPTION
# makes connexion and initialisation of devices then run the chosen scenario,
# stores data and make rms computation
#
# AUTHOR
# Anne-Marie Tobie

from Spectracom import Spectracom
import config_parser
import data_processing
import time
from threading import Thread
from ublox import Ublox


class AcquireData(Thread):
    def __init__(self, nb):
        Thread.__init__(self)
        self.nb = nb

    def run(self):
        if self.nb == 1:
            spectracomcnx.scenario_reading(scenario)
        if self.nb == 2:
            begin = time.time()
            ubloxfile = open('data/ublox_raw_data.txt', 'wb')
            while (time.time() < 300 + begin) or (thread_1.is_alive() is True):
                ubloxcnx.read_data(ubloxfile)
            ubloxfile.close()
        if self.nb == 3:
            while thread_1.is_alive() is True:
                ubloxcnx.poll('HUI')
                ubloxcnx.poll('EPH')
                ubloxcnx.poll('RAW')
                time.sleep(10)


if __name__ == "__main__":
    # connexion
    ubloxcnx = Ublox(com='COM6')
    spectracomcnx = Spectracom('USB0::0x14EB::0x0060::200448::INSTR')

    # Read scenario
    scenario = config_parser.read_scen('test/test_6.ini')

    # Launch spectracom
    spectracomcnx.control(control='start')

    # wait for the Spectracom to be really launch
    time.sleep(50)

    # set spectracom initial parameters
    spectracomcnx.set_observation()
    spectracomcnx.set_datetime(date='01-01-2001', hour='15:01:00.0')
    spectracomcnx.set_power(-130)
    spectracomcnx.set_position(float(scenario[0][0]), float(scenario[0][1]), float(scenario[0][2]))

    # set ublox parameters
    ubloxcnx.reset(command='Cold RST')
    ubloxcnx.enable(command='NMEA')
    ubloxcnx.enable(command='UBX')

    thread_1 = AcquireData(1)
    thread_2 = AcquireData(2)
    thread_2.start()

    time.sleep(270)

    # read data comming from both the Spectracom and the Ublox at the same time while the scenario is running
    thread_3 = AcquireData(3)
    thread_1.start()
    thread_3.start()
    thread_1.join()

    spectracomcnx.control(control='stop')
    Ublox.miseenforme()

    # computation of the root mean square error
    data_processing.computation()
