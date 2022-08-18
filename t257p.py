#!/usr/bin/env python3

import serial

class T257P:
    def __init__(self, port):
        self.dev = None
        self.port = port
        self.open()
        self.SENSORS = ["Supply Temp", "Return Temp", "External RTD", "External termistor"]
        
        self.ERR = {0: "Command OK",
                    1: "Checksum Error",
                    2: "Bad Command Number (Command Not used)",
                    3: "Parameter/Data Out of Bound",
                    4: "Message Length Error",
                    5: "Sensor/Feature not Configured or Used"}
        self.CTRLSTAT = {0: "Auto-Start",
                         1: "Standby",
                         2: "Run",
                         3: "Safety",
                         4: "Test"}
        self.PUMPSTAT = {0: "Pump OFF",
                         1: "Pump ON"}
        self.ALARMSTAT = {0: "No Alarm",
                          1: "Alarm Present"}
        self.WARNSTAT = {0: "No Warning",
                          1: "Warning Present"}
        self.W0 = {0: "No Alarm",
                   1: "Low Process Flow Warning",
                   2: "Process Fluid Level Warning",
                   4: "Switch to Supply Temp as Control Temp Warning",
                   8: "Reserved (Not used)"}
        self.W1 = {0: "No Alarm",
                   1: "High Control Temp Warning",
                   2: "Low Control Temp Warning",
                   4: "High Ambient Temp Warning",
                   8: "Low Ambient Temp Warning"}
        self.W2 = {0: "No Alarm",
                   1: "Reserved (Not used)",
                   2: "Reserved (Not used)",
                   4: "Reserved (Not used)",
                   8: "Reserved (Not used)"}
        self.W3 = {0: "No Alarm",
                   1: "Reserved (Not used)",
                   2: "Reserved (Not used)",
                   4: "Reserved (Not used)",
                   8: "Reserved (Not used)"}
        
        self.A0 = {0: "No Alarm",
                   1: "Ambient Temperature Sensor Alarm",
                   2: "High Control Temperature Alarm",
                   4: "PT7 High Temperature Alarm",
                   8: "Low Control Temperature Alarm"}
        self.A1 = {0: "No Alarm",
                   1: "Supply Temperature Sensor Alarm (Latched)",
                   2: "External RTD Sensor Alarm",
                   4: "High Ambient Temp Warning",
                   8: "External Thermistor Sensor Alarm"}
        self.A2 = {0: "No Alarm",
                   1: "Low Coolant Level Alarm (Latched)",
                   2: "Low Process Flow Alarm",
                   4: "Low Plant Flow Alarm",
                   8: "Current Sensor 1 Alarm"}
        self.A3 = {0: "No Alarm",
                   1: "PT7 Low Temperature Alarm",
                   2: "High Ambient Temperature Alarm",
                   4: "Low Ambient Temperature Alarm",
                   8: "External Connector Not Installed"}
        self.A4 = {0: "No Alarm",
                   1: "Default High Temperature Alarm",
                   2: "Default Low Temperature Alarm",
                   4: "No Process Flow Alarm",
                   8: "Fan Failure Alarm"}
        self.A5 = {0: "No Alarm",
                   1: "Current Sensor 2 Alarm",
                   2: "Internal 2.5V Reference Alarm",
                   4: "Internal 5V Reference Alarm",
                   8: "System Error Alarm (Global)"}
        
        self.B0 = {0: "No Alarm",
                   1: "Reserved (Not Used)",
                   2: "Reserved (Not Used)",
                   4: "Reserved (Not Used)",
                   8: "Reserved (Not Used)"}
        self.B1 = {0: "No Alarm",
                   1: "ADC System Error Alarm",
                   2: "I2C System Error Alarm",
                   4: "EEPROM System Error Alarm",
                   8: "Watchdog System Error Alarm"}
        self.B2 = {0: "No Alarm",
                   1: "Reserved (Not Used)",
                   2: "Reserved (Not Used)",
                   4: "Reserved (Not Used)",
                   8: "Reserved (Not Used)"}
        self.B3 = {0: "No Alarm",
                   1: "ADC Reset Error Alarm",
                   2: "ADC Calibration Error Alarm",
                   4: "ADC Conversion Error Alarm",
                   8: "Reserved (Not Used)"}
        self.B4 = {0: "No Alarm",
                   1: "IO Expender Acknowledge Error Alarm",
                   2: "PSA IO Expender Acknowoledge Alarm",
                   4: "RTC Acknowledge Error Alarm",
                   8: "Reserved (Not Used)"}
        self.B5 = {0: "No Alarm",
                   1: "I2C SCL Low Error Alarm",
                   2: "I2C SDA Low Error Alarm",
                   4: "EEPROM 1 (U201) Acknowledge Alarm",
                   8: "EEPROM 2 (U200) Acknowledge Alarm"}
        self.B6 = {0: "No Alarm",
                   1: "Reserved (Not Used)",
                   2: "Reserved (Not Used)",
                   4: "Reserved (Not Used)",
                   8: "Reserved (Not Used)"}
        self.B7 = {0: "No Alarm",
                   1: "EEPROM 1 (U201) Read Error Alarm",
                   2: "EEPROM 1 (U201) Write Error Alarm",
                   4: "EEPROM 2 (U200) Read Error Alarm",
                   8: "EEPROM 2 (U200) Write Error Alarm"}
        
        self.C0 = {0: "No Alarm",
                   1: "External RTD Sensor Open Alarm",
                   2: "External RTD Sensor Short Alarm",
                   4: "Return Temp Sensor Open Alarm",
                   8: "Return Temp Sensor Open Alarm"}
        self.C1 = {0: "No Alarm",
                   1: "Global Supply Temp Sensor Alarm",
                   2: "Supply Temp Sensor Locked Alarm",
                   4: "Supply Temp Sensor Open Alarm",
                   8: "Supply Temp Sensor Short Alarm"}
        self.C2 = {0: "No Alarm",
                   1: "Internal 2.5V Reference High Alarm",
                   2: "Internal 2.5V Reference Loe Alarm",
                   4: "nternal 5V Reference High Alarm",
                   8: "nternal 5V Reference Low Alarm"}
        self.C3 = {0: "No Alarm",
                   1: "External Therm. Sensor Open Alarm",
                   2: "External Therm. Sensor Short Alarm",
                   4: "Ambient Temp Sensor Open Alarm",
                   8: "Ambient Temp Sensor Short Alarm"}
        self.C4 = {0: "No Alarm",
                   1: "Reserved (Not Used)",
                   2: "Reserved (Not Used)",
                   4: "Reserved (Not Used)",
                   8: "Reserved (Not Used)"}
        self.C5 = {0: "No Alarm",
                   1: "Current Sensor 1 Open Alarm",
                   2: "Current Sensor 1 Short Alarm",
                   4: "Current Sensor 2 Open Alarm",
                   8: "Current Sensor 2 Short Alarm"}
        self.C6 = {0: "No Alarm",
                   1: "Rear Left Fan Noise Alarm",
                   2: "Rear Right Fan Noise Alarm",
                   4: "Front Left Fan Noise Alarm",
                   8: "Front Right Fan Noise Alarm"}
        self.C7 = {0: "No Alarm",
                   1: "Rear Left Fan Open Alarm",
                   2: "Rear Right Fan Open Alarm",
                   4: "Front Left Fan Open Alarm",
                   8: "Front Right Fan Open Alarm"}
        
        self.A = [self.A0, self.A1, self.A2, self.A3, self.A4, self.A5]
        self.W = [self.W0, self.W1, self.W2, self.W3]
        self.B = [self.B0, self.B1, self.B2, self.B3, self.B4, self.B5, self.B6, self.B7]
        self.C = [self.C0, self.C1, self.C2, self.C3, self.C4, self.C5, self.C6, self.C7]
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
        
    def build_msg(self, text, ID = 1):
        if ID < 1:
            print("ERR: device ID needs to be 1...32")
        elif ID > 32:
            print("ERR: device ID needs to be 1...32")
        else:
            bID = b'%02d' % ID
            
        prefix = b'.' + bID
        
        if type(text) == type('string'):
            msg = prefix + text.encode()
        else:
            msg = prefix + text
        CS = b'%02X' % (sum(msg) & 0xFF)
        return msg + CS + b'\r'
    
    def get_watchdog_status(self):
        ''' returns active control temperature sensor '''
        msg = self.build_msg('01WatchDog')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            cs_idx=int(ret[14])
            ps_idx=int(ret[15])
            as_idx=int(ret[16])
            ws_idx=int(ret[17])
            return ["Contro Status: " + self.CTRLSTAT[cs_idx], 
                    "Pump Status: " + self.PUMPSTAT[ps_idx], 
                    "Alarm Status: " + self.ALARMSTAT[as_idx], 
                    "Warning Status: " + self.WARNSTAT[ws_idx]]
        else:
            self.handle_error(ret[5])
            return None
    
    def get_control_sensor(self):
        ''' returns active control temperature sensor '''
        msg = self.build_msg('02rCtrlSen')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            sidx=int(ret[14])
            if (sidx >= 0) and (sidx < 3):
                return self.SENSORS[sidx]
            else:
                return None
        else:
            self.handle_error(ret[5])
            return None

    def get_set_t(self):
        ''' returns set temperature in degrees celsius '''
        msg = self.build_msg('03rSetTemp')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_supply_t(self):
        ''' returns reading of supply water temperature sensor in degrees celsius '''
        msg = self.build_msg('04rSupplyT')
        self.dev.write(msg)
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_ext_rtd_t(self):
        ''' returns reading of external RTD in degrees celsius '''
        msg = self.build_msg('05rExtRTD_')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_ext_termistor_t(self):
        ''' returns reading of external termistor in degrees celsius '''
        msg = self.build_msg('06rExtThrm')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_return_t(self):
        ''' returns reading of return water temperature sensor in degrees celsius '''
        msg = self.build_msg('07rReturnT')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_ambient_t(self):
        ''' returns reading of ambient temperature sensor in degrees celsius '''
        msg = self.build_msg('08rAmbTemp')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_process_flow(self):
        ''' returns flow in liters per minute '''
        msg = self.build_msg('09rProsFlo')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            fstr=ret[15:19]
            return float(fstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_tec1_current(self):
        ''' returns TEC1 current reading as ADC reading '''
        msg = self.build_msg('10rTECB1Cr')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            fstr=ret[15:19]
            return float(fstr)/1000
        else:
            self.handle_error(ret[5])
            return None
    
    def get_tec2_current(self):
        ''' returns TEC2 current reading as ADC reading '''
        msg = self.build_msg('11rTECB2Cr')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            fstr=ret[15:19]
            return float(fstr)/1000
        else:
            self.handle_error(ret[5])
            return None
    
    def set_extern_sensor_status(self, on: bool):
        ''' enables external sensor if on==True, disables otherwise '''
        msg = self.build_msg('12sExtSens1' if on else '12sExtSens0')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            reton=ret[14]
            return int(reton)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_te_drive_level(self):
        ''' desc '''
        msg = self.build_msg('13rTECDrLv')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            percent=ret[14:17]
            r=ret[18]
            mode = "Cooling" if r==b'C' else "Heating"
            return int(percent), mode
        else:
            self.handle_error(ret[5])
            return None
    
    #cmd 14 reserved
    
    def set_chiller_status(self, on: bool):
        ''' desc '''
        msg = self.build_msg('15sStatus_1' if on else '15sStatus_0')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            retstat=ret[14]
            return retstat
        else:
            self.handle_error(ret[5])
            return None
    
    def set_control_sensor(self, snum: int):
        ''' desc '''
        if snum < 0:
            print("ERR: sensor number needs to be 0...3")
            return None
        elif snum > 3 :
            print("ERR: sensor number needs to be 0...3")
            return None
        else:
            msg = self.build_msg('16sCtrlSen'+str(snum))
            self.dev.write(msg)
            ret = self.read()
            if ret[5] == '0':
                retsnum=ret[14]
                return int(retsnum)
            else:
                self.handle_error(ret[5])
                return None
    
    def set_control_temperature(self, t: float):
        ''' desc '''
        msg = self.build_msg('17sCtrlT__{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_alarm_state_level1(self):
        ''' '''
        msg = self.build_msg('18rAlrmLv1')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            A0idx = int(ret[14])
            A1idx = int(ret[15])
            A2idx = int(ret[16])
            A3idx = int(ret[17])
            A4idx = int(ret[18])
            A5idx = int(ret[19])
            Aidx = [A0idx, A1idx, A2idx, A3idx, A4idx, A5idx]
            if any(Aidx):
                res = []
                for i in range(len(Aidx)):
                    if Aidx[i]:
                        res.append(self.A[i][Aidx[i]])
                return res
            else:
                return 0
        else:
            self.handle_error(ret[5])
            return None
        
    def get_alarm_state_level21(self):
        ''' '''
        msg = self.build_msg('19rAlrmLv21')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            B0idx = int(ret[15])
            B1idx = int(ret[16])
            B2idx = int(ret[17])
            B3idx = int(ret[18])
            B4idx = int(ret[19])
            B5idx = int(ret[20])
            B6idx = int(ret[21])
            B7idx = int(ret[22])
            Bidx = [B0idx, B1idx, B2idx, B3idx, B4idx, B5idx, B6idx, B7idx]
            if any(Bidx):
                res = []
                for i in range(len(Bidx)):
                    if Bidx[i]:
                        res.append(self.B[i][Bidx[i]])
                return res
            else:
                return 0
            return statestr
        else:
            self.handle_error(ret[5])
            return None
    
    def get_alarm_state_level22(self):
        ''' '''
        msg = self.build_msg('19rAlrmLv22')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            C0idx = int(ret[15])
            C1idx = int(ret[16])
            C2idx = int(ret[17])
            C3idx = int(ret[18])
            C4idx = int(ret[19])
            C5idx = int(ret[20])
            C6idx = int(ret[21])
            C7idx = int(ret[22])
            Cidx = [C0idx, C1idx, C2idx, C3idx, C4idx, C5idx, C6idx, C7idx]
            if any(Cidx):
                res = []
                for i in range(len(Cidx)):
                    if Cidx[i]:
                        res.append(self.C[i][Cidx[i]])
                return res
            else:
                return 0
        else:
            self.handle_error(ret[5])
            return None
    
    def get_warning_state_level1(self):
        ''' '''
        msg = self.build_msg('20rWarnLv1')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            W0idx = int(ret[14])
            W1idx = int(ret[15])
            W2idx = int(ret[16])
            W3idx = int(ret[17])
            Widx = [W0idx, W1idx, W2idx, W3idx]
            if any(Widx):
                res = []
                for i in range(len(Widx)):
                    if Widx[i]:
                        res.append(self.W[i][Widx[i]])
                return res
            else:
                return 0
        else:
            self.handle_error(ret[5])
            return None
    
    def set_hi_supply_temp_warn(self, t: float):
        ''' '''
        msg = self.build_msg('21sHiSpTWn{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_low_supply_temp_warn(self, t: float):
        ''' '''
        msg = self.build_msg('22sLoSpTWn{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_hi_ambient_temp_warn(self, t: float):
        ''' '''
        msg = self.build_msg('23sHiAmTWn{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_low_ambient_temp_warn(self, t: float):
        ''' '''
        msg = self.build_msg('24sLoAmTWn{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def set_low_process_flow_warn(self, f: float):
        ''' '''
        msg = self.build_msg('25sLoPFlTWn+{0:04d}'.format(round(f*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[15:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def set_hi_supply_temp_alarm(self, t: float):
        ''' '''
        msg = self.build_msg('26sHiSpTAl{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_low_supply_temp_alarm(self, t: float):
        ''' '''
        msg = self.build_msg('27sLoSpTAl{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_hi_ambient_temp_alarm(self, t: float):
        ''' '''
        msg = self.build_msg('28sHiAmTAl{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def set_low_ambient_temp_alarm(self, t: float):
        ''' '''
        msg = self.build_msg('29sLoAmTAl{0:+05d}'.format(round(t*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def set_low_process_flow_alarm(self, f: float):
        ''' '''
        msg = self.build_msg('30sLoPFlTAl+{0:04d}'.format(round(f*10)))
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[15:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    #cmd 31 reserved
    #cmd 32 reserved
    #cmd 33 reserved
    
    def get_hi_supply_temp_warn(self):
        ''' '''
        msg = self.build_msg('34sHiSpTWn')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_low_supply_temp_warn(self):
        ''' '''
        msg = self.build_msg('35sLoSpTWn')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_hi_ambient_temp_warn(self):
        ''' '''
        msg = self.build_msg('36sHiAmTWn')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_low_ambient_temp_warn(self):
        ''' '''
        msg = self.build_msg('37sLoAmTWn')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def get_low_process_flow_warn(self):
        ''' '''
        msg = self.build_msg('38sLoPFlTWn')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[15:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def get_hi_supply_temp_alarm(self):
        ''' '''
        msg = self.build_msg('39sHiSpTAl')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_low_supply_temp_alarm(self):
        ''' '''
        msg = self.build_msg('40sLoSpTAl')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_hi_ambient_temp_alarm(self):
        ''' '''
        msg = self.build_msg('41sHiAmTAl')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    def get_low_ambient_temp_alarm(self):
        ''' '''
        msg = self.build_msg('42sLoAmTAl')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
        
    def get_low_process_flow_alarm(self):
        ''' '''
        msg = self.build_msg('43sLoPFlTAl')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[15:19]
            return float(tstr)/10
        else:
            self.handle_error(ret[5])
            return None
    
    #cmd44 reserved
    #cmd45 reserved
    
    def get_pwm_and_relay_status(self):
        ''' '''
        msg = self.build_msg('46rPulWdMo')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            pwm=ret[14:17]
            r=ret[18]
            mode = "Cooling" if r==b'C' else "Heating"
            return int(pwm), mode
        else:
            self.handle_error(ret[5])
            return None
    
    # cmd 47 reserved
    
    def get_pid_status(self):
        ''' '''
        msg = self.build_msg('48rPIDStat')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            tstr=ret[14:19]
            k = ret[20]
            #PID mode flag 0...9. but undefined in manual.
            return float(tstr)/10 , int(k)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_unit_uptime(self):
        ''' Return unit uptime in minutes'''
        msg = self.build_msg('49rUpTime_')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            minstr=ret[14:20]
            return int(minstr)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_fanspeed_1(self):
        ''' Return Fan 1 speed in Hz'''
        msg = self.build_msg('50rFanSpd1')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            hzstr=ret[14:18]
            return int(hzstr)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_fanspeed_2(self):
        ''' Return Fan 2 speed in Hz'''
        msg = self.build_msg('51rFanSpd2')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            hzstr=ret[14:18]
            return int(hzstr)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_fanspeed_3(self):
        ''' Return Fan 3 speed in Hz'''
        msg = self.build_msg('52rFanSpd3')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            hzstr=ret[14:18]
            return int(hzstr)
        else:
            self.handle_error(ret[5])
            return None
    
    def get_fanspeed_4(self):
        ''' Return Fan 4 speed in Hz'''
        msg = self.build_msg('53rFanSpd4')
        self.dev.write(msg)
        ret = self.read()
        if ret[5] == '0':
            hzstr=ret[14:18]
            return int(hzstr)
        else:
            self.handle_error(ret[5])
            return None
    
    # cmd 54 reserved
    # cmd 55 reserved
    # cmd 56 reserved
    # cmd 57 reserved
    # cmd 58 reserved
    
    def set_default_eeprom(self):
        ''' '''
        msg = self.build_msg('59sDUrEEPU')
        self.dev.write(msg)
        ret = self.read()
        
        return 0
    
    # cmd 60 reserved
    
    def handle_error(self, code):
        print(self.ERR[int(code)])
        return self.ERR[int(code)]
