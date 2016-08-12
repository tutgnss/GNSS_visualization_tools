# Tampere University of Technology
#
# DESCRIPTION
# Test Devices
#
# AUTHOR
# Anne-Marie Tobie

import unittest
from GNSSTools import Spectracom
from GNSSTools import tools
from GNSSTools import Ublox
from GNSSTools import Device


class TestDevices(unittest.TestCase, Ublox):

    def __init__(self, prodatafile='test/testfile.txt'):
        super(TestDevices, self).__init__()
        self.procdatafile = prodatafile

    def test_klobuchar_storage(self):
        received = self.klobuchar_data()
        expected = {0: {'utctow': 589824, 'kloa3': -1.1920928955078125e-07, 'kloa1': 2.2351741790771484e-08,
                        'utcdn': 7, 'kloa0': 8.381903171539307e-09, 'klob2': -65536.0, 'klob0': 92160.0,
                        'utcls': 17, 'utca0': -9.313225746154785e-10, 'utcwn': 1909, 'health': 'fd1ffff0',
                        'klob3': -589824.0, 'kloa2': -5.960464477539063e-08, 'utclsf': 18, 'klob1': 114688.0,
                        'utcwnf': 1929, 'utca1': -4.440892098500626e-15}}
        self.assertEqual(received, expected, 'Klobuchar Fails')

    def test_ephemeris_storage(self):
        received = self.ephemeris_data()
        expected = {0: {'cis': 7.078051567077637e-08, 'i0': 0.9704999357092461, 'ura': 2.0,
                        'tgd': -1.3504177331924438e-08, 'deltan': 4.5391176438980305e-09,
                        'flag': 'Curvefit interval of 4 hours', 'wn': 885, 'm0': -2.4799838019426295,
                        'iodesf3': 9, 'cuc': 2.3934990167617798e-06, 'health': 'Data ok',
                        'e': 0.008181710494682193, 'af2': 0.0, 'cic': -2.0489096641540527e-07,
                        'af1': -2.0463630789890885e-12, 'iodesf2': 9, 'omega0': -0.3692296566515383,
                        'svid': 31, 'omegadot': -8.025334287386005e-09, 'af0': 0.0002542673610150814,
                        'aodo': 0, 'cus': 5.8300793170928955e-06, 'toe': 302400, 'crc': 275.375,
                        'crs': 43.21875, 'tow': 196, 'iodc': 9, 'l2': 'P code ON', 'sqrta': 5153.797992706299,
                        'toc': 302400, 'idot': 9.786121916972699e-11, 'omega': -0.3926484062164583}}
        self.assertEqual(received, expected, 'Ephemeris Fails')

    def test_gga_storage(self):
        received = self.nmea_gga_store(self.procdatafile)
        expected = {"0": {"long": -2.279516666666667, "alt": "51.3", "time": "000439.000", "lat": 47.55203166666667}}
        self.assertEqual(received, expected, 'NMEA GGA Fails')

    def runTest(self):
        self.test_klobuchar_storage()
#        self.test_ephemeris_storage()
#        self.test_gga_storage()