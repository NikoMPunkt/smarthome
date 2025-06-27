# FRITZ!Smart Energy 200 device
from . import dev_all as __devices

TIME_DELTA = const(946_684_800) # diff beteen unix and uPy timestamp

PRODUCTNAME = const('FRITZ!Smart Energy 200')

class DECT_200(__devices.Devices):
    def __init__(self, fritzObj, ain):
        self.fb = fritzObj
        self.ain = ain
        self.stats_info = {}
        self.device_info = {}
        self.device_name = ''
        self.__check_id(ain)
        super().__init__(fritzObj)

    def Get_state(self):
        ''' reads switching state (on or off)'''
        cmd = 'getswitchstate'
        ret = self.fb.Send_cmd(cmd, self.ain)
        print(ret)
    
    def Get_sensors(self):
        U, P, E, T = self.Get_parameter('voltage', 'power', 'energy', 'celsius')
        return {'T': T, 'P': P, 'U': U, 'E': E}
  
    # SET commands
    def Set_switch(self, value=None):
        ''' set switching state to off, on or toggle'''
        if value is 1:
            cmd = 'setswitchon'
        elif value is 0:
            cmd = 'setswitchoff'
        else:
            cmd = 'setswitchtoggle'
        return self.fb.Send_cmd(cmd, self.ain)[:1]

