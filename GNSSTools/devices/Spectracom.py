# Tampere University of Technology
#
# DESCRIPTION
# defines initialisation functions of the spectracom, functions used to set parameters and to read
# information
#
# AUTHOR
# Anne-Marie Tobie

import time
import pyvisa
import interval
from GNSSTools import tools
from GNSSTools.devices.device import Device


class Spectracom(Device):

    def __init__(self, com, datafile='datatxt/spectracom_data.nmea', currentposfile='current_pos.txt', almanach='almanach.txt'):
        super(Spectracom, self).__init__()
        self.com = com
        self.datafile = datafile
        self.currentposfile = currentposfile
        self.almanach = almanach
        try:
            self.spectracom = pyvisa.ResourceManager().open_resource(self.com)
        except:
            raise ValueError('Connection with spectracom device failed')

    def clear(self):
        # Clears the status data structures by clearing all event registers and the error queue
        # also possible executing of scenario or signal generator is stopped
        return self.spectracom.write('*CLS')

    def reset(self):
        # Resets the device, any ongoing activity is stopped and the device is prepared to start new
        # operations
        return self.spectracom.write('*RST')

    def set_datetime(self, date, hour):
        # Sets the scenario start time as GPS time
        # Inputs: string format:
        # date: MM-DD-YYYY,  MM=Month {01- 12}, DD=day of month {01- 31}, YYYY=year
        # hour: hh:mm:ss.s, hh=hours {00- 23}, mm=minutes {00-59}
        return self.spectracom.write('SOURce:SCENario:DATEtime %s %s' % (date, hour))

    def control(self, control):
        # Launches, holds, arms or stops the scenario
        # Inputs:
        # control: {START,STOP,HOLD,ARM}
        return self.spectracom.write('SOURce:SCENario:CONTrol %s' % control)

    def set_power(self, power):
        # sets the transmit power of the device. The power for ublox integrity must be less (or
        # equal) than-130 dBm!!
        # Input:
        # power: decimal [-160,-65] dBm
        return self.spectracom.write('SOURce:POWer %f' % power)

    def set_observation(self):
        self.spectracom.write('SOURce:SCENario:OBS 10,3800, 1')

    def set_ext_attenuation(self, extatt):
        # Sets the external attenuation of the device. Note : Setting not stored during
        # scenario or 1-channel mode execution.
        # Input:
        # extatt: decimal = [0, 30] in dB
        return self.spectracom.write('SOURce:EXTATT %f' % extatt)

    def set_position(self, lat, long, alt):
        # Sets the position to the generator
        # Input:
        # lat: Decimal Latitude [-89.99999999, +89.99999999] degrees North
        # long: Decimal Longitude [-360.00000000, +360.00000000] degrees East
        # alt: Decimal Altitude [-1000.00, +20,200,000.00] meters
        return self.spectracom.write('SOURce:SCENario:POSition IMM, %f, %f, %f' % (lat, long, alt))

    def set_ecefpos(self, x, y, z):
        # Sets the ECEF position in X, Y, Z coordinates as the start position for the loaded scenario
        # or the current position if the scenario is Running.
        # Inputs:
        # x: Decimal X Position [-26 500 000.00, +26 500 000.00] meters
        # y: Decimal Y Position [-26 500 000.00, +26 500 000.00] meters
        # z: Decimal Z Position [-26 500 000.00, +26 500 000.00] meters
        return self.spectracom.write('SOURce:SCENario:ECEFPOSition IMM, %f, %f, %f' % x, y, z)

    def set_duration(self, start, duration, inter):
        # Turn on scenario observations.
        # Inputs:
        # start: Decimal start [-1,nnn] seconds. If ‘-1’ is used the logging will start immediately when a command is
        #        received number of seconds from scenario start.
        # duration: length of observations from start.
        # interval: the interval between the individual observations in the resulting Rinex OBS file
        return self.spectracom.write('SOURce:SCENario:OBS %f, %f, %f' % (start, tools.get_sec(duration), inter))

    def set_heading(self, heading):
        # Sets the vehicle true heading.
        # Input:
        # heading: Decimal Heading [0, 359.999] true heading in decimal degrees the heading is expressed
        #          in clockwise direction from the true north representing 0 degrees, increasing to 359.999 degrees
        return self.spectracom.write('SOURce:SCENario:HEADing imm, %f' % heading)

    def set_speed(self, speed):
        # Sets the vehicle's speed over ground (WGS84 ellipsoid)
        # Input:
        # speed: decimal 1D speed [0.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:SPEed imm, %f' % speed)

    def set_acceleration(self, acceleration):
        # Sets the 1D acceleration expressed in m/s2 when scenario is running.
        # Input:
        # acceleration: decimal 1d acceleration [-981 to +981] m/s2, ie [-100G to +100g]
        return self.spectracom.write('SOURce:SCENario:ACCeleration IMM, %f' % acceleration)

    def set_rateheadind(self, rateheading):
        # Set the heading change rate.
        # Input:
        # rateheading: Decimal RateHeading [-180.000, 180.000] true heading change in decimal degrees per second
        #              Positive value correspond to right turn, negative – left turn.
        return self.spectracom.write('SOURce:SCENario:RATEHEading IMM, %f' % rateheading)

    def set_turnrate(self, turnrate):
        # Set the rate of turning.
        # Input:
        # turnrate: Decimal TurnRate [- 180.000, 180.000] desired average heading rate (over single full closed circle)
        #           in decimal degrees per second. Positive value correspond to right turn, negative – left turn.
        return self.spectracom.write('SOURce:SCENario:TURNRATE IMM, %f' % turnrate)

    def set_turnradius(self, turnradius):
        # Sets the radius of turning. Radius is expressed in meters
        # Input:
        # turnradius: Decimal TurnRadius [-5 000 000.000, 5 000 000.000] radius of turning in meters. Positive value
        #             correspond to right turn, negative – left turn.
        return self.spectracom.write('SOURce:SCENario:TURNRADIUS IMM %f' % turnradius)

    def set_noise(self, noise):
        # set the noise simulation ON OFF
        return self.spectracom.write('SOURce:NOISE:CONTrol %s' % noise)

    def set_cno(self, cno):
        # set the maximum carrier to noise density of the simulated signals
        # Input:
        # cno: in dB.Hz, a decimal number, within the range [0.0, 56]
        return self.spectracom.write('SOURce:NOISE:CNO %f' % cno)

    def set_propa(self, env, sky, obstruction, nlos):
        # Sets built-in propagation environment model. The scenario must be running
        # <URBAN SUBURBAN RURAL OPEN> [,<sky_limit>, <obstruction_limit>, <nlos_probability>]
        # Inputs:
        # env: <URBAN SUBURBAN RURAL OPEN>
        # sky: decimal [00.0, 90.0] sky_limit: elevation above which there is no obstruction
        # obstruction: decimal [00.0, 90.0] obstruction_limit: elevation below ther is no line of sight satellites
        # nlos: decimal [0.0,1.0] nlos_probability: probability for a satellite with elevation between sky limit
        #       and obstruction limit to be non line of sight
        return self.spectracom.write('SOURce:SCENario:PROPenv %s, %f, %f, %f' % (env, sky, obstruction, nlos))

    def set_antenna(self, antenna):
        # Set the antenna model for the current scenario
        # Input:
        # antenna: model can be : Zero model, Helix, Patch, Cardioid
        return self.spectracom.write('SOURce:SCENario:ANTennamodel %s' % antenna)

    def set_tropo(self, tropo):
        # set the tropospheric model for the current scenario
        # Input:
        # tropo: tropospheric model can be : Saastamoinen, black, Goad&Goodman, Stanag
        return self.spectracom.write('SOURce:SCENario:TROPOmodel %s' % tropo)

    def set_iono(self, iono):
        # Select the ionospheric model to be used in the current scenario.
        # Input:
        # iono: Permitted values are ON and OFF
        return self.spectracom.write('SOURce:SCENario:IONOmodel %s' % iono)

    def set_keepalt(self, keepalt):
        # sets the altitude model setting for the current scenario. Default setting is ON.
        # When the model is active, the units will compensate for the altitude change resulting
        # from the difference between the ENU plane and the ellipsoid model of the earth.
        # Input:
        # keepalt: Permitted values are ON and OFF
        return self.spectracom.write('SOURce:SCENario:KEEPALTitude %s' % keepalt)

    def set_multipath(self, multipath):
        # This command sets the multipath parameters for satellite with a satID.
        # Input:
        # multipath: <satID>,<rangeoffset>,<rangechange>,<rangeinterval>,<doppleroffset>,<dopplerchange>,
        #            <dopplerinterval>,<poweroffset>,<powerchange>,<powerinterval>
        #                       satID: Satellite identifier of the satellite to update
        #                       rangeoffset: the Range Offset in meters [-999.0, 999.0]
        #                       rangechange: Range Change rate in meter/interval [-99.0, 99.0]
        #                       rangeinterval: Range Interval in seconds [0.0, 600.0]
        #                       doppleroffset: Doppler Offset in meters [-99.0, 99.0]
        #                       dopplerchange: Doppler Change rate in meters/sec/interval [-99.0, 99.0]
        #                       dopplerinterval: Doppler Interval in sec [0.0, 600.0]
        #                       poweroffset: Power Offset in meters [-30.0, 0.0]
        #                       powerchange: Power Change rate in dB/interval [-30.0, 0,0] and
        #                       powerinterval: Power Interval in seconds [0.0, 600.0].
        return self.spectracom.write('SOURce:SCENario:MULtipath IMM, %s' % multipath)

    def set_velocity(self, speed, heading):
        # Sets the vehicle's speed over ground (WGS84 ellipsoid) and heading in degrees
        # Input:
        # speed: Decimal 1D speed [0.000 to +20000.000] m/s
        # heading: Decimal bearing [0, 359.999] true bearing in decimal degrees
        return self.spectracom.write('SOURce:SCENario:VELocity IMM, %f, %f' % (speed, heading))

    def set_verticalspeed(self, vspeed):
        # Sets the vehicle's vertical speed
        # Input:
        # vspeed: Decimal 1D Speed [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:VSPEed IMM, %f' % vspeed)

    def set_enuvel(self, vest, vnorth, vup):
        # Sets the velocity expressed in ENU coordinates when scenario is running
        # Inputs:
        # vest: velocity East in [-20000.00 to +20000.00] m/s
        # vnorth: velocity North in [-20000.00 to +20000.00] m/s
        # vup: velocity Up in [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:ENUVELocity IMM, %f, %f, %f' % (vest, vnorth, vup))

    def set_ecefvel(self, velx, vely, velz):
        # Sets the current ECEF velocity in X, Y and Z coordinates when the scenario is running
        # Inputs:
        # velx: velocity X in [-20000.00 to +20000.00] m/s
        # vely: velocity Y in [-20000.00 to +20000.00] m/s
        # velz: velocity Z in [-20000.00 to +20000.00] m/s
        return self.spectracom.write('SOURce:SCENario:ECEFVELocity IMM, %f, %f, %f' % (velx, vely, velz))

    def set_vacceleration(self, vaccel):
        # Sets the vehicle's vertical acceleration
        # Input:
        # vaccel: Decimal 1D Acceleration [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:VACCel IMM, %f' % vaccel)

    def set_enuaccel(self, aest, anorth, aup):
        # Sets the acceleration expressed in ENU coordinates when scenario is running
        # Inputs:
        # aest: Acceleration East [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        # anorth: Acceleration North [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        # aup: Acceleration Up [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:ENUACCel IMM, %f, %f, %f' % (aest, anorth, aup))

    def set_ecefaccel(self, accelx, accely, accelz):
        # Sets the ECEF acceleration in 3-dimensions as acceleration X, Y, Z when scenario is running
        # Inputs:
        # accelx: Acceleration X [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        # accely: Acceleration Y [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        # accelz: Acceleration Z [-981 to +981] m/s^2 equivalent to [-100G to +100G]
        return self.spectracom.write('SOURce:SCENario:ECEFACCel IMM, %f, %f, %f' % (accelx, accely, accelz))

    def set_pryattitude(self, pitch, roll, yaw):
        # Sets the vehicle attitude in 3-dimension about the center of mass as Pitch, Roll and Yaw
        # when scenario is running.
        # Inputs:
        # pitch: Decimal Pitch [-?, +?] Radians
        # roll: Decimal Roll [-?, +?] Radians
        # yaw: Decimal Yaw [-?, +?] Radians
        return self.spectracom.write('SOURce:SCENario:PRYattitude IMM, %f, %f, %f' % (pitch, roll, yaw))

    def set_dpryatt(self, pitch, roll, yaw):
        # Sets the vehicle attitude in 3-dimension about the center of mass as Pitch, Roll and Yaw
        # when scenario is running.
        # Input:
        # dpryatt: <pitch>,<roll>,<yaw>
        #                   pitch: Decimal Pitch [-180, +180] Degrees
        #                   roll: Decimal Roll [-180, +180] Degrees
        #                   yaw: Decimal Yaw [-180, +180] Degrees
        return self.spectracom.write('SOURce:SCENario:DPRYattitude IMM, %f, %f, %f' % (pitch, roll, yaw))

    def set_kepler(self, kepler):
        # Sets the Kepler orbit parameters
        # Input:
        # kepler: <meananomaly>,<eccentricity>,<semimajoraxis>,<ascension>,<inclination>,<argperigee>
        #                       meananomaly: Decimal Mean anomaly [-?] radians
        #                       eccentricity: Decimal Eccentricity
        #                       semimajoraxis: Decimal Semi-major axis
        #                       ascension: Decimal Ascension of ascending node [-?, +?] Radians
        #                       inclination: Decimal Inclination [-?, +?] Radians
        #                       argperigee: Decimal Argument of perigee [-?, +?] Radians
        return self.spectracom.write('SOURce:SCENario:KEPLER IMM, %s' % kepler)

    def info_available(self, scenario, section):
        # Traverse the array containing the scenario data and if there is an information available,
        # set it to the Spectracom
        # Inputs:
        # scenario: array containing information of the test.ini file
        # section: section of the scenario
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
        if scenario[section][16] != '':
            info = scenario[section][16].split(',')
            self.set_ecefpos(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][17] != '':
            self.set_multipath(scenario[section][17])
        if scenario[section][18] != '':
            info = scenario[section][18].split(',')
            self.set_velocity(float(info[0]), float(info[1]))
        if scenario[section][19] != '':
            self.set_verticalspeed(scenario[section][19])
        if scenario[section][20] != '':
            info = scenario[section][20].split(',')
            self.set_enuvel(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][21] != '':
            info = scenario[section][21].split(',')
            self.set_ecefvel(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][22] != '':
            self.set_vacceleration(scenario[section][22])
        if scenario[section][23] != '':
            info = scenario[section][23].split(',')
            self.set_enuaccel(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][24] != '':
            info = scenario[section][24].split(',')
            self.set_ecefaccel(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][25] != '':
            info = scenario[section][25].split(',')
            self.set_pryattitude(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][26] != '':
            info = scenario[section][26].split(',')
            self.set_dpryatt(float(info[0]), float(info[1]), float(info[2]))
        if scenario[section][27] != '':
            self.set_kepler(scenario[section][27])

    def set_default(self, scenario,  section):
        # Traverse the array containing the scenario data and if there is no information available,
        # set default values to the Spectracom
        # Inputs:
        # scenario: array containing information of the test.ini file
        # section: section of the scenario
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
        if scenario[section][18] != '':
            self.set_velocity(0.0, 0)
        if scenario[section][19] != '':
            self.set_verticalspeed(0.0)
        if scenario[section][20] != '':
            self.set_enuvel(0.0, 0.0, 0.0)
        if scenario[section][21] != '':
            self.set_ecefvel(0.0, 0.0, 0.0)
        if scenario[section][22] != '':
            self.set_vacceleration(0.0)
        if scenario[section][23] != '':
            self.set_enuaccel(0.0, 0.0, 0.0)
        if scenario[section][24] != '':
            self.set_ecefaccel(0.0, 0.0, 0.0)
        if scenario[section][25] != '':
            self.set_pryattitude(0, 0, 0)
        if scenario[section][26] != '':
            self.set_dpryatt(0, 0, 0)

    def scenario_reading(self, scenario):
        # Run the scenario chosen, set parameters and save data in a file
        # Input:
        # scenario: array containing information of the chosen test.ini file
        # Output:
        # when a section is done, gives a set of information specified in query function
        print('Running...')
        savefile = open(self.datafile, 'w')
        for section in range(len(scenario)-2):
            section += 1
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
                    self.info_available(scenario, section)
                    self.data(savefile)
                self.set_default(scenario, section)

            else:
                if (scenario[section][0] != '') or (scenario[section][1] != '') or (scenario[section][2] != ''):
                    self.set_position(float(scenario[section][0]), float(scenario[section][1]),
                                      float(scenario[section][2]))
                self.info_available(scenario, section)
                self.data(savefile)
                duration = tools.get_sec(scenario[section][3])
                tps = time.time()
                while time.time() - tps < duration:
                    self.data(savefile)
                self.set_default(scenario, section)
            self.query()
        savefile.close()
        self.query()
        print('End')

    def query(self):
        print('LLA position', self.spectracom.query('SOURce:SCENario:POSition?'))
        print('ECEF position', self.spectracom.query('SOURce:SCENario:ECEFPOSition?'))
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
        print('speed over ground', self.spectracom.query('SOURce:SCENario:VELocity?'))
        print('vertical speed', self.spectracom.query('SOURce:SCENario:VSPEed?'))
        print('ENU velocity', self.spectracom.query('SOURce:SCENario:ENUVELocity?'))
        print('ECEF velocity', self.spectracom.query('SOURce:SCENario:ECEFVELocity?'))
        print('vertical acceleration', self.spectracom.query('SOURce:SCENario:VACCel?'))
        print('ENU acceleration', self.spectracom.query('SOURce:SCENario:ENUACCel?'))
        print('ECEF acceleration', self.spectracom.query('SOURce:SCENario:ECEFACCel?'))
        print('PRY attitude', self.spectracom.query('SOURce:SCENario:PRYattitude?'))
        print('DPRY attitude', self.spectracom.query('SOURce:SCENario:DPRYattitude?'))
        print('Kepler', self.spectracom.query('SOURce:SCENario:KEPLER?'))


    def data(self, savefile):
        # take the data and print the result into the savefile chosen
        # Input:
        # savefile: chosen savefile tu store data
        data = self.spectracom.query('SOURce:SCENario:LOG?')
        savefile.write(data)

    def get_data(self):
        # take the nmea data for the duration of the scenario sent by the spectracom and store them into the file
        savefile = open(self.datafile, 'w')
        while True:
            data = self.spectracom.query('SOURce:SCENario:LOG?')
            savefile.write(data)
            time.sleep(0.8)
        savefile.close()
        return savefile

    def get_current_pos(self):
        # save the current position in this shape [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m]
        savefile = open(self.currentposfile, 'w')
        data = self.spectracom.query('SOURce:SCENario:LOG?')
        savefile.write(data)
        savefile.close()
        pos = (tools.data(self.currentposfile))
        return pos

    def get_almanach(self):
        # Return:
        # a matrix of almanach data, almanach[i] contains:
        # [ID, Health, Eccentricity, Time of Applicability in seconds, Orbital Inclination in rad,
        # Rate of Right Ascen in rad/s, SQRT(A) in m 1/2, Right Ascen at Week(rad), Argument of Perigee in rad
        # Mean Anom in rad, Af0 in s, Af1 in s/s, week]
        self.spectracom.write('MMEMory:CDIRectory observations')
        file = open(self.almanach, 'w')
        file.write(self.spectracom.query('MMEMory:DATA? alm_gps.txt'))
        file.close()
        file = open(self.almanach, 'r')
        i = 0
        almanach = []
        inter = []
        for line in file:
            if line[0] == '#' or line[0] == '\n':
                pass
            elif line[0] == '*':
                i += 1
                almanach.append(inter)
                inter = []
            else:
                b = 0
                while line[27 + b] != '\n':
                    b += 1
                inter.append(line[27:(27 + b)])
        almanach.append(inter)
        file.close()
        return almanach
