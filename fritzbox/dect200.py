# FRITZ!Smart Energy 200 device

PRODUCTNAME = const('FRITZ!Smart Energy 200')

class DECT_200:
    def __init__(self, fritzObj, ain):
        self.fb = fritzObj
        self.XML = fritzObj.XML
        self.ain = ain
        self.device_status = False
        self.__check_id(ain)
        self.stats = {}
    
    def __check_id(self, identifier):
        ''' check if ain and device type is correct '''
        for device in self.fb.devices:
            if device['identifier']==self.ain and device['productname']==PRODUCTNAME:
                self.device_status = True
    
    def Get_state(self):
        ''' reads switching state (on or off)'''
        cmd = 'getswitchstate'
        ret = self.fb.Send_cmd(cmd, self.ain)
        print(ret)
    
    def Get_connection(self):
        ''' is switch connected ? '''
        cmd = 'getswitchpresent'
        ret = self.fb.Send_cmd(cmd, self.ain)
        print(ret)
        
    def Get_sensors(self):
        cmd = 'getdeviceinfos'
        xml = self.fb.Send_cmd(cmd, self.ain)
        T = self.XML.Data_from_tagname(xml, 'celsius')
        P = self.XML.Data_from_tagname(xml, 'power')
        E = self.XML.Data_from_tagname(xml, 'energy')
        U = self.XML.Data_from_tagname(xml, 'voltage')
        return {'T': T, 'P': P, 'U': U, 'E': E}
    
    def Get_statistics(self, parameter=None):
        ''' temperature '''
        assert parameter is not None, 'temperature, power, voltage, energy'
        cmd = 'getbasicdevicestats'
        xml = self.fb.Send_cmd(cmd, self.ain)
        data = self.XML.Data_from_tagname(xml, parameter, 'stats')
        self.stats = self.XML.Extract_attributes()
        return data

    # SET commands
    def Set_switch(self, value=None):
        ''' set switching state to off, on or toggle'''
        if value is 1:
            cmd = 'setswitchon'
        elif value is 0:
            cmd = 'setswitchoff'
        else:
            cmd = 'setswitchtoggle'
        return self.fb.Send_cmd(cmd, self.ain)

