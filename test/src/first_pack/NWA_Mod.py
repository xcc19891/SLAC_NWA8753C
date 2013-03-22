'''
Created on Mar 18, 2013

@author: charliex
'''
from visa import *
#from NetworkAnaly_GUI import *

class BPM_NWA:
    def __init__(self):
        self.name = "BPM testing module"
        self.gpib_dev = 0
        #root = Tk()
 
    
    def GPIB_fetch(self):
        error = 1
        self.myinstr = get_instruments_list()
        #print self.myinstr
        for devices in self.myinstr:
            #print devices
            if "GPIB0::16" in devices:
                self.gpib_dev = instrument(devices)
                while True:
                    try:
                        self.gpib_dev_attri = self.gpib_dev.ask("*IDN?")
                        manufact, model_num, ser_num, firm_ver = self.gpib_dev_attri.split(",",4)
                        if (model_num == "8753C") and (manufact == "HEWLETT PACKARD"):
                            print("Device found")
                            self.gpib_dev.write("OPC?;PRES") 
                        error = 0
                        break
                    except VisaIOError:
                        print("Please check connection with the HP8753C")
                        error = 1
                        break                
            if error == 0:
                break    
        return manufact, model_num, ser_num, firm_ver, error
    
    def NWA_cal(self):
        #print(self.gpib_dev)
        #print("Let's start the calibration!")
        #The 8753C Network Analyzer doesn't support the CALK35ME calkit, so the CALK35MM calkit is used
        self.gpib_dev.write("CALK35MM;CLES,ESE64")
        self.gpib_dev.write("CALIFUL2")                         #Performing a full 2-port cal
        self.gpib_dev.write("REFL")                             #Reflection calibration
        raw_input("Connect OPEN to port 1, then press enter")
        self.gpib_dev.write("CLASS11A")
        raw_input("Connect SHORT to port 1, then press enter")
        self.gpib_dev.write("CLASS11B")
        raw_input("Connect LOAD to port 1, then press enter")
        self.gpib_dev.write("CLASS11C")
        raw_input("Connect OPEN to port 2, then press enter")
        self.gpib_dev.write("CLASS22A")
        raw_input("Connect SHORT to port 2, then press enter")
        self.gpib_dev.write("CLASS22B")
        raw_input("Connect LOAD to port 2, then press enter")
        self.gpib_dev.write("CLASS22C")
        print("Waiting for instrument to calculate calibration coefficient.")
        self.gpib_dev.write("OPC?;REFD")
        while True:                             #Exception handling incase the calibration timesout PyVISA
            try:
                self.gpib_dev.ask("*OPC?")
                
                break
            except VisaIOError:
                self.gpib_dev.ask("*OPC?")
                
        print("Reflection calibration finished.")
        
        self.gpib_dev.write("TRAN")                                 #Transmission calibration
        raw_input("Connect port 1 to port 2, then press enter")
        self.gpib_dev.write("FWDT")
        print("Measuring fwd transmission")
        self.gpib_dev.ask("*OPC?")
        self.gpib_dev.write("FWDM")
        print("Measuring fwd match")
        self.gpib_dev.ask("*OPC?")
        self.gpib_dev.write("REVT")
        print("Measuring reverse transmission")
        self.gpib_dev.ask("*OPC?")
        self.gpib_dev.write("REVM")
        print("Measuring reverse match")
        print("waiting for instrument to calculate calibration coefficient")
        self.gpib_dev.ask("*OPC?")
        self.gpib_dev.write("TRAD")
        self.gpib_dev.ask("*OPC?")
        print("Transmission calibration finished")
        
        self.gpib_dev.write("OMII")
    
        self.gpib_dev.write("DONE")
        self.gpib_dev.write("SAV2")
        print("Calculating calibration coefficient for the full 2-port calibration")
        while True:
            try:
                self.gpib_dev.ask("*OPC?")
                
                break
            except VisaIOError:
                self.gpib_dev.ask("*OPC?")
        print("Full 2-port calibration finished")
        
    def S21_measure(self):
        print("Got you in NWA_Mod")
        pass