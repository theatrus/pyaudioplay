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


from exceptions import Exception

class ByteSwapError(Exception):
    pass


def bytewwap(data, width):
    slen = len(data)

    if width < 16:
        raise ByteSwapError, "Width is not > 16 bits. You can't swap bytes with themselves :)"
    if width % 8:
        raise ByteSwapError, "Width is not a multiple of 8 bits"
    if width > len:
        raise ByteSwapError, "Data is too short to be swapped"
    if slen % (width/8):
        raise ByteSwapError,"Data not in " +`width` + " bit segments"

    data = list(data)


    newdata = ""
    for i in range(0,slen/(width/8)):

        tdata = ""
        for x in range(0,width/8):
            tdata = data.pop(0) + tdata
        newdata = newdata + tdata



    return str(newdata)
            



    
