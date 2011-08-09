#!/usr/bin/env python

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




import sys
import threading
import thread
import time
from output import AudioOutput
from input import InputFile


class Player(object):
    """ The main player class. This is generally the class you would
    instance in order to provide playback.

    A general playback loop would be to create a Player, call load_file(file)
    and then finally play().

    """


    def __init__(self):


        self.status = {'cont_playing' : threading.Event(), # check if playing
                       'finished' : threading.Event(),
                       'playing' : threading.Event(), # stop or play
                       'time'    : 0}
        
    def load_file(self, file):
        """ Attempts to load the file specified using the InputFile class.
        Will autodetect the file format using the file name.

        Also opens up the AudioOutput device with the sample
        rate and endianness reported by the file.
        """
        try:
            self.file = InputFile(file)
        except:
            raise
        self.output = AudioOutput(endian = self.file.endian, output = 'oss',
                                  rate = self.file.rate)
        self.output.open()

    def toggle_pause(self):
        """ Pauses and unpauses playback """

        if self.status['cont_playing'].isSet():
            self.status['cont_playing'].clear()
        else:
            self.status['cont_playing'].set()


    def pretty_pos(self):
        """ Returns a string representing the current playback
        time as mm:ss """
        pos = self.file.position
        min = int(pos) / 60
        sec = int(pos) - min*60
        tin = "%02d:%02d" % (min,sec)
        
        pos = self.file.length
        min = int(pos) / 60
        sec = int(pos) - min*60
        tot = "%02d:%02d" % (min,sec)

        return (tin,tot)

    def pause(self):
        """ Pauses. If the playback is paused, does nothing"""
        self.status['cont_playing'].clear()

    def unpause(self):
        """ Unpause. If the playback is unpaused, does nothing """
        self.status['cont_playing'].set()

    def seek(self):
        """ Not yet implemented """
        pass

    def stop(self):
        """ Stops the playback. Will stop the playing thread and close the audio device """
        self.status['playing'].clear()

    def play(self, wait_start = False, wait_finish = False):

        """ Plays the file loaded with load_file. If the wait_start
        flag is set, the function waits until the playback thread is
        actually playing the file. If wait_finish is set, the function
        will not return until the playback is finished. """
        self.thread = thread.start_new_thread(self.playth, ())
        if wait_finish:
            wait_start = True
        if wait_start:
            self.status['playing'].wait()

        if wait_finish:
            self.status['finished'].wait()
            
        
    def playth(self):
        """ Internal playback thread. """

        self.status['finished'].clear()
        self.status['cont_playing'].set()
        self.status['playing'].set()
        
        
        while self.status['playing'].isSet():
            self.status['cont_playing'].wait() # wait until playing
            
            (buff, bytes) = self.file.read()
            if bytes:
                self.output.write(buff, bytes)
            else:
                break
        self.output.close()
        
        self.status['cont_playing'].set()
        self.status['playing'].clear()
        self.status['finished'].set()

        thread.exit()    
        

if __name__ == '__main__':

    
    
    pl = Player()



    for x in sys.argv[1:]:
        print x
        pl.load_file(x)
        pl.play(wait_start = True)
        while pl.status['playing'].isSet():

            print pl.file.position, "s in of ",pl.file.length,"s"

            time.sleep(0.5)
            
            
	
    
            
        
    


    


