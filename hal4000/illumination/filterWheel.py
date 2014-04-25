#!/usr/bin/python
#
## @file
#
# This file contains hardware classes that interface with filter wheels.
#
# Hazen 04/14
#

from PyQt4 import QtCore

import illumination.hardwareModule as hardwareModule


## ThorlabsFW102C
#
# Filter wheel class that interfaces with a Thorlabs FW102C filter wheel.
#
class ThorlabsFW102C(hardwareModule.BufferedAmplitudeModulation):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):
        hardwareModule.BufferedAmplitudeModulation.__init__(self, parameters, parent)

        import sc_hardware.thorlabs.FW102C as FW102C
        self.filter_wheel = FW102C.FW102C(parameters.port)
        if not (self.filter_wheel.getStatus()):
            self.working = False

    ## cleanup
    #
    def cleanup(self):
        hardwareModule.BufferedAmplitudeModulation.cleanup(self)
        self.filter_wheel.shutDown()

    ## deviceSetAmplitude
    #
    # @param channel The channel.
    # @param amplitude The channel amplitude.
    #
    def deviceSetAmplitude(self, channel, amplitude):
        self.device_mutex.lock()
        self.filter_wheel.setPosition(amplitude)
        self.device_mutex.unlock()


## NoneFilterWheel
#
# Filter wheel emulator.
#
class NoneFilterWheel(hardwareModule.AmplitudeModulation):

    ## __init__
    #
    # @param parameters A XML object containing initial parameters.
    # @param parent The PyQt parent of this object.
    #
    def __init__(self, parameters, parent):
        hardwareModule.AmplitudeModulation.__init__(self, parameters, parent)


#
# The MIT License
#
# Copyright (c) 2014 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#