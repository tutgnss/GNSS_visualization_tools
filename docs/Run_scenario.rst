================
Run the scenario
================

Choose your scenario
--------------------

Once you have create your own scenario, or if you want to run a pre-defined scenario, in the
main file fill the argument of ``tools.read_scen()`` with the name of your scenario like this
for example::

        scenario = tools.read_scen('data/scenariotest/test_2.ini')

Ublox initialisation
--------------------

There is different steps to configure the receiver(s):

- First of all, fill the COM port like this::

        ubloxcnx = Ublox(com='COM6')

- Then you have to choose which reset you want to make between **Cold RST**, **Warm RST** or **Hot RST**, like this::

            ubloxcnx.reset(command='Cold RST')

- Then you have to enable and disable which message you want or don't want to receive from the receiver, you can:

    enable:
            - ephemerides message thanks to **'EPH'**
            - ionospheric messages thanks to **'HUI'**
            - pseudo-range messages thanks to **'RAW'**
            - if you want all the UBX data just put **'UBX'**
            - position messages thanks to **'GGA'**
            - if you want all the NMEA data just put **'NMEA'**

    disable:
            - all NMEA message thanks to **'NMEA'**
            - all UBX message thanks to **'UBX'**

Here is an example of how to enable/disable message::

        ubloxcnx.enable(command='NMEA')
        ubloxcnx.disable(command='UBX')

.. note:: If you don't want to get any UBX message, please comment the following lines::
            thread_3 = AcquireData(3)
            thread_3.start()

Spectracom initialisation
-------------------------

To make the connexion with the Spectracom, you need to fill the argument of ``Spectracom()``, like this for example::

        spectracomcnx = Spectracom('USB0::0x14EB::0x0060::200448::INSTR')

