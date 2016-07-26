# Tampere University of Technology
#
# DESCRIPTION
# Configuration of ublox: enabling or disabling messages output
# Read data from ublox and store them into matrix
#
# AUTHOR
# Anne-Marie Tobie

import serial
import time
import binascii
import math


class Ublox:
    # this class makes the connexion with the ublox device
    def __init__(self, com, baud_rate=4800, data_bits=8, parity='N', stop_bit=1, timeout=1):
        self.com = com
        self.baud_rate = baud_rate
        self.data_bits = data_bits
        self.parity = parity
        self.stop_bit = stop_bit
        self.timeout = timeout
        try:
            self.device = serial.Serial(self.com, timeout=timeout, stopbits=stop_bit, write_timeout=None,
                                        bytesize=data_bits, rtscts=False, xonxoff=False, parity=parity,
                                        baudrate=baud_rate, inter_byte_timeout=None, dsrdtr=False)
        except:
            raise ValueError('connexion with Ublox device failed')

    def find_message(self):
        msgsent = time.time()
        wait = 1
        while time.time() < wait + msgsent:
            line = self.device.readline()
            if line[0:4] == b'\xb5b\x05\x01':
                print('ack received')
            elif line[0:4] == b'\xb5b\x05\x00':
                print('nak received')

    def reset(self, command):
        # Permits to make a cold, warm or a hot start reset
        if command == 'Cold RST':
            reset = b'\xB5\x62\x06\x04\x04\x00\xFF\xA1\x02\x00\xB0\x47'
            self.device.write(reset)
            self.find_message()

        elif command == 'Warm RST':
            reset = b'\xB5\x62\x06\x04\x04\x00\x01\x00\x02\x00\x11\x6C'
            self.device.write(reset)
            self.find_message()

        elif command == 'Hot RST':
            reset = b'\xB5\x62\x06\x04\x04\x00\x00\x00\x02\x00\x10\x68'
            self.device.write(reset)
            self.find_message()

        else:
            raise ValueError('Unknown resetting command')

    def enable(self, command):
        # set ephemerides, ionosphere and pseudo range message available
        # ste all ubx, nmea messages enable
        if command == 'EPH':
            eph_on = b'\xB5\x62\x06\x01\x03\x00\x0B\x31\x01\x47\xC3'
            self.device.write(eph_on)
            self.find_message()

        elif command == 'HUI':
            hui_on = b'\xB5\x62\x06\x01\x03\x00\x0B\x02\x01\x18\x65 '
            self.device.write(hui_on)
            self.find_message()

        elif command == 'RAW':
            raw_on = b'\xB5\x62\x06\x01\x03\x00\x02\x10\x01\x1D\x66'
            self.device.write(raw_on)
            self.find_message()

        elif command == 'GGA':
            gga = b'\xB5\x62\x06\x01\x03\x00\xF0\x00\x01\xFB\x10'
            self.device.write(gga)
            self.find_message()

        elif command == 'NMEA':  # receive an ack when test
            # DTM   GBS    GGA    GLL    GRS    GSA    GST    GSV    RMC
            # VTG   ZDA    PUBX 00     PUBX 03    PUBX 04
            nmea_on = b'\xB5\x62\x06\x01\x03\x00\xF0\x0A\x01\x05\x24'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x09\x01\x04\x22'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x00\x01\xFB\x10'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x01\x01\xFC\x12'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x06\x01\x01\x1C'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x02\x01\xFD\x14'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x07\x01\x02\x1E'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x03\x01\xFE\x16'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x04\x01\xFF\x18'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x05\x01\x00\x1A'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x08\x01\x03\x20'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x00\x01\xFC\x13'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x03\x01\xFF\x19'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x04\x01\x00\x1B'
            self.device.write(nmea_on)
            self.find_message()
        elif command == 'UBX':
            ubx_on = b'\xB5\x62\x06\x01\x03\x00\x0B\x30\x01\x46\xC1'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x50\x01\x66\x01'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x33\x01\x49\xC7'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x31\x01\x47\xC3'\
                     b'\xB5\x62\x06\x01\x03\x00\x10\x02\x01\x1D\x74'\
                     b'\xB5\x62\x06\x01\x03\x00\x10\x10\x01\x2B\x90'\
                     b'\xB5\x62\x06\x01\x03\x00\x28\x00\x01\x33\xB8'\
                     b'\xB5\x62\x06\x01\x03\x00\x21\x0E\x01\x3A\xBF'\
                     b'\xB5\x62\x06\x01\x03\x00\x21\x08\x01\x34\xB3'\
                     b'\xB5\x62\x06\x01\x03\x00\x21\x0B\x01\x37\xB9'\
                     b'\xB5\x62\x06\x01\x03\x00\x21\x0F\x01\x3B\xC1'\
                     b'\xB5\x62\x06\x01\x03\x00\x21\x0D\x01\x39\xBD'\
                     b'\xB5\x62\x06\x01\x03\x00\x13\x80\x01\x9E\x79'\
                     b'\xB5\x62\x06\x01\x03\x00\x13\x21\x01\x3F\xBB'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x05\x01\x1A\x68'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x09\x01\x1E\x70'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x0B\x01\x20\x74'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x02\x01\x17\x62'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x06\x01\x1B\x6A'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x07\x01\x1C\x6C'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x21\x01\x36\xA0'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x2E\x01\x43\xBA'\
                     b'\xB5\x62\x06\x01\x03\x00\x0A\x08\x01\x1D\x6E'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x60\x01\x6C\x03'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x22\x01\x2E\x87'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x31\x01\x3D\xA5'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x04\x01\x10\x4B'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x40\x01\x4C\xC3'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x01\x01\x0D\x45'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x02\x01\x0E\x47'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x32\x01\x3E\xA7'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x06\x01\x12\x4F'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x03\x01\x0F\x49'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x30\x01\x3C\xA3'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x20\x01\x2C\x83'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x21\x01\x2D\x85'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x11\x01\x1D\x65'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x12\x01\x1E\x67'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x30\x01\x3D\xA6'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x31\x01\x3E\xA8'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x10\x01\x1D\x66'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x13\x01\x20\x6C'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x20\x01\x2D\x86'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x04\x01\x1C\x6F'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x03\x01\x1B\x6D'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x01\x01\x19\x69'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x06\x01\x1E\x73'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x32\x01\x48\xC5'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x02\x01\x18\x65'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x01\x01\x17\x63'\
                     b'\xB5\x62\x06\x01\x03\x00\x0B\x00\x01\x16\x61'\
                     b'\xB5\x62\x06\x01\x03\x00\x10\x15\x01\x30\x9A'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x05\x01\x11\x4D'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x3A\x01\x46\xB7'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x61\x01\x6D\x05'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x39\x01\x45\xB5'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x09\x01\x15\x55'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x34\x01\x40\xAB'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x07\x01\x13\x51'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x3C\x01\x48\xBB'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x35\x01\x41\xAD'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x3B\x01\x47\xB9'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x24\x01\x30\x8B'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x25\x01\x31\x8D'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x23\x01\x2F\x89'\
                     b'\xB5\x62\x06\x01\x03\x00\x01\x26\x01\x32\x8F'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x61\x01\x6E\x08'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x14\x01\x21\x6E'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x15\x01\x22\x70'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x59\x01\x66\xF8'\
                     b'\xB5\x62\x06\x01\x03\x00\x02\x11\x01\x1E\x68'\
                     b'\xB5\x62\x06\x01\x03\x00\x27\x01\x01\x33\xB7'\
                     b'\xB5\x62\x06\x01\x03\x00\x27\x03\x01\x35\xBB'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x11\x01\x29\x89'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x16\x01\x2E\x93'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x13\x01\x2B\x8D'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x12\x01\x2A\x8B'\
                     b'\xB5\x62\x06\x01\x03\x00\x0D\x15\x01\x2D\x91'\
                     b'\xB5\x62\x06\x01\x03\x00\x09\x14\x01\x28\x83'
            self.device.write(ubx_on)
            self.find_message()
        else:
            raise ValueError('Unknown Enabling Command')

    def poll(self, command):
        # poll messages
        if command == 'EPH':
            eph_get = b'\xB5\x62\x0B\x31\x00\x00\x3C\xBF'
            self.device.write(eph_get)

        elif command == 'HUI':
            hui_get = b'\xB5\x62\x0B\x02\x00\x00\x0D\x32'
            self.device.write(hui_get)

        elif command == 'RAW':
            raw_get = b'\xB5\x62\x02\x10\x00\x00\x12\x38'
            self.device.write(raw_get)

        elif command == 'random':
            # CFG-NAV5  NAV-DOP  RXM-SVSI
            random_get = b'\xB5\x62\x06\x24\x00\x00\x2A\x84'\
                         b'\xB5\x62\x01\x04\x00\x00\x05\x10'\
                         b'\xB5\x62\x02\x20\x00\x00\x22\x68'
            self.device.write(random_get)

        else:
            raise ValueError('Unknown Polling Command')

    def disable(self, command):
        # disable UBX or NMEA message
        if command == 'UBX':  # Receive a Nac when test -- pb : UBX msg turn off by default
            disable = b'\xB5\x62\x06\x01\x03\x00\x0B\x30\x01\x45\xC0'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x50\x00\x65\x00'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x33\x00\x48\xC6'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x31\x00\x46\xC2'\
                      b'\xB5\x62\x06\x01\x03\x00\x10\x02\x00\x1C\x73'\
                      b'\xB5\x62\x06\x01\x03\x00\x10\x10\x00\x2A\x8F'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x05\x00\x19\x67'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x09\x00\x1D\x6F'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x0B\x00\x1F\x73'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x02\x00\x16\x61'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x06\x00\x1A\x69'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x07\x00\x1B\x6B'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x21\x00\x35\x9F'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x08\x00\x1C\x6D'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x60\x00\x6B\x02'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x22\x00\x2D\x86'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x31\x00\x3C\xA4'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x04\x00\x0F\x4A'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x40\x00\x4B\xC2'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x01\x00\x0C\x44'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x02\x00\x0D\x46'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x32\x00\x3D\xA6'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x06\x00\x11\x4E'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x03\x00\x0E\x48'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x30\x00\x3B\xA2'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x20\x00\x2B\x82'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x21\x00\x2C\x84'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x11\x00\x1C\x64'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x12\x00\x1D\x66'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x30\x00\x3C\xA5'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x31\x00\x3D\xA7'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x10\x00\x1C\x65'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x11\x00\x1D\x67'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x13\x00\x1F\x6B'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x20\x00\x2C\x85'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x04\x00\x1B\x6E'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x03\x00\x1A\x6C'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x01\x00\x18\x68'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x06\x00\x1D\x72'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x32\x00\x47\xC4'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x02\x00\x17\x64'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x01\x00\x16\x62'\
                      b'\xB5\x62\x06\x01\x03\x00\x0B\x00\x00\x15\x60'\
                      b'\xB5\x62\x06\x01\x03\x00\x10\x15\x00\x2F\x99'\
                      b'\xB5\x62\x06\x01\x03\x00\x28\x00\x00\x32\xB7'\
                      b'\xB5\x62\x06\x01\x03\x00\x21\x0E\x00\x39\xBE'\
                      b'\xB5\x62\x06\x01\x03\x00\x21\x08\x00\x33\xB2'\
                      b'\xB5\x62\x06\x01\x03\x00\x21\x0B\x00\x36\xB8'\
                      b'\xB5\x62\x06\x01\x03\x00\x21\x0F\x00\x3A\xC0'\
                      b'\xB5\x62\x06\x01\x03\x00\x21\x0D\x00\x38\xBC'\
                      b'\xB5\x62\x06\x01\x03\x00\x13\x80\x00\x9D\x78'\
                      b'\xB5\x62\x06\x01\x03\x00\x13\x21\x00\x3E\xBA'\
                      b'\xB5\x62\x06\x01\x03\x00\x0A\x2E\x00\x42\xB9'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x05\x00\x10\x4C'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x3A\x00\x45\xB6'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x61\x00\x6C\x04'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x39\x00\x44\xB4'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x09\x00\x14\x54'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x34\x00\x3F\xAA'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x07\x00\x12\x50'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x3C\x00\x47\xBA'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x35\x00\x40\xAC'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x3B\x00\x46\xB8'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x24\x00\x2F\x8A'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x25\x00\x30\x8C'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x23\x00\x2E\x88'\
                      b'\xB5\x62\x06\x01\x03\x00\x01\x26\x00\x31\x8E'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x61\x00\x6D\x07'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x14\x00\x20\x6D'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x15\x00\x21\x6F'\
                      b'\xB5\x62\x06\x01\x03\x00\x02\x59\x00\x65\xF7'\
                      b'\xB5\x62\x06\x01\x03\x00\x27\x01\x00\x32\xB6'\
                      b'\xB5\x62\x06\x01\x03\x00\x27\x03\x00\x34\xBA'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x11\x00\x28\x88'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x16\x00\x2D\x92'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x13\x00\x2A\x8C'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x12\x00\x29\x8A'\
                      b'\xB5\x62\x06\x01\x03\x00\x0D\x15\x00\x2C\x90'\
                      b'\xB5\x62\x06\x01\x03\x00\x09\x14\x00\x27\x82'
            self.device.write(disable)
            self.find_message()

        elif command == 'NMEA':
            # DTM   GBS    GGA    GLL    GRS    GSA    GST    GSV    RMC
            # VTG   ZDA    PUBX 00     PUBX 03    PUBX 04
            disable = b'\xB5\x62\x06\x01\x03\x00\xF0\x0A\x00\x04\x23'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x09\x00\x03\x21'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x00\x00\xFA\x0F'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x01\x00\xFB\x11'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x06\x00\x00\x1B'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x02\x00\xFC\x13'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x07\x00\x01\x1D'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x03\x00\xFD\x15'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x04\x00\xFE\x17'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x05\x00\xFF\x19'\
                      b'\xB5\x62\x06\x01\x03\x00\xF0\x08\x00\x02\x1F'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x00\x00\xFB\x12'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x03\x00\xFE\x18'\
                      b'\xB5\x62\x06\x01\x03\x00\xF1\x04\x00\xFF\x1A'
            self.device.write(disable)
            self.find_message()

        else:
            raise ValueError('Unknown Disabling Command')

    @staticmethod
    def miseenforme():
        data = open('ublox_raw_data.txt', 'r')
        thing = data.read()
        data.close()

        first = thing.replace('b562', '\nb562')
        second = first.replace('2447', '\n2447')
        third = second.replace('0d0a$G', '\n$G')

        data = open('ublox_processed_data.txt', 'w')
        data.write(third)
        data.close()

    @staticmethod
    def klobuchar_data():
        # creates the matrix of ephemeris data decimal values
        # kloa0 and klob0 in second
        # kloa1 and klob1 in second/radian (semi circle*pi)
        # kloa2 and klob2 in second/radian^2
        # kloa3 and klob3 in second/radian^3
        file = open('ublox_processed_data.txt', 'r')
        klobuchar = []
        for line in file:
            if line[0:12] == 'b5620b024800':
                # hui message
                kloa0 = int(line[84:92], 16)*pow(2, -30)
                kloa1 = int(line[92:100], 16)*pow(2, -27)/math.pi
                kloa2 = int(line[100:108], 16)*pow(2, -24)/pow(2, math.pi)
                kloa3 = int(line[108:116], 16)*pow(2, -24)/pow(3, math.pi)
                klob0 = int(line[116:124], 16)*pow(2, 11)
                klob1 = int(line[124:132], 16)*pow(2, 14)/math.pi
                klob2 = int(line[132:140], 16)*pow(2, 16)/pow(2, math.pi)
                klob3 = int(line[140:148], 16)*pow(2, 16)/pow(3, math.pi)
                klobuchar.append([kloa0, kloa1, kloa2, kloa3, klob0, klob1, klob2, klob3])
        file.close()
        return klobuchar

    @staticmethod
    def ephemeris_data():
        # creates the matrix of ephemeris data with application of the scale factor decimal values
        # toc and toe in seconds, af2 in sec/sec^2, af1 in sec/sec, af0 in sec,
        # cuc cus cic and cis in radians, sqrta in meter^0,5
        # omega0 omega m0 and i0 in radians (semi circles * pi),
        # crc and crs in meters, deltan omegadot and idot in rad/sec (semicircles*pi/sec)
        file = open('ublox_processed_data.txt', 'r')
        ephemeris = []
        for line in file:
            if line[0:12] == 'b5620b316800':
                # eph message
                hexline = int(line, 16)
                binline = format(hexline, 'b')
                join = ''
                svid = int(binline[48:56], 2)
                wn = int(binline[112:122], 2)
                cap = int(binline[122:124], 2)
                ura = int(binline[124:128], 2)
                health = int(binline[128:134], 2)
                iodc = int(join.join((binline[134:136], binline[272:280])), 2)
                tgd = int(binline[256:264], 2)
                toc = int(binline[280:296], 2)*pow(2, 4)
                af2 = int(binline[304:312], 2)*pow(2, -55)
                af1 = int(binline[312:328], 2)*pow(2, -43)
                af0 = int(binline[336:358], 2)*pow(2, -31)
                iodesf2 = int(binline[368:376], 2)
                crs = int(binline[376:392], 2)*pow(2, -5)
                deltan = int(binline[400:416], 2)*pow(2, -43)
                m0 = int(join.join((binline[416:424], binline[432:456])), 2)*pow(2, -31)*math.pi
                cuc = int(binline[464:480], 2)*pow(2, -29)
                e = int(join.join((binline[480:488], binline[496:520])), 2)*pow(2, -33)
                cus = int(binline[528:544], 2)*pow(2, -29)
                sqrta = int(join.join((binline[544:552], binline[560:584])), 2)*pow(2, -19)
                toe = int(binline[592:608], 2)*pow(2, 4)
                flag = int(binline[608], 2)
                aodo = int(binline[609:614], 2)
                cic = int(binline[624:640], 2)*pow(2, -29)
                omega0 = int(join.join((binline[640:648], binline[656:680])), 2)*pow(2, -31)*math.pi
                cis = int(binline[688:704], 2)*pow(2, -29)
                i0 = int(join.join((binline[704:712], binline[720:744])), 2)*pow(2, -31)*math.pi
                crc = int(binline[752:768], 2)*pow(2, -5)
                omega = int(join.join((binline[768:776], binline[784:808])), 2)*pow(2, -31)*math.pi
                omegadot = int(binline[816:840], 2)*pow(2, -43)*math.pi
                iodesf3 = int(binline[848:856], 2)
                idot = int(binline[856:870], 2)*pow(2, -43)*math.pi
                ephemeris.append([svid, wn, cap, ura, health, iodc, tgd, toc, af2, af1, af0, iodesf2,
                                  crs, deltan, m0, cuc, e, cus, sqrta, toe, flag, aodo, cic, omega0,
                                  cis, i0, crc, omega, omegadot, iodesf3, idot])
        file.close()
        return ephemeris

    @staticmethod
    def raw_data():
        # Stores the PRN data under this way :
        # print(raw) == [['a', 'b', 'c', [[15, 1, 2, 3, 4, 5, 6], [16, 2, 3, 4, 5, 6, 7]]], ['a', 'b', 'c', ...
        # to access data of the first message :
        # print(raw[0]) == ['a', 'b', 'c', [[15, 1, 2, 3, 4, 5, 6], [16, 2, 3, 4, 5, 6, 7]]]
        # to access rcvtow : print(raw[0][1])
        # to access the inter matrix : print(raw[0][3]
        # to access the cpmes of the first satellite : print(raw[0][3][0][0])
        file = open('ublox_processed_data.txt', 'r')
        raw = []
        for line in file:
            if line[0:8] == 'b5620210':
                # RXM-RAW
                # rcvtow in ms, week in weeks, cpmes in cycles, prmes in m, domes in Hz, cno in dBHz
                inter = []
                rcvtow = int(line[12:20], 16)
                week = int(line[20:24], 16)
                numsv = int(line[24:26], 16)
                for sat in range(numsv):
                    cpmes = int(line[(28 + 24*sat):(44 + 24*sat)], 16)
                    prmes = int(line[(44 + 24*sat):(60 + 24*sat)], 16)
                    domes = int(line[(60 + 24*sat):(68 + 24*sat)], 16)
                    sv = int(line[(68 + 24*sat):(70 + 24*sat)], 16)
                    mesqi = int(line[(70 + 24*sat):(72 + 24*sat)], 16)
                    cno = int(line[(72 + 24*sat):(74 + 24*sat)], 16)
                    lli = int(line[(74 + 24*sat):(76 + 24*sat)], 16)
                    inter.append([cpmes, prmes, domes, sv, mesqi, cno, lli])
                raw.append([rcvtow, week, numsv, inter])
        file.close()
        return raw

    @staticmethod
    def random_data():
        file = open('ublox_processed_data.txt', 'r')
        nav = []
        dop = []
        svsi = []
        for line in file:
            if line[0:12] == 'b56206242400':
                # CFG-NAV5
                # fixedalt in m, fixedaltvar in m^2, minelev in deg, pacc and tacc in m,
                # staticholdthresh in cm/s, dgpstimeout in s, cnothresh in dBHz
                dynmodel = int(line[16:18], 16)
                fixmode = int(line[18:20], 16)
                fixedalt = int(line[20:28], 16)
                fixedaltvar = int(line[28:36], 16)
                minelev = int(line[36:38], 16)
                pdop = int(line[40:44], 16)
                tdop = int(line[44:48], 16)
                pacc = int(line[48:52], 16)
                tacc = int(line[52:56], 16)
                staticholdthresh = int(line[56:58], 16)
                dgpstimeout = int(line[58:60], 16)
                cnothreshnumsv = int(line[60:62], 16)
                cnothresh = int(line[62:64], 16)
                nav.append([dynmodel, fixmode, fixedalt, fixedaltvar, minelev, pdop, tdop,
                            pacc, tacc, staticholdthresh, dgpstimeout, cnothreshnumsv, cnothresh])
            if line[0:12] == 'b56201041200':
                # NAV-DOP
                itow = int(line[12:20], 16)
                gdop = int(line[20:24], 16)
                pdop = int(line[24:28], 16)
                tdop = int(line[28:32], 16)
                vdop = int(line[32:36], 16)
                hdop = int(line[36:40], 16)
                ndop = int(line[40:44], 16)
                edop = int(line[44:48], 16)
                dop.append([itow, gdop, pdop, tdop, vdop, hdop, ndop, edop])
            if line[0:8] == 'b5620220':
                # RXM-SVSI
                # itow in ms, week in weeks
                # to access the svid of the first satellite : print(svid[0][4][0][0])
                itow = int(line[12:20], 16)
                week = int(line[20:24], 16)
                numvis = int(line[24:26], 16)
                numsv = int(line[26:28], 16)
                inter = []
                for sat in range(numvis):
                    svid = int(line[28:30], 16)
                    azim = int(line[32:36], 16)
                    elev = int(line[36:38], 16)
                    age = int(line[38:40], 16)
                    inter.append([svid, azim, elev, age])
                svsi.append([itow, week, numvis, numsv, inter])
        file.close()
        return nav, dop, svsi

    @staticmethod
    def nmea_data_gbs():
        file = open('ublox_processed_data.txt', 'r')
        satfaultdetection = []
        for line in file:
            if line[3:6] == 'GBS':
                    # errlat, errlong, erralt are expected error in LLA in meters
                # svid gives the sat ID of most likely failed sat
                data = line.split(',')
                tme = data[1]
                errlat = data[2]
                errlong = data[3]
                erralt = data[4]
                svid = data[5]
                satfaultdetection.append([tme, errlat, errlong, erralt, svid])
        file.close()
        return satfaultdetection

    @staticmethod
    def nmea_data_gsa():
        file = open('ublox_processed_data.txt', 'r')
        dopandactivesat = []
        for line in file:
            if line[3:6] == 'GSA':
                data = line.split(',')
                activesat = data[3:14]
                pdop = data[15]
                hdop = data[16]
                vdop = data[17]
                dopandactivesat.append([activesat, pdop, hdop, vdop])
        file.close()
        return dopandactivesat

    @staticmethod
    def nmea_data_vtg():
        file = open('ublox_processed_data.txt', 'r')
        courseandspeed = []
        for line in file:
            if line[3:6] == 'VTG':
                # spd = speed over ground in knot/s
                # cogt = course over ground true in degrees
                # kph = speed over ground in kilometer per hour
                data = line.split(',')
                cogt = data[1]
                spd = data[5]
                kph = data[7]
                courseandspeed.append([cogt, spd, kph])
        file.close()
        return courseandspeed

    @staticmethod
    def nmea_data_pubx3():
        file = open('ublox_processed_data.txt', 'r')
        satinview = []
        for line in file:
            if line[0:8] == '$PUBX,03':
                # az = azimut in degrees
                # elev = elevation in degrees
                # cno in dBHz
                data = line.split(',')
                inter = []
                nbsat = int(data[2])
                for i in range(nbsat):
                    svid = data[3 + i*6]
                    svstatus = data[4 + i*6]
                    az = data[5 + i*6]
                    elev = data[6 + i*6]
                    cno = data[7 + i*6]
                    inter.append([svid, svstatus, az, elev, cno])
                satinview.append([nbsat, inter])
        file.close()
        return satinview

    def read_data(self, file):
        info = self.device.readline()
        if info[0:2] != b'$P' and info[0:2] != b'$G':
            file.write(binascii.hexlify(info))
        else:
            file.write(info)
