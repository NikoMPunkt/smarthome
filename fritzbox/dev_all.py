# General fincrions for all devices
from . import tinyXML_250625 as __xml

TIME_DELTA = const(946_684_800) # diff beteen unix and uPy timestamp

class Devices:
    def __init__(self, frizxbox):
        self.fb = frizxbox
        self.XML = __xml.XML()
        
    def __check_id(self, identifier):
        ''' check if ain and device type is correct '''
        for device in self.fb.devices:
            if device['identifier']==self.ain and device['productname']==PRODUCTNAME:
                self.device_status = True
                
    def __convert_time(self, unix_ts):
        return __import__('utime').localtime(unix_ts - TIME_DELTA)
    
    def Get_device_info(self):
        ''' attributes of <device ....> tag '''
        cmd = 'getdeviceinfos'
        xml = self.fb.Send_cmd(cmd, self.ain)
        self.XML.Data_from_tagname(xml, 'device')
        self.device_info = self.XML.Extract_attributes()
        return self.device_info
    
    def __list_parameter_info(self):
        ''' list all parameters acc <parameter>data</parameter>'''
        cmd = 'getdeviceinfos'
        xml = self.fb.Send_cmd(cmd, self.ain)
        pos = 0
        para_list = []
        while True:
            y0 = xml.find('</', pos)
            if y0 is -1:
                break
            y1 = xml.find('>', y0)
            tag = xml[y0+2:y1]
            if xml[y0-1]!='>':
                para_list.append(tag)
            pos = y1
        return para_list
        
    def Get_parameter(self, *parameter):
        ''' give data for <parameter>data</parameter>'''
        if parameter is ():
            return self.__list_parameter_info()
        cmd = 'getdeviceinfos'
        xml = self.fb.Send_cmd(cmd, self.ain)
        data = []
        for para in parameter:
            data.append(self.XML.Data_from_tagname(xml, para))
            self.device_info = self.XML.Extract_attributes()
        return data
    
    def __get_parameters(self, xml, tag):
        ptr = 0
        nr_of_para = xml.count(tag)
        tag_pos = 0
        para_list = []
        for i in range(nr_of_para):
            x1 = xml.find(tag, tag_pos) - 1
            x0 = xml.rfind('<', tag_pos, x1) + 1
            para = xml[x0:x1]
            tag_pos = x1 + 2
            if xml[x0]=='/':
                continue
            para_list.append(para)
        return para_list
        
    def Get_statistics(self, parameter=None):
        ''' get history values '''
        cmd = 'getbasicdevicestats'
        xml = self.fb.Send_cmd(cmd, self.ain)
        if parameter is None:
            para_list = self.__get_parameters(xml, '<stats ')
            return para_list
        data = self.XML.Data_from_tagname(xml, parameter, 'stats')
        self.stats_info = self.XML.Extract_attributes()
        return data
    
    def Get_device_name(self):
        ''' Liefert Bezeichner des Aktors '''
        cmd = 'getswitchname'
        self.device_name = self.fb.Send_cmd(cmd, self.ain)[:-1]
        return self.device_name
    
    def Get_connection(self):
        ''' Ermittelt Verbindungsstatus des Aktors '''
        cmd = 'getswitchpresent'
        return self.fb.Send_cmd(cmd, self.ain)[:-1]
    
    def Get_temperature(self):
        ''' Temperaturinformation des Aktors '''
        cmd = 'gettemperature'
        ret = self.fb.Send_cmd(cmd, self.ain)
        return int(ret)/10
    
    

