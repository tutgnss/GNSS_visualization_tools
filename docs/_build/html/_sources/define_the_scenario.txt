===================
Define the scenario
===================

Create a new .ini file and use this template::

        [START]
        LAT:
        LONG:
        ALT:
        Duration:
        Heading:
        Speed:
        Acceleration:
        Rateheading:
        Turnrate:
        Turnradius:
        Cn0:
        Propagation:
        Antenna:
        Tropo:
        Iono:
        keepalt:
        ECEFpos:
        Multipath:
        SpeedOverGround:
        Verticalspeed:
        Enuvel:
        Ecefvel:
        VerticalAcceleration:
        ENUAccel:
        ECEFAccel:
        PRYattitude:
        DPRYattitude:
        Kepler:
        [SECTION 1]
        LAT:
        LONG:
        ALT:
        Duration:
        Heading:
        Speed:
        Acceleration:
        Rateheading:
        Turnrate:
        Turnradius:
        Cn0:
        Propagation:
        Antenna:
        Tropo:
        Iono:
        keepalt:
        signaltype:
        ECEFpos:
        Multipath:
        SpeedOverGround:
        Verticalspeed:
        Enuvel:
        Ecefvel:
        VerticalAcceleration:
        ENUAccel:
        ECEFAccel:
        PRYattitude:
        DPRYattitude:
        Kepler:
        [END]

In the [START] section, just fill the Latitude, Longitude and altitude information.

Copy/Paste the number of [SECTION] needed.

In each section, put all the parameters you want to set from (section-1) to the section, if not given, default
parameters will be set.
Pay attention:

    - fill LAT, LONG, ALT or Duration, Heading not both!
    - fill LAT, LONG, ALT or ECEFpos not both
    - fill ENUvel or ECEFvel or Speed or SpeedOverGround not four of them
    - fill ENUaccel or ECEFaccel or Acceleration not three of them
    - fill PRYattitue or DPRYattitude not both

