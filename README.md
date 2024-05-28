# N56FU
Python module for reading the N56FU multimeter

    n56fu   v1.0 b4  (beta)

    Python module for reading data from the
    Precision Gold N56FU mulitmeter.

    Linux only currently

    By Brian Swatton, May 2024


Please Note:
No data was available to write this, it was reverse engineered
from analysing message frames.  I'm not aware of errors, but
they could exist still.

I may not code very "pythonically" sometimes. I'm just grateful
not to be poking bytes into REM statements.


### Module Usage

If you run the file as a main program, it will just spit out
readings if/when it can. Not really the intended use, but handy
for checking setups.  The meter will need to have USB selected.

I would import with the line:

    from n56fu import N56FU

It contains just one class, 'N56FU', which inherits from
pyserial's serial.Serial() class. It has three methods for the
module user

	find_ports()
	get_reading()
	get_state()

Pass N56FU the port name, probably 'ttyUSB0', and it will return an
open a connection to it if it can.

You can get a list of ports with an N56FU meter attached with:

	ports = N56FU.find_ports()

(The meter will need to be on, and in USB mode, to be found.)

You can then:

    meter = N56FU(ports[0])

    reading = meter.get_reading()

to have a human readable string returned, or

    meterstate = meter.get_state()

will give a dictionary back with all the information in a more
programmer friendly form:

    display     string reflecting the main digit display
    function    string, 'Voltage', 'Current' etc.
    modes       list of strings of modes, ie 'ac' 'hold' etc.
    mult        string of reading mulitplier, ie 'm', 'k' etc.
    value       float of the value without mulitplier, in units
    units       string, 'V', 'A', 'Hz' etc
    bargraph    int for bargraph (not exactly tested yet!)


#### flush=True

By default, these methods will flush the buffer before reading a
fresh frame, to ensure an up to the second measurement. This suits
my usual use case, but may not be desirable for all applications.

To instead just get the next from the queue, set the parameter
flush=False. ie

    nextstate = meter.get_state(flush=False)

or just

    nextstate = meter.get_state(False)


#### Multiple Meters


It should be possible to open multiple connections to meters
on different ports, but this as yet untested.  ie

    m1 = N56FU('ttyUSb0')
    m2 = N56FU('ttyUSb1')


Collaboration


I've really just put this module here to make it available for
use, as I saw a number of posts looking for something like it
when researching the meter.

If you have something you'd like to contribute to the project, I
am open to suggestion for improvement. I am a total noob with
online software collaboration. I have been using git as a solo
coder for a few years though. I've not got on well with getting
ssh working again with github since a drive crash though. 

I've been coding since 1979, for work and hobby (electronics,
business admin). Usually programs for just me to use, though this
is changing.

