===================
Define the scenario
===================

There is already some scenario define in data/scenariotest but you can also define your own
scenario

Scenarios already define
------------------------

6 scenarios have been defined for you to test your devices:

        test_1:
This is the static case, for a minute, data are taken from your simulator and/or your
receiver(s).

        test_2:
This is the temporal square test, the simulator run a path representing a square at constant speed
, each section last a minute. It basically test if the receiver(s) is well responding to a brutal
change of direction.

        test_3:
This is the temporal circle test, the simulator run a path representing a circle at constant
speed, during 2 minutes.

        test_4:
This is the test of constant acceleration in straight line.

        test_5:
This is the sensitivity test, staying static, the C/N0 is increased. The goal is to see until
which C/N0 it is still possible to receive something

        test_6:
This is the Free to Urban space test. The goal is to test if the receiver can keep its
reliability when passing from a free space to a urban space.

Create your scenario
--------------------

If you want to create your own scenario, follow the following step:

    1st step:
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

.. note:: In the [START] section, just fill the Latitude, Longitude and altitude information of your
departure position.

    2nd step:
Copy/Paste the number of [SECTION] needed.
.. image:: images/scenario.png

In each section, put all the parameters you want to set from (section-1) to the section, if not given, default
parameters will be set.
Pay attention:

    - fill LAT, LONG, ALT or Duration, Heading not both!
    - fill LAT, LONG, ALT or ECEFpos not both
    - fill ENUvel or ECEFvel or Speed or SpeedOverGround not four of them
    - fill ENUaccel or ECEFaccel or Acceleration not three of them
    - fill PRYattitue or DPRYattitude not both

