from . import dev_all as __devices

TIME_DELTA = const(946_684_800) # diff beteen unix and uPy timestamp

class HKR(__devices.Devices):
    def __init__(self, fritzObj, ain):
        self.fb = fritzObj
        self.ain = ain
        self.stats_info = {}
        self.device_info = {}
        self.device_name = ''
        self.__check_id(ain)
        self.stats = {}
        super().__init__(fritzObj)
        
    def __val2temp(self, val):
        if val=='253':
            return 'OFF'
        elif val=='254':
            return 'ON'
        else:
            return int(val)/2

    def Get_soll(self):
        '''  aktuell eingestellte Solltemperatur '''
        cmd = 'gethkrtsoll'
        ret = self.fb.Send_cmd(cmd, self.ain)
        return self.__val2temp(ret[:-1])
    
    def Get_komfort(self):
        '''  Für HKR-Zeitschaltung eingestellte Komforttemperatur '''
        cmd = 'gethkrkomfort'
        ret = self.fb.Send_cmd(cmd, self.ain)
        return self.__val2temp(ret[:-1])
    
    def Get_absenk(self):
        ''' Für HKR-Zeitschaltung eingestellte Spartemperatur '''
        cmd = 'gethkrabsenk'
        ret = self.fb.Send_cmd(cmd, self.ain)
        return sself.__val2temp(ret[:-1])
    
