# Tampere University of Technology
#
# DESCRIPTION
# define initialisation function of the spectracom, functions used to set parameters and to read
# information
#
# AUTHOR
# Anne-Marie Tobie

import pyvisa
import time
import math
import interval
import connection
import tools
import config_parser


if connection.connect_spectracom() == 'connected':
    inst = pyvisa.ResourceManager().open_resource('USB0::0x14EB::0x0060::200448::INSTR')

scenario = config_parser.read_scen()


# INITIALISATION
def clear():
    # clears the status data structures by clearing all event registers and the error queue
    # also possible executing of scenario or signal generator is stopped
    return inst.write('*CLS')


def reset():
    # Reset the device, any ongoing activity is stopped and the device is prepared to start new
    # operations
    return inst.write('*RST')


def set_power(power):
    # sets the transmit power of the device. The power for ublox integrity must be less (or
    # equal) than -130 dBm!!
    return inst.write('SOURce:POWer %f' % power)


def set_ext_attenuation(extatt):
    # Set the external attenuation of the device. Note : Setting not stored during
    # scenario or 1-channel mode execution. Parameter : decimal = [0, 30] in dB
    return inst.write('SOURce:EXTATT %f' % extatt)

# SET SCENARIO


def set_datetime(date, hour):
    # Set the scenario start time as GPS time
    return inst.write('SOURce:SCENario:DATEtime %s %s' % (date, hour))


def set_position(lat, long, alt):
    # set the position to the generator
    return inst.write('SOURce:SCENario:POSition IMM, %f, %f, %f' % (lat, long, alt))


def set_ecefpos(x, y, z):
    # Sets the ECEF position in X, Y, Z coordinates as the start position for the loaded scenario
    # or the current position if the scenario is Running. The X, Y, Z position is given in decimal meters
    return inst.write('SOURce:SCENario:ECEFPOSition IMM, %f, %f, %f' % x, y, z)


def set_duration(start, duration, interval):
    # Turn on scenario observations. Start is the number of seconds from scenario start.
    # Duration is length of observations from start. Interval is the interval between the individual
    # observations in the resulting Rinex OBS file
    return inst.write('SOURce:SCENario:OBS %f, %f, %f' % (start, tools.Tools.get_sec(duration), interval))


def set_heading(heading):
    # sets the vehicle true heading. the heading is expressed in clockwise direction
    # from the true north representing 0 degrees, increasing to 359.999 degrees
    return inst.write('SOURce:SCENario:HEADing imm, %f' % heading)


def set_speed(speed):
    # sets the vehicle's speed over ground (WGS84 ellipsoid)
    # decimal 1D speed [0.00 to +20000.00] m/s
    return inst.write('SOURce:SCENario:SPEed imm, %f' % speed)


def set_acceleration(acceleration):
    # Sets the 1D acceleration expressed in m/s2 when scenario is running. Parameter: decimal 1d
    # acceleration [-981 to +981] m/s2, ie [-100G to +100g]
    return inst.write('SOURce:SCENario:ACCeleration IMM, %f' % acceleration)


def set_rateheadind(rateheading):
    # Set th heading change rate. Rate is expressed as degrees per second.
    return inst.write('SOURce:SCENario:RATEHEading IMM, %f' % rateheading)


def set_turnrate(turnrate):
    # Set the rate of turning. Rate is expressed as degrees per second.
    return inst.write('SOURce:SCENario:TURNRATE IMM, %f' % turnrate)


def set_turnradius(turnradius):
    # Sets the radius of turning. Radius is expressed in meters
    return inst.write('SOURce:SCENario:TURNRADIUS IMM %f' % turnradius)


def set_noise(noise):
    # set the noise simulation ON OFF
    return inst.write('SOURce:NOISE:CONTrol %s' % noise)


def set_cno(cno):
    # set the maximum carrier to noise density of the simulated signals
    # cn0 in dB.Hz, a decimalnumber, within the range [0.0, 56]
    return inst.write('SOURce:NOISE:CNO %f' % cno)


def set_propa(env, sky, obstruction, nlos):
    # Sets built-in propagation environment model. The scenario must be running
    # <URBAN SUBURBAN RURAL OPEN> [,<sky_limit>, <obstruction_limit>, <nlos_probability>]
    # decimal [00.0, 90.0] sky_limit: elevation above which there is no obstruction
    # decimal [00.0, 90.0] obstruction_limit: elevation below ther is no line of sight satellites
    # decimal [0.0,1.0] nlos_probability: probability for a satellite with elevation between sky limit
    # and obstruction limit to be non line of sight
    return inst.write('SOURce:SCENario:PROPenv %s, %f, %f, %f' % (env, sky, obstruction, nlos))


def set_antenna(antenna):
    # Set the antenna model for the current scenario
    # model can be : Zero model, Helix, Patch, Cardioid
    return inst.write('SOURce:SCENario:ANTennamodel %s' % antenna)


def set_tropo(tropo):
    # set the tropospheric model for the current scenario
    # model can be : Saastamoinen, black, Goad&Goodman, Stanag
    return inst.write('SOURce:SCENario:TROPOmodel %s' %tropo)


def set_iono(iono):
    # Select the ionospheric model to be used in the current scenario. Permitted values are ON
    # and OFF
    return inst.write('SOURce:SCENario:IONOmodel %s' % iono)


def set_keepalt(keepalt):
    # sets the altitude model setting for the current scenario. Default setting is ON.
    # When the model is active, the units will compensate for the altitude change resulting
    # from the difference between the ENU plane and the ellipsoid model of the earth.
    return inst.write('SOURce:SCENario:KEEPALTitude %s' % keepalt)


def set_signaltype(signal):
    # Sets signal(s) to be simulated. Signal consists of comma separated list of signal names:
    # parameters: string GPSL1CA, GPSL1P or GPSL1PY, GPSL2P or GPSL2PY for GPS
    #             string GLOL1, GLOL2 for GLONASS
    #             string GALE1, GALE5a or GALE5b for Galileo
    #             string BDSB1, BDSB2 for BeiDou
    pass

def set_multipath(multipath):
    # This command sets the multipath parameters for satellite with a satID. The parameters include
    # the Range Offset in meters [-999.0, 999.0], Range Change rate in meter/interval [-99.0, 99.0],
    # Range Interval in seconds [0.0, 600.0], Doppler Offset in meters [-99.0, 99.0],
    # Doppler Change rate in meters/sec/interval [-99.0, 99.0], Doppler Interval in sec [0.0, 600.0],
    # Power Offset in meters [-30.0, 0.0], Power Change rate in dB/interval [-30.0, 0,0] and
    # Power Interval in seconds [0.0, 600.0].
    return inst.write('SOURce:SCENario:MULtipath IMM %s' % multipath)


# SCENARIO


def set_init(date, hour, lat, long, alt, start, duration, interval):
    # set the configuration to the Spectracom
    set_datetime(date, hour)
    set_position(lat, long, alt)
    set_duration(start, duration, interval)


def heading_compute(lat1, lat2, long1, long2):
    # Compute the heading that has to be followed
    angle = abs(math.atan((long1-long2)/(lat1-lat2))*180/math.pi)
    if long2 >= long1:
        if lat2 >= lat1:
            heading = angle
        else:
            heading = 180 - angle
    else:
        if lat2 >= lat1:
            heading = 360 - angle
        else:
            heading = 180 + angle
    return heading


def info_available(section):
    if scenario[section][4] != '':
        set_heading(float(scenario[section][4]))
    if scenario[section][5] != '':
        set_speed(float(scenario[section][5]))
    if scenario[section][6] != '':
        set_acceleration(float(scenario[section][6]))
    if scenario[section][7] != '':
        set_rateheadind(float(scenario[section][7]))
    if scenario[section][8] != '':
        set_turnrate(float(scenario[section][8]))
    if scenario[section][9] != '':
        set_turnradius(float(scenario[section][9]))
    if scenario[section][10] != '':
        set_noise('ON')
        set_cno(float(scenario[section][10]))
    if scenario[section][11] != '':
        info = scenario[section][11].split(',')
        set_propa(info[0], float(info[1]), float(info[2]), float(info[3]))
    if scenario[section][12] != '':
        set_antenna(scenario[section][12])
    if scenario[section][13] != '':
        set_tropo(scenario[section][13])
    if scenario[section][14] != '':
        set_iono(scenario[section][14])
    if scenario[section][15] != '':
        set_keepalt(scenario[section][15])
    if scenario[section][16] != '':
        set_signaltype(scenario[section][16])
#    if scenario[section][17] != '':
#        set_multipath(scenario[section][17])

def set_default(section):
    if scenario[section][5] == '':
        set_speed(0.0)
    if scenario[section][6] == '':
        set_acceleration(0.0)
    if scenario[section][7] == '':
        set_rateheadind(0.0)
    if scenario[section][8] == '':
        set_turnrate(0.0)
    if scenario[section][9] == '':
        set_turnradius(0.0)
    if scenario[section][10] == '':
        set_noise('OFF')
    if scenario[section][11] == '':
        set_propa('OPEN', 0.0, 0.0, 0.0)
    if scenario[section][12] == '':
        set_antenna('Zero model')
    if scenario[section][13] == '':
        set_tropo('Saastamoinen')
    if scenario[section][14] == '':
        set_iono('OFF')
    if scenario[section][15] == '':
        set_keepalt('OFF')
    if scenario[section][16] == '':
        set_signaltype('GPSL1CA')


def query():
    print('position', inst.query('SOURce:SCENario:POSition?'))
    print('heading', inst.query('SOURce:SCENario:HEADing?'))
    print('speed', inst.query('SOURce:SCENario:SPEed?'))
    print('acceleration', inst.query('SOURce:SCENario:ACCeleration?'))
    print('rate heading', inst.query('SOURce:SCENario:RATEHEading?'))
    print('turn rate', inst.query('SOURce:SCENario:TURNRATE?'))
    print('turn radius', inst.query('SOURce:SCENario:TURNRADIUS?'))
    print('noise control', inst.query('SOURce:NOISE:CONTRol?'))
    print('noise cno', inst.query('SOURce:NOISE:CNO?'))
    print('propagation model', inst.query('SOURce:SCENario:PROPenv?'))
    print('antenna model', inst.query('SOURce:SCENario:ANTennamodel?'))
    print('tropospheric model', inst.query('SOURce:SCENario:TROPOmodel?'))
    print('ionospheric model', inst.query('SOURce:SCENario:IONOmodel?'))
    print('scenario signal type 1', inst.query('SOURce:SCENario:SIGNALtype1?'))
    print('scenario signal type 2', inst.query('SOURce:SCENario:SIGNALtype2?'))
    print('scenario signal type 3', inst.query('SOURce:SCENario:SIGNALtype3?'))
    print('scenario signal type 4', inst.query('SOURce:SCENario:SIGNALtype4?'))
    print('scenario signal type 5', inst.query('SOURce:SCENario:SIGNALtype5?'))
    print('scenario signal type 6', inst.query('SOURce:SCENario:SIGNALtype6?'))
    print('scenario signal type 7', inst.query('SOURce:SCENario:SIGNALtype7?'))
    print('scenario signal type 8', inst.query('SOURce:SCENario:SIGNALtype8?'))
    print('scenario signal type 9', inst.query('SOURce:SCENario:SIGNALtype9?'))



def scenario_reading():
    print('running...')
    savefile = open('spectracom_data.nmea', 'w')
    for section in range(len(scenario)-2):
        section += 1
        print(section)
        if scenario[section][3] == '':
            # if there is no duration given in the scenario for the section
            precision = 0.00006
            while ((get_current_pos()[0][1] not in interval.Interval.between(float(scenario[section][0]) - precision, float(scenario[section][0]) + precision)) and
                           (get_current_pos()[0][2] not in interval.Interval.between(float(scenario[section][0]) - precision, float(scenario[section][0]) + precision))):
                set_heading(heading_compute(get_current_pos()[0][1],(float(scenario[section][0])),
                                                get_current_pos()[0][2], (float(scenario[section][1]))))
                info_available(section)
                data(savefile)
            set_default(section)

        else:
            print('boucle 5')
            if (scenario[section][0] != '') or (scenario[section][1] != '') or (scenario[section][2] != ''):
                set_position(float(scenario[section][0]), float(scenario[section][1]), float(scenario[section][2]))
            info_available(section)
            data(savefile)
            duration = tools.Tools.get_sec(scenario[section][3])
            tps = time.time()
            while time.time() - tps < duration:
                data(savefile)
            set_default(section)
        query()
    print('done')
    savefile.close()
    query()


# CONTROL


def launch():
    # Launch the scenario charged previously
    return inst.write('SOURce:SCENario:CONTrol start')


def stop():
    # Stop the scenario from running
    return inst.write('SOURce:SCENario:CONTrol stop')

# GET DATA


def data(savefile):
    # take the data and print the result into the savefile chosen
    data = inst.query('SOURce:SCENario:LOG?')
    savefile.write(data)


def get_data(duration):
    # take the nmea data for the duration of the scenario
    # sent by the spectracom and print them into the file
    savefile = open('spectracom_data.nmea', 'w')
    duree = tools.Tools.get_sec(duration)
    i = 0
    while i <= duree:
        data = inst.query('SOURce:SCENario:LOG?')
        savefile.write(data)
        time.sleep(0.8)
        i += 1
        print(i)
    savefile.close()
    return savefile


def get_current_pos():
    # save the current position in this shape [time in HHMMSS.DD, LAT in DMS, LONG in DMS, ALT in m]
    savefile = open('current_pos.txt', 'w')
    data = inst.query('SOURce:SCENario:LOG?')
    savefile.write(data)
    savefile.close()
    pos = (tools.data('current_pos.txt'))
    return pos

# print(get_current_pos())
# print(inst.query('SOURce:SCENario:LOG?'))

# done = tools.data('spectracom_data.nmeaprint(done)
#stop()
