# Tampere University of Technology
#
# DESCRIPTION
# Test Storage Data
#
# AUTHOR
# Anne-Marie Tobie

import unittest
from GNSSTools import Spectracom
from GNSSTools import tools
from GNSSTools import Ublox
from GNSSTools import Device



class TestDevices(unittest.TestCase):

    def test_klobuchar_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').klobuchar_data()
        expected = {0: {'utctow': 589824, 'kloa3': -1.1920928955078125e-07, 'kloa1': 2.2351741790771484e-08,
                        'utcdn': 7, 'kloa0': 8.381903171539307e-09, 'klob2': -65536.0, 'klob0': 92160.0,
                        'utcls': 17, 'utca0': -9.313225746154785e-10, 'utcwn': 1909, 'health': 'fd1ffff0',
                        'klob3': -589824.0, 'kloa2': -5.960464477539063e-08, 'utclsf': 18, 'klob1': 114688.0,
                        'utcwnf': 1929, 'utca1': -4.440892098500626e-15}}
        self.assertDictEqual(received, expected)

    def test_ephemeris_storage(self):
        self.maxDiff = None
        received = Ublox('COM6', procdatafile='testfile.txt').ephemeris_data()
        expected = {0: {'af2': 0.0, 'cuc': 2.3934990167617798e-06, 'iodesf3': 9, 'iodesf2': 9, 'deltan': 4.5391176438980305e-09,
                        'omega': -0.3926484062164583, 'i0': 0.9704999357092461, 'svid': 31, 'e': 0.008181710494682193,
                        'crc': 275.375, 'aodo': 0, 'cic': -2.0489096641540527e-07, 'af0': 0.0002542673610150814,
                        'tgd': -1.3504177331924438e-08, 'wn': 885, 'iodc': 9, 'crs': 43.21875, 'af1': -2.0463630789890885e-12,
                        'omega0': -0.3692296566515383, 'health': ('Some bad data', '000000'), 'toe': 302400,
                        'omegadot': -8.025334287386005e-09, 'toc': 302400, 'idot': 9.786121916972699e-11,
                        'sqrta': 5153.797992706299, 'm0': -2.4799838019426295, 'l2': 'P code ON', 'cus': 5.8300793170928955e-06,
                        'cis': 7.078051567077637e-08, 'ura': 2.0, 'flag': 'Curvefit interval greater than 4 hours'}}
        self.assertDictEqual(received, expected, 'Ephemeris Fails')

    def test_gga_storage(self):
        received = Device().nmea_gga_store(datafile='testfile.txt')
        expected = {0: {'alt': '51.3', 'long': -2.279516666666667, 'lat': 47.55203166666667, 'time': '000439.000'}}
        self.assertDictEqual(received, expected, 'NMEA GGA Fails')

    def test_gsv_storage(self):
        received = Device().nmea_gsv_store(datafile='testfile.txt')
        expected = {0: {0: {'C/N0': '39', 'Sat ID': '01', 'elevation': '24', 'azimuth': '314'},
                        1: {'C/N0': '', 'Sat ID': '09', 'elevation': '03', 'azimuth': '034'},
                        2: {'C/N0': '39', 'Sat ID': '11', 'elevation': '32', 'azimuth': '291'},
                        3: {'C/N0': '39', 'Sat ID': '14', 'elevation': '72', 'azimuth': '013'},
                        4: {'C/N0': '', 'Sat ID': '18', 'elevation': '17', 'azimuth': '110'},
                        5: {'C/N0': '39', 'Sat ID': '19', 'elevation': '11', 'azimuth': '248'},
                        6: {'C/N0': '39', 'Sat ID': '22', 'elevation': '59', 'azimuth': '097'},
                        7: {'C/N0': '39', 'Sat ID': '25', 'elevation': '', 'azimuth': ''},
                        8: {'C/N0': '39', 'Sat ID': '31', 'elevation': '40', 'azimuth': '181'},
                        9: {'C/N0': '39', 'Sat ID': '32', 'elevation': '23', 'azimuth': '300'}}}
        self.assertDictEqual(received, expected, 'NMEA GSV Fails')

    def test_rmc_storage(self):
        received = Device().nmea_rmc_store(datafile='testfile.txt')
        expected = {0: {'lat': 48.856548833333335, 'long': 2.3512306666666665,
                        'Speed Over Ground': '19.333', 'N/S': 'N', 'time': '000839.00',
                        'Course Over Ground': '269.14', 'E/W': 'E'}}
        self.assertDictEqual(received, expected, 'NMEA RMC Fails')

    def test_random_data_nav5_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').random_data()[0]
        expected = {0: {'pdop': 25.0, 'pacc': 100, 'cnothreshnumsv': 0, 'fixedalt': 0.0,
                        'fixedaltvar': 1.0, 'fixmode': 3, 'tdop': 25.0, 'Dynmodel': 0,
                        'cnothresh': 0, 'tacc': 300, 'minelev': 5, 'staticholdthresh': 0,
                        'dgpstimeout': 0}}
        self.assertDictEqual(received, expected, 'Random data NAV5 Fails')

    def test_random_data_navdop_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').random_data()[1]
        expected ={0: {'itow': 212594000, 'tdop': 2.52, 'pdop': 3.79, 'vdop': 2.43,
                       'edop': 0.99, 'hdop': 2.91, 'gdop': 4.55, 'ndop': 2.73}}
        self.assertDictEqual(received, expected, 'Random data DOP Fails')

    def test_random_data_rxmsvsi_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').random_data()[2]
        expected = {0: {'info': {0: {'svid': 1, 'elev': -61, 'age': 242, 'azim': 251},
                                 1: {'svid': 2, 'elev': -9, 'age': 82, 'azim': 54},
                                 2: {'svid': 3, 'elev': -56, 'age': 242, 'azim': 301},
                                 3: {'svid': 4, 'elev': 60, 'age': 63, 'azim': 210},
                                 4: {'svid': 5, 'elev': 29, 'age': 82, 'azim': 49},
                                 5: {'svid': 6, 'elev': -40, 'age': 242, 'azim': 43},
                                 6: {'svid': 7, 'elev': 3, 'age': 242, 'azim': 357},
                                 7: {'svid': 8, 'elev': -18, 'age': 242, 'azim': 281},
                                 8: {'svid': 9, 'elev': 3, 'age': 242, 'azim': 328},
                                 9: {'svid': 10, 'elev': -13, 'age': 242, 'azim': 184},
                                 10: {'svid': 11, 'elev': -49, 'age': 242, 'azim': 260},
                                 11: {'svid': 12, 'elev': -26, 'age': 82, 'azim': 141},
                                 12: {'svid': 13, 'elev': -2, 'age': 242, 'azim': 77},
                                 13: {'svid': 14, 'elev': -36, 'age': 242, 'azim': 220},
                                 14: {'svid': 15, 'elev': -7, 'age': 242, 'azim': 106},
                                 15: {'svid': 16, 'elev': 43, 'age': 242, 'azim': 297},
                                 16: {'svid': 17, 'elev': -79, 'age': 242, 'azim': 72},
                                 17: {'svid': 18, 'elev': 12, 'age': 50, 'azim': 164},
                                 18: {'svid': 19, 'elev': -62, 'age': 242, 'azim': 87},
                                 19: {'svid': 20, 'elev': 41, 'age': 50, 'azim': 114},
                                 20: {'svid': 21, 'elev': 65, 'age': 50, 'azim': 185},
                                 21: {'svid': 22, 'elev': -58, 'age': 242, 'azim': 272},
                                 22: {'svid': 23, 'elev': -7, 'age': 242, 'azim': 306},
                                 23: {'svid': 24, 'elev': -47, 'age': 242, 'azim': 126},
                                 24: {'svid': 25, 'elev': 1, 'age': 50, 'azim': 154},
                                 25: {'svid': 26, 'elev': 59, 'age': 242, 'azim': 253},
                                 26: {'svid': 27, 'elev': 12, 'age': 242, 'azim': 277},
                                 27: {'svid': 28, 'elev': -60, 'age': 242, 'azim': 352},
                                 28: {'svid': 29, 'elev': 39, 'age': 50, 'azim': 104},
                                 29: {'svid': 30, 'elev': -12, 'age': 242, 'azim': 13},
                                 30: {'svid': 31, 'elev': 8, 'age': 50, 'azim': 225},
                                 31: {'svid': 32, 'elev': -38, 'age': 242, 'azim': 197},
                                 32: {'svid': 120, 'elev': 13, 'age': 255, 'azim': 223},
                                 33: {'svid': 121, 'elev': -91, 'age': 255, 'azim': 0},
                                 34: {'svid': 122, 'elev': -35, 'age': 255, 'azim': 343},
                                 35: {'svid': 123, 'elev': -91, 'age': 255, 'azim': 0},
                                 36: {'svid': 124, 'elev': 20, 'age': 255, 'azim': 182},
                                 37: {'svid': 125, 'elev': -91, 'age': 255, 'azim': 0},
                                 38: {'svid': 126, 'elev': 20, 'age': 255, 'azim': 178},
                                 39: {'svid': 127, 'elev': 13, 'age': 255, 'azim': 136},
                                 40: {'svid': 128, 'elev': -91, 'age': 255, 'azim': 0},
                                 41: {'svid': 129, 'elev': -20, 'age': 255, 'azim': 66},
                                 42: {'svid': 130, 'elev': -91, 'age': 255, 'azim': 0},
                                 43: {'svid': 131, 'elev': 13, 'age': 255, 'azim': 136},
                                 44: {'svid': 132, 'elev': -91, 'age': 255, 'azim': 0},
                                 45: {'svid': 133, 'elev': -91, 'age': 255, 'azim': 0},
                                 46: {'svid': 134, 'elev': -33, 'age': 255, 'azim': 28},
                                 47: {'svid': 135, 'elev': -33, 'age': 255, 'azim': 334},
                                 48: {'svid': 136, 'elev': -91, 'age': 255, 'azim': 0},
                                 49: {'svid': 137, 'elev': -22, 'age': 255, 'azim': 62},
                                 50: {'svid': 138, 'elev': -26, 'age': 255, 'azim': 307},
                                 51: {'svid': 139, 'elev': -91, 'age': 255, 'azim': 0},
                                 52: {'svid': 140, 'elev': -91, 'age': 255, 'azim': 0},
                                 53: {'svid': 141, 'elev': -91, 'age': 255, 'azim': 0},
                                 54: {'svid': 142, 'elev': -91, 'age': 255, 'azim': 0},
                                 55: {'svid': 143, 'elev': -91, 'age': 255, 'azim': 0},
                                 56: {'svid': 144, 'elev': -91, 'age': 255, 'azim': 0},
                                 57: {'svid': 145, 'elev': -91, 'age': 255, 'azim': 0},
                                 58: {'svid': 146, 'elev': -91, 'age': 255, 'azim': 0},
                                 59: {'svid': 147, 'elev': -91, 'age': 255, 'azim': 0},
                                 60: {'svid': 148, 'elev': -91, 'age': 255, 'azim': 0},
                                 61: {'svid': 149, 'elev': -91, 'age': 255, 'azim': 0},
                                 62: {'svid': 150, 'elev': -91, 'age': 255, 'azim': 0},
                                 63: {'svid': 151, 'elev': -91, 'age': 255, 'azim': 0},
                                 64: {'svid': 152, 'elev': -91, 'age': 255, 'azim': 0},
                                 65: {'svid': 153, 'elev': -91, 'age': 255, 'azim': 0},
                                 66: {'svid': 154, 'elev': -91, 'age': 255, 'azim': 0},
                                 67: {'svid': 155, 'elev': -91, 'age': 255, 'azim': 0},
                                 68: {'svid': 156, 'elev': -91, 'age': 255, 'azim': 0},
                                 69: {'svid': 157, 'elev': -91, 'age': 255, 'azim': 0},
                                 70: {'svid': 158, 'elev': -91, 'age': 255, 'azim': 0}},
                        'numvis': 18, 'week': 1910, 'itow': 212680000, 'numsv': 71}}
        self.assertDictEqual(received, expected, 'Random data SVSI Fails')

    def test_gbs_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').nmea_data_gbs()
        expected = {0: {'SatIDfailed': '', 'Errlong': '8.4', 'Erralt': '11.6',
                        'time': '120333.00', 'Errlat': '13.8'}}
        self.assertDictEqual(received, expected, 'NMEA GBS Fails')

    def test_gsa_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').nmea_data_gsa()
        expected = {0: {'active sat': ['29', '26', '21', '20', '18', '10', '15', '16'],
                        'PDOP': '2.66', 'HDOP': '1.79', 'VDOP': '1.97'}}
        self.assertDictEqual(received, expected, 'NMEA GSA Fails')

    def test_vtg_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').nmea_data_vtg()
        expected = {0: {'speed in km per hour': '0.577', 'speed in knots': '0.312',
                        'course over ground': '124.05'}}
        self.assertDictEqual(received, expected, 'NMEA VTG Fails')

    def test_pubx03_storage(self):
        received = Ublox('COM6', procdatafile='testfile.txt').nmea_data_pubx3()
        expected = {0: {'nb of sat': 15, 'info': {
            0: {'C/N0': '', 'elevation': '31', 'SV ID': '4', 'SV status': 'e', 'azimuth': '190'},
            1: {'C/N0': '', 'elevation': '09', 'SV ID': '5', 'SV status': '-', 'azimuth': '033'},
            2: {'C/N0': '', 'elevation': '17', 'SV ID': '7', 'SV status': '-', 'azimuth': '336'},
            3: {'C/N0': '', 'elevation': '07', 'SV ID': '8', 'SV status': '-', 'azimuth': '290'},
            4: {'C/N0': '37', 'elevation': '13', 'SV ID': '10', 'SV status': 'U', 'azimuth': '180'},
            5: {'C/N0': '', 'elevation': '16', 'SV ID': '13', 'SV status': '-', 'azimuth': '056'},
            6: {'C/N0': '24', 'elevation': '14', 'SV ID': '15', 'SV status': 'U', 'azimuth': '088'},
            7: {'C/N0': '24', 'elevation': '56', 'SV ID': '16', 'SV status': 'U', 'azimuth': '254'},
            8: {'C/N0': '', 'elevation': '39', 'SV ID': '18', 'SV status': 'e', 'azimuth': '153'},
            9: {'C/N0': '17', 'elevation': '44', 'SV ID': '20', 'SV status': 'U', 'azimuth': '074'},
            10: {'C/N0': '23', 'elevation': '70', 'SV ID': '21', 'SV status': 'U', 'azimuth': '108'},
            11: {'C/N0': '36', 'elevation': '43', 'SV ID': '26', 'SV status': 'U', 'azimuth': '210'},
            12: {'C/N0': '', 'elevation': '40', 'SV ID': '27', 'SV status': '-', 'azimuth': '283'},
            13: {'C/N0': '38', 'elevation': '11', 'SV ID': '29', 'SV status': 'U', 'azimuth': '114'},
            14: {'C/N0': '', 'elevation': '07', 'SV ID': '30', 'SV status': '-', 'azimuth': '359'}}}}
        self.assertDictEqual(received, expected, 'NMEA PUBX 03 Fails')