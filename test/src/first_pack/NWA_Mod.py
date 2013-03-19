'''
Created on Mar 18, 2013

@author: charliex
'''
from visa import *
#from NetworkAnaly_GUI import *

class BPM_NWA:
    def __init__(self):
        self.name = "BPM testing module"
        #root = Tk()
    
    def GPIB_fetch(self):
        self.myinstr = get_instruments_list()
        print self.myinstr
        for devices in self.myinstr:
            if 'GPIB' in devices:
                gpib_dev = instrument(devices)
                gpib_dev_attri = gpib_dev.ask("*IDN?")
                print("Device %s is a %s" %(gpib_dev, gpib_dev_attri))
        return self.myinstr
 
'''           
    def GPIB_init(self,GPIB_device):
        self.my_instr_dev = instrument(GPIB_device)
        self.instrument_attri = self.my_instr_dev.ask("*IDN?")
'''