#    PyAudioPlay - A python audio player library
#    Copyright (C) 2004 Yann Ramin
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License (in file COPYING) for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#


import ao

class AudioOutput(object):
    def __init__(self, endian = 1, rate = 44100, bits = 16, output = 'oss'):
        self.bits = bits
        
        if output is 'oss':
            self.output = 3
        elif output is 'alsa':
            self.output = 2

        self.byte_format = endian
        self.rate = rate
        
        

    def open(self):
        self.driver = ao.AudioDevice(self.output, byte_format = self.byte_format,  bits = self.bits, rate = self.rate)

    def close(self):
        del self.driver
        
    def write(self, buff, bytes):
        self.driver.play(buff, bytes)


