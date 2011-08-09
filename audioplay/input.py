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

support = {}

try:
    import aifc
    aifc._skiplist = aifc._skiplist + tuple(['ID3 '])
    # Skip ID3 tags. Common with iTunes AIFFs
    support['aiff'] = True
except:
    support['aiff'] = False

try:
    import mad
    support['mp3'] = True
except:
    support['mp3'] = False


try:
    import ogg.vorbis
    support['vorbis'] = True
except:
    support['vorbis'] = False

import re
import wave

class InputFile(object):
    def __init__(self, file):
        self.file = file
        self.rate = 44100 # default
        self.length = 0 # always expressed in seconds
        self.position = 0
        ext = file.split('.')[-1]
        self.endian = 1
        if file.rfind('.mp3') is not -1 and support['mp3'] is True:
            self.stream = mad.MadFile(file)
            self.read = self.read_mad
            self.endian = 1
            rate = self.stream.samplerate()
            vrates = [96000,44100,48000,32000,22050,16000,8000]
            if rate not in vrates:
                rate = 44100
            self.rate = rate

            self.length = float(self.stream.total_time()) / 1000.0
        elif file.rfind('.ogg') is not -1 and support['vorbis'] is True:
            self.stream = ogg.vorbis.VorbisFile(file)
            self.read = self.read_ogg
            self.endian = 1
            self.rate = self.stream.info().rate
            self.length = float(self.stream.time_total(-1)) / 1.0
        elif file.rfind('.aif') is not -1 and support['aiff'] is True:
            self.stream = aifc.open(file, 'r')
            self.read = self.read_pcm
            self.endian = 2
            self.rate = self.stream.getframerate()
            self.length = float(self.stream.getnframes()) / float(self.rate)
        elif file.rfind('.wav') is not -1:
            self.stream = wave.open(file, 'r')
            self.read = self.read_pcm
            self.endian = 1
            self.rate = self.stream.getframerate()
            self.length = float(self.stream.getnframes()) / float(self.rate)
        else:
            raise
    def read_mad(self):
        (buff) = self.stream.read()
        self.position = float(self.stream.current_time()) / 1000.0
        if buff is None:
            return (buff, 0)
        else :
            return (buff, len(buff))
    def read_ogg(self):
        (buff,a,b) = self.stream.read(4096)
        self.position = self.stream.time_tell()
        if buff is None:
            return (buff, 0)
        else :
            return (buff, a)

        
    def read_pcm(self):
        (buff) = self.stream.readframes(1024)
        self.position = float(self.stream.tell()) / float(self.rate)
        
        if buff is None:
            return (buff, 0)
        else:
            return (buff, len(buff))
