# old TR-064-Protokoll with GET request and MD5

from . import md5 as __md5		# MD5 hash 
from . import tinyXML_250625 as __xml		# evaluating XML strings
import urequests as __rq		#	

FB_LOGIN_URL = const('http://fritz.box/login_sid.lua')						# URL for getting SID via TR-064 protokol
FB_CMD_URL = const('http://fritz.box/webservices/homeautoswitch.lua')		# URL for communication with devices via fritzbox
USERNAME = const('esp_smarthome')
FB_PASSWD = const('Nikomey12!')
CHUNKSIZE = 512

# Check if esp is connected to fritzbox
def connect():
    import network
    sta = network.WLAN(network.STA_IF)
    sta.active(1) if not sta.active() else None
    print('\rLooking for Wifis....')
    wifis = sta.scan()
    for i, ssid in enumerate(wifis):
        print(f'{i:2d} {ssid[0]} | {ssid[3]} | {ssid[4]}')
    i = input('Enter number: ')
    assert i.isdigit() and int(i)<=len(wifis), 'Invalid input!'
    ssid = wifis[int(i)][0].decode()
    pwd = input(f'Password for {ssid}: ')
    sta.connect(ssid, pwd)
    i = 0
    char = ['|', '/', '-', '\\']
    while not sta.isconnected() and i<40:
        print(f'Connecting to {ssid}{char[i%4]}', end='\r')
        i += 1
        __import__('utime').sleep_ms(500)
    print(f'Connection sucessfull: {sta.isconnected()}!')
    

class FritzBox:
    def __init__(self, usr=USERNAME, pwd=FB_PASSWD):
        self.sta = __import__('network').WLAN(__import__('network').STA_IF)
        self.sid = None
        self.challenge = None
        self.devices = {}
        self.usr = usr
        self.__first_chunk = False
        self.__chunks = False
        self.XML = __xml.XML()
        self.__get_challenge()
        self.__calc_response(pwd)
        self.__send_response()
        
    def __get_rq(self, url):
        ''' get request via urequest function '''
        return __rq.get(url)
      
    def __get_challenge(self):
        ''' asks Fritzbox for a CHALLENGE  value '''
        assert self.sta.isconnected(), 'Not connected to Wifi'
        print(f'1. Ask Fritzbox for CHALLENGE', end=': ')
        getRQ = self.__get_rq(FB_LOGIN_URL)
        assert getRQ.status_code==200, f'Fritzbox not reachable, status={getRQ.status}'
        # find SID and challenge values
        self.sid = self.XML.Data_from_tagname(getRQ.text, 'SID')
        self.challenge = self.XML.Data_from_tagname(getRQ.text, 'Challenge')
        print(f'{self.challenge}')
        
    def __calc_response(self, pwd):
        ''' calulate response from challange and pwd: response = 'challange-md5.hash(challenge-password)' '''
        utf16le = b''
        resp_str = self.challenge + '-' + pwd
        for i in resp_str:
            utf16le += ord(i).to_bytes(2, 'little')
        md5 = __md5.MD5()
        md5.update(utf16le)
        self.response = self.challenge + '-' + md5.hash
    
    def __send_response(self):
        url = f'{FB_LOGIN_URL}?username={self.usr}&response={self.response}'
        print(f'2. Response string sent: {self.response}')
        getRQ = self.__get_rq(url).text
        self.XML.Reset()
        self.sid = self.XML.Data_from_tagname(getRQ, 'SID')
        print(f'3. SID: {self.sid}')
        
    def Send_cmd(self, cmd, ain=None):
        ''' Send a command '''
        if ain is not None:
            ain = ain.replace(' ', '')
        url = f'{FB_CMD_URL}?switchcmd={cmd}&sid={self.sid}' if ain is None else f'{FB_CMD_URL}?switchcmd={cmd}&sid={self.sid}&ain={ain}'
        print(f'COMMAND: {cmd}') if ain is None else print(f'COMMAND: {cmd} to {ain}')
        return self.__get_rq(url).text

    def Getdevicelistinfos(self):
        assert int(self.sid, 16)!=0, 'SID is 00000000000'
        xml = self.Send_cmd('getdevicelistinfos')
        attrib = self.XML.Attributes_from_tagname(xml, 'devicelist')
        self.fb_version = attrib['fwversion']
        i = 0
        self.ain = {}
        while True:
            attrib = self.XML.Attributes_from_tagname(xml, 'device')
            i += 1
            if i==self.XML.tag_identities:
                return self.ain
            if attrib['identifier']!='':
                self.ain[attrib['identifier']] = attrib['productname']
            
       
    
    

    
        
"""
    def __get_rq_chunk(self, url, chunksize=CHUNKSIZE):
        print('A')
        if not self.__first_chunk:
            self.response = __rq.get(url, stream=True)
            self.__first_chunk = True
        data = self.response.raw.read(512) if self.response.raw is not None else b''
        if data==b'':
            self.response.close()
            self.__chunks = False
        return data
"""
        
        
        
        
        
