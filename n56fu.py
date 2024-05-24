#!/usr/bin/python3

#   n56fu.py

#   Module for getting data from the Precision Gold N56FU USB multimeter.
#   (and possible rebadges)

#   Note: Made without information on the data, by analysing serial messages.
#   Use or modify freely.

#   Brian Swatton, May 2024


import sys, os, time

__version__ = '1.0 b2'
__date__ = '24/05/24 22:10'


try:
    import serial
except ImportError as impErr:
    print(f"[Error]: Failed to import - {impErr.args[0]}")
    print('\n !  This program requires the python module "pyserial"')
    print(' !  to be installed in your python environment.\n')
    sys.exit(1)


class N56FU(serial.Serial):
    """Class for connecting to an N56FU USB multimeter on a given port"""
    mode0 = {32:'auto', 16:"dc", 8:'ac', 4:'rel', 2:'hold'}
    mode1 = {32:'max', 16:'min'}
    mult = {128:('u',1e-6), 64:('m',1e-3), 32:('k',1e3), 16:('M',1e6), 2:('%',1), 0:('',1)}
    units = {128:'V', 64:"A", 32:'R', 16:'hFE', 8:'Hz', 4:'F', 2:'tC', 1:'tF' , 0:''}
    function = {128:'Voltage',
                64:"Current",
                32:'Resistance',
                16:'hFE',
                8:'Frequency',
                4:'Capacitance',
                2:'Centigrade',
                1:'Fahrenheit',
                0:'Duty Cyle'}


    def __init__(self, port):
        device = f'/dev/{port}'
        if not os.path.exists(device):
            print(f'\n! Port \'{port}\' does not exist !\n')
            sys.exit(2)
        super().__init__()
        self.port = device
        self.baudrate = 2400
        self.timeout = 2
        self.open()


    def get_raw(self, flush=True):
        """Get a raw frame, usually flushing the buffer first to get current data."""
        if flush:
            self.reset_input_buffer()

        data = self.get_frame()
        if data[0] == '!':
            return data

        if len(data) != 14:
            data = self.get_frame()

        if len(data) != 14:
            data = '!length'
        return data


    def get_frame(self):
        """Reads to the next end of frame"""
        data = bytes()
        crlf = False
        while not crlf:
            data += bytes(self.read(1))
            if len(data) == 0:
                data = '!timeout'
                break
            if len(data) > 1:
                crlf = data[-2:] == b'\r\n'
        return data


    def get_reading(self, flush=True):
        """Returns a humanized reading string"""
        state = self.get_state()

        if type(state) is str:
            # It's an error
            return state

        reading = f"{state['display']} {state['mult']}{state['units']}"
        for mode in state['modes']:
            reading += f' {mode}'
        return reading


    def _display(self, raw):
        """Returns the value displayed on the meter from a raw frame, as a string"""
        data = raw[:8].decode()
        digits = data[:5]
        dp = int(data[6])
        dp = 3 if dp == 4 else dp   # for some reason!
        status = raw[7:-2]
        reading = digits if dp == 0 else f'{digits[:dp+1]}.{digits[dp+1:]}'
        return reading


    def get_state(self, flush=True):
        """Returns a dictionary of a decoded frame or '!timeout' string"""
        raw = self.get_raw(flush)
        if raw[0] == '!':
            return raw
        status = raw[7:-2]
        state = {}
        state['display'] = self._display(raw)
        state['function'] = N56FU.function[status[3]]
        state['modes'] = []
        for mode in N56FU.mode0:
            if status[0] & mode == mode:
                state['modes'].append(N56FU.mode0[mode])

        for mode in N56FU.mode1:
            if status[1] & mode == mode:
                state['modes'].append(N56FU.mode1[mode])

        if status[1] == 2:  # pesky nano multiplier in mode1 byte
            state['mult'] = 'n'
            factor = 1e-9
        else:
            state['mult'] = N56FU.mult[status[2]][0]
            factor = N56FU.mult[status[2]][1]

        if state['display'][1] == '?':
            state['value'] = 0
        else:
            state['value'] = float(state['display']) * factor

        state['units'] = N56FU.units[status[3]]
        state['bargraph'] = status[4]

        return state

# End of N56FU class


##################################################################
# Main program

if __name__ == '__main__':
    print(f'\n  Module: n56fu v{__version__}, {__date__}  ~ Brian Swatton\n')
    print('  For reading the N56FU USB multimeter.')
    print('  Intended for import, but have some readings...\n')

    m = N56FU('ttyUSB0')
    while True:
        print(m.get_reading())
