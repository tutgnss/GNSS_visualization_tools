# Tampere University of Technology
#
# DESCRIPTION
# Test Devices
#
# AUTHOR
# Anne-Marie Tobie

import unittest
import serial
from GNSSTools import Spectracom
from GNSSTools import tools
from GNSSTools import Ublox
from GNSSTools import Device


class TestDevices(unittest.TestCase):

    def test_connection_receiver(self):
        device = serial.Serial('COM6')
        self.assertTrue(serial.Serial.isOpen(device))
