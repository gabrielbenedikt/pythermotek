#!/usr/bin/env python3

import serial

class T255P:
    def __init__(self, port):
        
        self.ERRCODES =         {0: 'No Error',
                                 1: 'Checksum Error',
                                 2: 'Bad Command',
                                 3: 'Out of Bound Qualifier'}
        
        self.MODESTATUS =       {0: 'Auto Start',
                                 1: 'Stand By',
                                 2: 'Chiller Run',
                                 3: 'Safety Default'}
        self.ALARMSTATUS =      {0: 'No Alarms',
                                 1: 'Alarm ON'}
        self.DRYERSTATUS =      {0: 'Dryer OFF',
                                 1: 'Dryer ON'}
        self.CHILLERSTATUS =    {0: 'Chiller OFF',
                                 1: 'Chiller ON'}
        
        self.dev = None
        self.port = port
        self.open()
        
    def set_port(self, port):
        self.port = port
        
    def get_port(self):
        return self.port
    
    def read(self):
        line = bytearray()
        eol = b'\r'
        while True:
            c = self.dev.read(1)
            if c:
                line += c
                if c == eol:
                    break
        return line.decode()
    
    def open(self):
        self.dev = serial.Serial(self.port)
    
    def close(self):
        self.dev.close()
        
    def build_msg(self, text):
        prefix = b'.' 
        
        if type(text) == type('string'):
            msg = prefix + text.encode()
        else:
            msg = prefix + text
            
        CS = b'%02X' % (sum(msg) & 0xFF)
        
        ret = msg + CS + b'\r'
        #print(ret, '\t', ''.join('{0:02x} '.format(x) for x in ret))
        return ret
    
    def check_response(self, ret):
        #check checksum
        retmsg = ret[:-3].encode()
        retcs  = ret[-3:-1].encode()
        expectcs = b'%02X' % (sum(retmsg) & 0xFF)
        #print(ret.encode(), '\t', ''.join('{0:02x} '.format(x) for x in ret.encode()), '\t', retcs, '\t', expectcs)
        if not (retcs == expectcs):
            print("ERR: Response checksum wrong")
            return -1
        else:
            #check errorcodes
            if (ret[2]=="0"):
                return 0
            elif (ret[1]=="G") and (ret[2]=="3"): #mode select response quirk
                return 0
            elif (ret[1]=="O") and (ret[2]=="3"): #mode select response quirk
                return 0
            else:
                try:
                    print("ERR: " + self.ERRCODES[int(ret[2])])
                except Exception as e:
                    print("ERR: Unknown error code")
                return -1

    def set_mode(self, on: bool):
        ''' set chiller mode to "stand by" (on==False) or "Run Mode" (on==True) 
            Note: Trying to set mode to current mode will produce an "out ouf bounds" error '''
        msg = self.build_msg("G1" if on else "G0")
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return ret[3]
    
    def get_memory(self):
        ''' returns set point temperature in deg C, max power setting '''
        msg = self.build_msg('H0')
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[4:8])/10, ret[9:12]
    
    def get_manifold_temp(self):
        ''' returns manifold temperature in deg C '''
        msg = self.build_msg('I')
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[3:8])/100
    
    def get_alarm_state(self):
        ''' get state of 
            float switch
            high alarm
            lw alarm
            sensor alarm
            eeprom fail
            watch dog
            0 indicates normal condition
            1 indicates alarm'''
        msg = self.build_msg('J')
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[3]), int(ret[4]), int(ret[5]), int(ret[6]), int(ret[7]), int(ret[8])
    
    def set_stabilized_temp(self, t: float):
        ''' set set point temperature. 0.1deg C precision '''
        msg = self.build_msg('M{0:+4d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[3:7])/10
    
    def get_stabilized_temp(self):
        ''' get set point temperature. 0.1deg C precision '''
        t, _ = self.get_memory()
        return t
    
    def set_external_temp_sense_mode(self, internal: bool):
        ''' use internal (internal==True) or external (internal==False) temperature sensor 
            Note: Trying to set mode to current mode will produce an "out ouf bounds" error '''
        msg = self.build_msg('O0' if internal else 'O1')
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[3])
    
    def get_watchdog_status(self):
        ''' returns
            mode status
            alarm status
            chiller status
            dryer status'''
        msg = self.build_msg('U')
        self.dev.write(msg)
        ret = self.read()
        if not (self.check_response(ret)):
            return int(ret[3]), int(ret[4]), int(ret[5]), int(ret[6])

    def send_custom_msg(self, msg):
        msg = self.build_msg(msg)
        self.dev.write(msg)
        ret = self.read()
        return ret
