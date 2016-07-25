# Tampere University of Technology
#
# DESCRIPTION
# define initialisation functions of the spectracom, functions used to set parameters and to read
# information
#
# AUTHOR
# Anne-Marie Tobie

import pyvisa
import time
import interval
import tools
import config_parser

scenario = config_parser.read_scen()


class Spectracom:
    # Makes the connection with the Spectracom, clear it and reset it
    def __init__(self, com):
        self.com = com
        try:
            self.spectracom = pyvisa.ResourceManager().open_resource(self.com)
        except:
            raise ValueError('Connection with spectracom device failed')

    def clear(self):
        # clears the status data structures by clearing all event registers and the error queue
        # also possible executing of scenario or signal generator is stopped
        return self.spectracom.write('*CLS')

    def reset(self):
        # Reset the device, any ongoing activity is stopped and the device is prepared to start new
        # operations
        return self.spectracom.write('*RST')

    def set_datetime(self, date, hour):
        # Set the scenario start time as GPS time
        return self.spectracom.write('SOURce:SCENario:DATEtime %s %s' % (date, hour))

    def control(self, control):
        # Launch or stop the scenario
        return self.spectracom.write('SOURce:SCENario:CONTrol %s' % control)

    def set_power(self, power):
        # sets the transmit power of the device. The power for ublox integrity must be less (or
        # equal) than-130 dBm!!
        return self.spectracom.write('SOURce:POWer %f' % power)

    def set_ext_attenuation(self, extatt):
        # Set the external attenuation of the device. Note : Setting not stored during
        # scenario or 1-channel mode execution. Parameter : decimal = [0, 30] in dB
        return self.spectracom.write('SOURce:EXTATT %f' % extatt)

    def set_position(self, lat, long, alt):
        # set the position to the generator
        return self.spectracom.write('SOURce:SCENario:POSition IMM, %f, %f, %f' % (lat, long, alt))

    def set_ecefpos(self, x, y, z):
        # Sets the ECEF position in X, Y, Z coordinates as the start position for the loaded scenario
        # or the current position if the scenario is Running. The X, Y, Z position is given in decimal meters
        return self.spectracom.write('SOURce:SCENario:ECEFPOSition IMM, %f, %f, %f' % x, y, z)

    def set_duration(self, start, duration, inter):
        # Turn on scenario observations. Start is the number of seconds from scenario start.
        # Duration is length of observations from start. Interval is the interval between the individual
        # observations in the resulting Rinex OBS file
        return self.spectracom.write('SOURce:SCENario:OBS %f, %f, %f' % (start, tools.Tools.get_sec(duration), inter))

    def set_heading(self, heading):
        # sets the vehicle true heading. the heading is expressed in clockwise direction
        # from the true north representing 0 degrees, increasing to 359.999 degrees
        return self.spectracom.write('SOURce:SCENario:HEADing imm, %f' % heading)

    def set_speed(self, speed):
        # sets the vehicle's speed over ground (WGS84 ellipsoid)
        # decimal 1D speed [0.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:SPEed imm, %f' % speed)

    def set_acceleration(self, acceleration):
        # Sets the 1D acceleration expressed in m/s2 when scenario is running. Parameter: decimal 1d
        # acceleration [-981 to +981] m/s2, ie [-100G to +100g]
        return self.spectracom.write('SOURce:SCENario:ACCeleration IMM, %f' % acceleration)

    def set_rateheadind(self, rateheading):
        # Set th heading change rate. Rate is expressed as degrees per second.
        return self.spectracom.write('SOURce:SCENario:RATEHEading IMM, %f' % rateheading)

    def set_turnrate(self, turnrate):
        # Set the rate of turning. Rate is expressed as degrees per second.
        return self.spectracom.write('SOURce:SCENario:TURNRATE IMM, %f' % turnrate)

    def set_turnradius(self, turnradius):
        # Sets the radius of turning. Radius is expressed in meters
        return self.spectracom.write('SOURce:SCENario:TURNRADIUS IMM %f' % turnradius)

    def set_noise(self, noise):
        # set the noise simulation ON OFF
        return self.spectracom.write('SOURce:NOISE:CONTrol %s' % noise)

    def set_cno(self, cno):
        # set the maximum carrier to noise density of the simulated signals
        # cn0 in dB.Hz, a decimalnumber, within the range [0.0, 56]
        return self.spectracom.write('SOURce:NOISE:CNO %f' % cno)

    def set_propa(self, env, sky, obstruction, nlos):
        # Sets built-in propagation environment model. The scenario must be running
        # <URBAN SUBURBAN RURAL OPEN> [,<sky_limit>, <obstruction_limit>, <nlos_probability>]
        # decimal [00.0, 90.0] sky_limit: elevation above which there is no obstruction
        # decimal [00.0, 90.0] obstruction_limit: elevation below ther is no line of sight satellites
        # decimal [0.0,1.0] nlos_probability: probability for a satellite with elevation between sky limit
        # and obstruction limit to be non line of sight
        return self.spectracom.write('SOURce:SCENario:PROPenv %s, %f, %f, %f' % (env, sky, obstruction, nlos))

    def set_antenna(self, antenna):
        # Set the antenna model for the current scenario
        # model can be : Zero model, Helix, Patch, Cardioid
        return self.spectracom.write('SOURce:SCENario:ANTennamodel %s' % antenna)

    def set_tropo(self, tropo):
        # set the tropospheric model for the current scenario
        # model can be : Saastamoinen, black, Goad&Goodman, Stanag
        return self.spectracom.write('SOURce:SCENario:TROPOmodel %s' % tropo)

    def set_iono(self, iono):
        # Select the ionospheric model to be used in the current scenario. Permitted values are ON
        # and OFF
        return self.spectracom.write('SOURce:SCENario:IONOmodel %s' % iono)

    def set_keepalt(self, keepalt):
        # sets the altitude model setting for the current scenario. Default setting is ON.
        # When the model is active, the units will compensate for the altitude change resulting
        # from the difference between the ENU plane and the ellipsoid model of the earth.
        return self.spectracom.write('SOURce:SCENario:KEEPALTitude %s' % keepalt)

    # def set_signaltype(signal):
        # Sets signal(s) to be simulated. Signal consists of comma separated list of signal names:
        # parameters: string GPSL1CA, GPSL1P or GPSL1PY, GPSL2P or GPSL2PY for GPS
        #             string GLOL1, GLOL2 for GLONASS
        #             string GALE1, GALE5a or GALE5b for Galileo
        #             string BDSB1, BDSB2 for BeiDou
    #    pass

    def set_multipath(self, multipath):
        # This command sets the multipath parameters for satellite with a satID. The parameters include
        # the Range Offset in meters [-999.0, 999.0], Range Change rate in meter/interval [-99.0, 99.0],
        # Range Interval in seconds [0.0, 600.0], Doppler Offset in meters [-99.0, 99.0],
        # Doppler Change rate in meters/sec/interval [-99.0, 99.0], Doppler Interval in sec [0.0, 600.0],
        # Power Offset in meters [-30.0, 0.0], Power Change rate in dB/interval [-30.0, 0,0] and
        # Power Interval in seconds [0.0, 600.0].
        return self.spectracom.write('SOURce:SCENario:MULtipath IMM, %s' % multipath)

    def set_velocity(self, speed, heading):
        # Sets the vehicle's speed over ground (WGS84 ellipsoid) and heading in degrees
        # parameter: Decimal 1D speed [0.000 to +20000.000] m/s
        #            Decimal bearing [0, 359.999] true bearing in decimal degrees
        return self.spectracom.write('SOURce:SCENario:VELocity IMM, %f, %f' % (speed, heading))

    def set_verticalspeed(self, vspeed):
        # Sets the vehicle's vertical speed
        # parameter: Decimal 1D Speed [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:VSPEed IMM, %f' % vspeed)

    def set_enuvel(self, vest, vnorth, vup):
        # Sets the velocity expressed in ENU coordinates when scenario is running
        # Parameters: velocity East, North, Up in [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:ENUVELocity IMM, %f, %f, %f' % (vest, vnorth, vup))

    def set_ecefvel(self, velx, vely, velz):
        # Sets the current ECEF velocity in X, Y and Z coordinates when the scenario is running
        # Parameters: velocity X, Y, Z in [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:ECEFVELocity IMM, %f, %f, %f' % (velx, vely, velz))

    def set_vacceleration(self, vaccel):
        # Sets the vehicle's vertical acceleration
        # Parameter: Decimal 1D Acceleration [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:VACCel IMM, %f' % vaccel)

    def set_enuaccel(self, aest, anorth, aup):
        # Sets the acceleration expressed in ENU coordinates when scenario is running
        # Parameter: Acceleration East, North, Up [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:ENUACCel IMM, %f, %f, %f' % (aest, anorth, aup))

    def set_ecefaccel(self, accelx, accely, accelz):
        # Sets the ECEF acceleration in 3-dimensions as acceleration X, Y, Z when scenario is running
        # Parameter: Acceleration X, Y, Z [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:ECEFACCel IMM, %f, %f, %f' % (accelx, accely, accelz))

    def set_pryattitude(self, pitch, roll, yaw):
        # Sets the vehicle attitude in 3-dimension about the center of mass as Pitch, Roll and Yaw
        # when scenario is running, parameters are in radians
        return self.spectracom.write('SOURce:SCENario:PRYattitude IMM, %f, %f, %f' % (pitch, roll, yaw))

    def set_dpryatt(self, pitch, roll, yaw):
        # Sets the vehicle attitude in 3-dimension about the center of mass as Pitch, Roll and Yaw
        # when scenario is running, parameters are in degrees [-180, +180]
        return self.spectracom.write('SOURce:SCENario:DPRYattitude IMM, %f, %f, %f' % (pitch, roll, yaw))

    def set_kepler(self, meananomaly, eccentricity, semimajoraxis, ascension, inclination, argumentperigee):
        # Sets the Kepler orbit parameters
        # Parameters: Mean anomaly, ascension of ascending node, inclination and argument of perigee are in radians
        return self.spectracom.write('SOURce:SCENario:KEPLER IMM, %f, %f, %f, %f, %f, %f' % (
                                     meananomaly, eccentricity, semimajoraxis, ascension, inclination, argumentperigee))

    def info_available(self, section):
        if scenario[section][4] != '':
            self.set_heading(float(scenario[section][4]))
        if scenario[section][5] != '':
            self.set_speed(float(scenario[section][5]))
        if scenario[section][6] != '':
            self.set_acceleration(float(scenario[section][6]))
        if scenario[section][7] != '':
            self.set_rateheadind(float(scenario[section][7]))
        if scenario[section][8] != '':
            self.set_turnrate(float(scenario[section][8]))
        if scenario[section][9] != '':
            self.set_turnradius(float(scenario[section][9]))
        if scenario[section][10] != '':
            self.set_noise('ON')
            self.set_cno(float(scenario[section][10]))
        if scenario[section][11] != '':
            info = scenario[section][11].split(',')
            self.set_propa(info[0], float(info[1]), float(info[2]), float(info[3]))
        if scenario[section][12] != '':
            self.set_antenna(scenario[section][12])
        if scenario[section][13] != '':
            self.set_tropo(scenario[section][13])
        if scenario[section][14] != '':
            self.set_iono(scenario[section][14])
        if scenario[section][15] != '':
            self.set_keepalt(scenario[section][15])
#    if scenario[section][16] != '':
#        self.set_signaltype(scenario[section][16])
#    if scenario[section][17] != '':
#        set_multipath(scenario[section][17])

    def set_default(self, section):
        if scenario[section][5] == '':
            self.set_speed(0.0)
        if scenario[section][6] == '':
            self.set_acceleration(0.0)
        if scenario[section][7] == '':
            self.set_rateheadind(0.0)
        if scenario[section][8] == '':
            self.set_turnrate(0.0)
        if scenario[section][9] == '':
            self.set_turnradius(0.0)
        if scenario[section][10] == '':
            self.set_noise('OFF')
        if scenario[section][11] == '':
            self.set_propa('OPEN', 0.0, 0.0, 0.0)
        if scenario[section][12] == '':
            self.set_antenna('Zero model')
        if scenario[section][13] == '':
            self.set_tropo('Saastamoinen')
        if scenario[section][14] == '':
            self.set_iono('OFF')
        if scenario[section][15] == '':
            self.set_keepalt('OFF')
#    if scenario[section][16] == '':
#        SpectracomCommand.set_signaltype('GPSL1CA')

    def scenario_reading(self):
        savefile = open('spectracom_data.nmea', 'w')
        for section in range(len(scenario)-2):
            section += 1
            print(section)
            if scenario[section][3] == '':
                # if there is no duration given in the scenario for the section
                precision = 0.00006
                while ((self.get_current_pos()[0][1] not in interval.Interval.between(
                        float(scenario[section][0]) - precision, float(scenario[section][0]) + precision)) and
                        ((self.get_current_pos()[0][2] not in interval.Interval.between(
                        float(scenario[section][0]) - precision, float(scenario[section][0]) + precision)))):
                    self.set_heading(tools.heading_compute(
                        self.get_current_pos()[0][1], (float(scenario[section][0])),
                        self.get_current_pos()[0][2], (float(scenario[section][1]))))
                    self.info_available(section)
                    self.data(savefile)
                self.set_default(section)

            else:
                print('boucle 5')
                if (scenario[section][0] != '') or (scenario[section][1] != '') or (scenario[section][2] != ''):
                    self.set_position(float(scenario[section][0]), float(scenario[section][1]),
                                      float(scenario[section][2]))
                self.info_available(section)
                self.data(savefile)
                duration = tools.Tools.get_sec(scenario[section][3])
                tps = time.time()
                while time.time() - tps < duration:
                    self.data(savefile)
                self.set_default(section)
            self.query()
        print('done')
        savefile.close()
        self.query()

    def query(self):
        print('position', self.spectracom.query('SOURce:SCENario:POSition?'))
        print('heading', self.spectracom.query('SOURce:SCENario:HEADing?'))
        print('speed', self.spectracom.query('SOURce:SCENario:SPEed?'))
        print('acceleration', self.spectracom.query('SOURce:SCENario:ACCeleration?'))
        print('rate heading', self.spectracom.query('SOURce:SCENario:RATEHEading?'))
        print('turn rate', self.spectracom.query('SOURce:SCENario:TURNRATE?'))
        print('turn radius', self.spectracom.query('SOURce:SCENario:TURNRADIUS?'))
        print('noise control', self.spectracom.query('SOURce:NOISE:CONTRol?'))
        print('noise cno', self.spectracom.query('SOURce:NOISE:CNO?'))
        print('propagation model', self.spectracom.query('SOURce:SCENario:PROPenv?'))
        print('antenna model', self.spectracom.query('SOURce:SCENario:ANTennamodel?'))
        print('tropospheric model', self.spectracom.query('SOURce:SCENario:TROPOmodel?'))
        print('ionospheric model', self.spectracom.query('SOURce:SCENario:IONOmodel?'))
        print('scenario signal type 1', self.spectracom.query('SOURce:SCENario:SIGNALtype1?'))

    def data(self, savefile):
        # take the data and print the result into the savefile chosen
        data = self.spectracom.query('SOURce:SCENario:LOG?')
        savefile.write(data)

    def get_data(self):
        # take the nmea data for the duration of the scenario
        # sent by the spectracom and print them into the file
        savefile = open('spectracom_data.nmea', 'w')
        while True:
            data = self.spectracom.query('SOURce:SCENario:LOG?')
            savefile.write(data)
            time.sleep(0.8)
        savefile.close()
        return savefile

    def get_current_pos(self):
        # save the current position in this shape [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m]
        savefile = open('current_pos.txt', 'w')
        data = self.spectracom.query('SOURce:SCENario:LOG?')
        savefile.write(data)
        savefile.close()
        pos = (tools.data('current_pos.txt'))
        return pos
