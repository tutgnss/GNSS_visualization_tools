__author__ = 'tobie'

import pyvisa, time, math
import connection, tools, config_parser

if connection.connect_spectracom() == 'connected':
    inst = pyvisa.ResourceManager().open_resource ('USB0::0x14EB::0x0060::200448::INSTR')

scenario = config_parser.read_scen()

## INITIALISATION

def clear():
    # clears the status data structures by clearing all event registers and the error queue
    # also possible executing of scenario or signal dgenerator is stopped
    return inst.write('*CLS')

def reset():
    # Reset the device, any ongoing activity is stopped and the device is prepared to start new
    # operations
    return inst.write('*RST')

def set_power (Power):
    #sets the transmit power of the device. The power for ublox integrity must be less (or
    # equal) than -130 dBm!!
    return inst.write('SOURce:POWer %f' % Power)

def set_extAttenuation(Extatt):
    # Set the external attenuation of the device. Note : Setting not stored during
    # scenario or 1-channel mode execution. Parameter : decimal = [0, 30] in dB
    return inst.write('SOURce:EXTATT %f' % Extatt)

## SET SCENARIO

def set_DateTime(Date, Hour):
    #Set the scenario start time as GPS time
    return inst.write('SOURce:SCENario:DATEtime %s %s' % (Date , Hour))

def set_position (LAT, LONG, ALT):
    # set the position to the generator
    return inst.write('SOURce:SCENario:POSition IMM, %f, %f, %f' % (LAT, LONG, ALT))

def set_ECEFpos(X, Y, Z):
    # Sets the ECEF position in X, Y, Z coordinates as the start position for the loaded scenario
    # or the current position if the scenario is Running. The X, Y, Z position is given in decimal meters
    return inst.write('SOURce:SCENario:ECEFPOSition IMM, %f, %f, %f' % X, Y, Z)

def set_duration (Start, Duration, Interval):
    # Turn on scenario observations. Start is the number of seconds from scenario start.
    # Duration is length of observations from start. Interval is the interval between the individual
    # observations in the resulting Rinex OBS file
    return inst.write('SOURce:SCENario:OBS %f, %f, %f' %(Start, tools.Tools.get_sec(Duration),Interval))

def set_noise(Noise):
    # set the noise simulation ON OFF
    return inst.write('SOURce:NOISE:CONTrol %s' % Noise)

def set_cno(CN0):
    # set the maximun carrier to noise density of the simulated signals
    return inst.write('SOURce:NOISE:CN0 %f' % CN0)

def set_propa(env, sky, obstruction, nlos):
    # Sets built-in propagation environment model. The scenario must be running
    # <URBAN SUBURBAN RURAL OPEN> [,<sky_limit>, <obstruction_limit>, <nlos_probability>]
    return inst.write('SOURce:SCENario:PROPenv %s %f %f %f' % env, sky, obstruction, nlos)

def set_speed(Speed):
    # sets the vehicle's speed over ground (WGS84 ellipsoid)
    # decimal 1D speed [0.00 to +20000.00] m/s
    return inst.write('SOURce:SCENario:SPEed imm, %f' %Speed)

def set_acceleration(acceleration):
    # Sets the 1D acceleration expressed in m/s2 when scenario is running. Parameter: decimal 1d
    # acceleratin [-981 to +981] m/s2, ie [-100G to +100g]
    return inst.write('SOURce:SCENario:ACCeleration IMM, %f' % acceleration)

def set_heading(Heading):
    # sets the vehicule true heading. the heading is expressed in clockwise direction
    # from the true north representing 0 degrees, increasing to 359.999 degrees
    return inst.write('SOURce:SCENario:HEADing imm, %f' % Heading)

def set_antenna(antenna):
    #set the antenna model for the current scenario
    # model can be : Zero model, Helix, Patch, Cardioid
    return inst.write('SOURce:SCENario:ANTennamodel %s' % antenna)

def set_tropo(tropo):
    # set the tropospheric model for the current scenario
    # model can be : Saastamoinen, black, Goad&Goodman, Stanag
    return inst.write('SOURce:SCENario:TROPOmodel %s' %tropo)

def set_iono(iono):
    # Select the ionosperic model to be used in the current scenario. Permitted values are ON
    # and OFF
    return inst.write('SOURce:SCENario:IONOmodel %s' % iono)

def set_keepAlt(keepalt):
    # sets the altitude model setting for the current scenario. Default setting is ON.
    # When the model is active, the units will compensate for the altitude change resulting
    # from the difference between the ENU plane and the ellipsoid model of the earth.
    return inst.write('SOURce:SCENario:KEEPALTitude %s' % keepalt)

def set_rateHeadind(rateheading):
    #set th heading change rate. Rate is expressed as degrees per second.
    return inst.write('SOURce:SCENario:RATEHEading IMM, %f' % rateheading)

def set_turnRate(turnrate):
    # set the rate of turning. Rate is expressed as degrees per second.
    return inst.write('SOURce:SCENario:TURNRATE IMM, %f' % turnrate)

def set_turnradius(turnradius):
    # Sets the radius of turning. Radius is expressed in meters
    return inst.write('SOURce:SCENario:TURNRADIUS IMM %f' % turnradius)

# SCENARIO

def set_init(Date, Hour, LAT, LONG, ALT, Start, Duration, Interval):
    # set the configuration to the Spcetracom
    set_DateTime(Date, Hour)
    set_position(LAT, LONG, ALT)
    set_duration(Start, Duration, Interval)

def heading_compute(lat1, lat2, long1, long2):
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

#def scenario_reading():

    ## Time version FONCTIONNE

#    for section in range(len(scenario)-1):
#        section = section + 1
#        time.sleep(30)
#        if ((scenario[section][0] != '') or (scenario[section][1] != '') or (scenario[section][2] != '' )):
#            print(float(scenario[section][0]), float(scenario[section][1]), float(scenario[section][2]))
#            set_position(float(scenario[section][0]), float(scenario[section][1]), float(scenario[section][2]))
#        if scenario[section][6] != '':
#            set_acceleration(float(scenario[section][6]))
#        if scenario[section][4] != '':
#            set_heading(float(scenario[section][4]))
#        if scenario[section][5] != '':
#            set_speed(float(scenario[section][5]))
#        if scenario[section][7] != '':
#            set_rateHeadind(float(scenario[section][7]))
#        if scenario[section][8] != '':
#            set_turnRate(float(scenario[section][8]))
#        if scenario[section][9] != '':
#            set_turnradius(float(scenario[section][9]))


    ## position version FONCTIONNE

def scenario_reading():
    savefile = open('spectracom_data.nmea', 'w')
    for section in range(len(scenario)-2):
        section = section+1
        if (abs(float(scenario[section-1][0]))<=abs(float(scenario[section][0]))) and (abs(float(scenario[section-1][1]))<=abs(float(scenario[section][1]))):
            while (((get_current_pos()[0][1] <= (float(scenario[section][0])))) and
                   ((get_current_pos()[0][2] <= (float(scenario[section][1]))))):
                set_heading(heading_compute(float(scenario[section-1][0]),float(scenario[section][0]),
                                            float(scenario[section-1][1]),float(scenario[section][1])))
                    #get_current_pos()[0][1],float(scenario[section][0]),
                     #                       get_current_pos()[0][2],float(scenario[section][1])))
                set_speed(float(scenario[section][5]))
                data = inst.query('SOURce:SCENario:LOG?')
                savefile.write(data)
        if (abs(float(scenario[section-1][0]))<=abs(float(scenario[section][0]))) and (abs(float(scenario[section-1][1]))>=abs(float(scenario[section][1]))):
            while (((get_current_pos()[0][1] <= (float(scenario[section][0])))) and
                   ((get_current_pos()[0][2] >= (float(scenario[section][1]))))):
                set_heading(heading_compute(float(scenario[section-1][0]),float(scenario[section][0]),
                                            float(scenario[section-1][1]),float(scenario[section][1])))
                    #get_current_pos()[0][1],float(scenario[section][0]),
                     #                       get_current_pos()[0][2],float(scenario[section][1])))
                set_speed(float(scenario[section][5]))
                data = inst.query('SOURce:SCENario:LOG?')
                savefile.write(data)
        if (abs(float(scenario[section-1][0]))>= abs(float(scenario[section][0]))) and (abs((float(scenario[section-1][1])))>=abs(float(scenario[section][1]))):
            while (((get_current_pos()[0][1] >= (float(scenario[section][0])))) and
                   ((get_current_pos()[0][2] >= (float(scenario[section][1]))))):
                set_heading(heading_compute(float(scenario[section-1][0]),float(scenario[section][0]),
                                            float(scenario[section-1][1]),float(scenario[section][1])))
                    #get_current_pos()[0][1],float(scenario[section][0]),
                     #                       get_current_pos()[0][2],float(scenario[section][1])))
                set_speed(float(scenario[section][5]))
                data = inst.query('SOURce:SCENario:LOG?')
                savefile.write(data)
        if (abs(float(scenario[section-1][0]))>=abs(float(scenario[section][0]))) and (abs(float(scenario[section-1][1]))<=abs(float(scenario[section][1]))):
            while (((get_current_pos()[0][1] >= (float(scenario[section][0])))) and
                   ((get_current_pos()[0][2] <= (float(scenario[section][1]))))):
                set_heading(heading_compute(float(scenario[section-1][0]),float(scenario[section][0]),
                                            float(scenario[section-1][1]),float(scenario[section][1])))
                set_speed(float(scenario[section][5]))
                data = inst.query('SOURce:SCENario:LOG?')
                savefile.write(data)
    savefile.close()

# CONTROL

def launch():
    # Launch the scenario charged previously
    inst.write('SOURce:SCENario:CONTrol start')
    return('running')

def stop():
    # Stop the scenario from running
    return inst.write('SOURce:SCENario:CONTrol stop')

# GET DATA

def get_data(Duration):
    # take the nmea data for the duration of the scenario
    # sent by the spectracom and print them into the file
    savefile = open('spectracom_data.nmea', 'w')
    duree = tools.Tools.get_sec(Duration)
    i= 0
    while i <= duree :
        data = inst.query('SOURce:SCENario:LOG?')
        savefile.write(data)
        time.sleep(0.8)
        i = i+1
        print(i)
    savefile.close()
    return savefile

def get_current_pos():
    savefile = open('current_pos.txt', 'w')
    data = inst.query('SOURce:SCENario:LOG?')
    savefile.write(data)
    savefile.close()
    pos = (tools.data('current_pos.txt'))
    return pos

#print(get_current_pos())
#print(inst.query('SOURce:SCENario:LOG?'))

#done = tools.data('spectracom_data.nmeaprint(done)