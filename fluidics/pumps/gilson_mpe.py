#!/usr/bin/env python
# 
# Interface for Gilson MINIPULS Evolution V1.02
# Tom Robbins 2016
# thomas.robbins@cruk.cam.ac.uk

import serial

class APump():

    RESPONSE_OK     = 'OK\r'
    #RESPONSE_PRIME     = u'\u2014.\u2014\r'
    RESPONSE_PRIME  = '--.--\r'

    PRIME_SPEED     = 60.0 # RPM

    def __init__(self, parameters=None):
        self.com_port = parameters.get("pump_com_port", 3)
        self.pump_ID = parameters.get("pump_ID", 30)
        self.verbose = parameters.get("verbose", True)
        self.simulate = parameters.get("simulate_pump", True)
        self.serial_verbose = parameters.get("serial_verbose", False)
        self.flip_flow_direction = parameters.get("flip_flow_direction", False)

        self.serial = serial.Serial(port=self.com_port, baudrate=19200,
                                    parity=serial.PARITY_EVEN,
                                    bytesize=serial.SEVENBITS,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=0.1)

        self.identification = self.getIdentification()

    
    def ask(self,query):
        print "Telling pump:", query
        self.serial.write(query)
        response = self.serial.readline()
        print "Pump said:", response
        return response
    
    def getIdentification(self):
        return self.ask("%\r")[:-1]

    def getStatus(self):
        raw_status = self.ask("R\r")
        return ["Stopped" if raw_status[0] == " " else "Flowing", 
                float(self.PRIME_SPEED if raw_status[1:] == self.RESPONSE_PRIME else raw_status[1:-1]),
                {'+':'Forward','-':'Reverse', ' ':''}[raw_status[0]]]

    def setSpeed(self, speed):
        return self.ask("S%.0f\r"%(speed * 100)) == self.RESPONSE_OK

    def startFlow(self, speed, direction):
        if self.setSpeed(speed):
            self.initialisePump()
            return self.ask("K{}\r".format('>' if direction == "Forward" else '<')) == self.RESPONSE_OK
        else:
            return False

    def stopFlow(self):
        self.ask("KH\r")

    def initialisePump(self, force=False):
        if force or self.getStatus()[0] == "Stopped":    
            return self.ask("KG\r") == self.RESPONSE_OK

    def close(self):
        self.stopFlow()
        self.serial.close()

