'''
Created on Mar 14, 2013

@author: charliex
'''
from visa import *
from math import pow, exp
import time
import sys
import datetime

class BPM_chara:
    def __init__(self):
        print("Welcome to SLAC BPM characterization program\n")
        self.BPM_ser = raw_input("Please enter BPM serial number:\n")
        
        self.BPM_record = open("BPM-"+self.BPM_ser+"-cal.txt", "w+")
        #print("Filename: %s" %self.BPM_record.name)
        #print("File mode: %s" %self.BPM_record.mode)
        self.BPM_record.write("Calibration Date:")
        self.rec_time_stampe = datetime.datetime.today()
        self.BPM_record.write("%s\n" %self.rec_time_stampe)
        self.BPM_record.write("BPM Serial Number: %s\n" %self.BPM_ser)
        self.BPM_pmcc_str = raw_input("Please enter BPM radius in mm: \n--->")
        self.BPM_pmcc = int(self.BPM_pmcc_str)
        self.BPM_record.write("BPM radius is: %d mm\n" %self.BPM_pmcc)
        
        myinstr = get_instruments_list()
        print(myinstr)
        print("Default GPIB address for the network analyzer is \"GPIB0:16\"\n")
        #This is used when the script is asking the user to specify the instrument name
        #myinstr = input("What is your instrument name? ") 
        while True:
            try:
                self.my_instr = instrument("GPIB0::16")
                break
            except VisaIOError:
                print("Please connect the network analyzer and try again.")
                sys.exit("Exiting program")
            
        instrument_attri = self.my_instr.ask("*IDN?")
        manufact, model_num, ser_num, firm_ver = instrument_attri.split(",",4)
        #manufact, model_num, ser_num, firm_ver, error = [0,0,0,0,0]    
        print("Instrument is a %s %s, firmware version is %s. \n" % (manufact, model_num, firm_ver))
        
        self.my_instr.write("OPC?;PRES")                        #Return instrument to preset
        
        self.instrument_timeout = self.my_instr.timeout
        #print("Time out timers is %s second" %self.instrument_timeout)
        
        #print(self.my_instr.ask("READDATE"))
        #print(self.my_instr.ask("READTIME"))
        
        print("WARNING:If you are running this process for the first time\n you need to calibrate the network analyzer")
        cal_opt = raw_input("Do you want to calibrate the Network analyzer?\n---> ")
        
        if (cal_opt == "yes") or (cal_opt == "Yes"):
            self.NWA_cal()
        
        
        self.S21_measure()
        self.BPM_record.close()
        
        
        
    def S21_measure(self):
        #Change the timeout timer to work with marker output
        self.instrument_timeout_def = self.instrument_timeout     #save the old timeout time
        self.instrument_timeout = 20.0
        self.my_instr.timeout = self.instrument_timeout
        print("Changing the timeout timer to %s sec" %self.my_instr.timeout)
        
        # Ask about what kind of BPM is being calibrated
        self.BPM_cnt_f = raw_input("What style is the BPM's processing freq? (In MHZ)\n---> ")
        self.BPM_cnt_f_int = int(self.BPM_cnt_f)
        self.NWA_star = str(self.BPM_cnt_f_int - 30)
        self.NWA_stop = str(self.BPM_cnt_f_int + 30)
        self.my_instr.write("STAR "+self.NWA_star+" MHZ; STOP "+self.NWA_stop+" MHZ;OPC?")
        self.my_instr.write("S21")
        self.my_instr.write("LINM")
        self.my_instr.write("AUTO")
        self.my_instr.write("IFBW 100HZ")
        self.my_instr.write("MARK1 "+self.BPM_cnt_f+"MHZ")
        
        self.BPM_record.write("BPM processing freq: %s\n MHz" %self.BPM_cnt_f)
        
        self.my_instr.ask("*OPC?")
        
        test1 = self.S_TRAN()
        test2 = self.S_TRAN()
        test3 = self.S_TRAN()
        
        raw_input("Connect port 1 to RED and port 2 to BLUE, then press enter")
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        #result = self.my_instr.read_values()
        #result = self.my_instr.read()
        #print(result)
        #test1["S21"], phase, frequency = result
        #print("magnitude is %s Unit, phase is %s degree, at %.3eHz" %(test1["S21"], phase, frequency))
        test1["S21"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test2["S21"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test3["S21"], phase, frequency = result
        time.sleep(2)
            
        raw_input("Connect port 1 to RED and port 2 to GREEN, then press enter")
        self.my_instr.write("MARK1 300MHZ")
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test1["S41"], phase, frequency = result 
        time.sleep(2)
        self.my_instr.write("WAIT")   
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test2["S41"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test3["S41"], phase, frequency = result
        time.sleep(2)
        
        raw_input("Connect port 1 to YELLOW and port 2 to BLUE, then press enter")
        self.my_instr.write("MARK1 300MHZ")
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test1["S23"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test2["S23"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test3["S23"], phase, frequency = result
        time.sleep(2)
                
        raw_input("Connect port 1 to YELLOW and port 2 to GREEN, then press enter")
        self.my_instr.write("MARK1 300MHZ")
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test1["S43"], phase, frequency = result
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test2["S43"], phase, frequency = result  
        time.sleep(2)
        self.my_instr.write("WAIT")
        result = self.my_instr.ask_for_values("OUTPMARK")
        self.my_instr.ask("*OPC?")
        test3["S43"], phase, frequency = result
        time.sleep(2)
        
        #Changing back the timeout timer
        self.instrument_timeout = self.instrument_timeout_def
        self.my_instr.timeout = self.instrument_timeout
        print("Time out timer is changed back to %s sec" %self.my_instr.timeout)
                  
        x1 = ((test1["S41"]-test1["S21"])-(test1["S43"]-test1["S23"]))/(test1["S21"]+test1["S41"]+test1["S43"]+test1["S23"])
        y1 = ((test1["S41"]-test1["S43"])-(test1["S21"]-test1["S23"]))/(test1["S21"]+test1["S41"]+test1["S43"]+test1["S23"])
        
        x2 = ((test2["S41"]-test2["S21"])-(test2["S43"]-test2["S23"]))/(test2["S21"]+test2["S41"]+test2["S43"]+test2["S23"])
        y2 = ((test2["S41"]-test2["S43"])-(test2["S21"]-test2["S23"]))/(test2["S21"]+test2["S41"]+test2["S43"]+test2["S23"])
        
        x3 = ((test3["S41"]-test3["S21"])-(test3["S43"]-test3["S23"]))/(test3["S21"]+test3["S41"]+test3["S43"]+test3["S23"])
        y3 = ((test3["S41"]-test3["S43"])-(test3["S21"]-test3["S23"]))/(test3["S21"]+test3["S41"]+test3["S43"]+test3["S23"])
                
        print("First sets of sample data:\n %s" %test1)
        print("Second sets of sample data:\n %s" %test2)
        print("Third sets of sample data:\n %s" %test3)
        print("X center for\n1st set: %s,\n2nd set: %s,\n3rd set: %s\n" %(x1,x2,x3))
        print("Y center for\n1st set: %s,\n2nd set: %s,\n3rd set: %s\n" %(y1,y2,y3))
  
        self.BPM_record.write("Record format is: \n")
        self.BPM_record.write("S21,S41,S23,S43\n")
        self.BPM_record.write("%s\n" %test1)
        self.BPM_record.write("%s\n" %test2)
        self.BPM_record.write("%s\n" %test2)
        self.BPM_record.write("X center is at:\n")
        self.BPM_record.write("%s,%s,%s\n" %(x1,x2,x3))
        self.BPM_record.write("Y center is at:\n")
        self.BPM_record.write("%s,%s,%s\n" %(y1,y2,y3))
        

    def S_TRAN(self):
        return {"S21":0,"S41":0,"S23":0,"S43":0}
        
    def NWA_cal(self):
        #Instrument calibration code
        #The 8753C Network Analyzer doesn't support the CALK35ME calkit, so the CALK35MM calkit is used
        self.my_instr.write("CALK35MM;CLES,ESE64")
        self.my_instr.write("CALIFUL2")                         #Performing a full 2-port cal
        self.my_instr.write("REFL")                             #Reflection calibration
        raw_input("Connect OPEN to port 1, then press enter")
        self.my_instr.write("CLASS11A")
        raw_input("Connect SHORT to port 1, then press enter")
        self.my_instr.write("CLASS11B")
        raw_input("Connect LOAD to port 1, then press enter")
        self.my_instr.write("CLASS11C")
        raw_input("Connect OPEN to port 2, then press enter")
        self.my_instr.write("CLASS22A")
        raw_input("Connect SHORT to port 2, then press enter")
        self.my_instr.write("CLASS22B")
        raw_input("Connect LOAD to port 2, then press enter")
        self.my_instr.write("CLASS22C")
        print("Waiting for instrument to calculate calibration coefficient.")
        self.my_instr.write("OPC?;REFD")

        while True:                             #Exception handling incase the calibration timesout PyVISA
            try:
                self.my_instr.ask("*OPC?")
                
                break
            except VisaIOError:
                self.my_instr.ask("*OPC?")
                
        print("Reflection calibration finished.")
        
        self.my_instr.write("TRAN")                                 #Transmission calibration
        raw_input("Connect port 1 to port 2, then press enter")
        self.my_instr.write("FWDT")
        print("Measuring fwd transmission")
        self.my_instr.ask("*OPC?")
        self.my_instr.write("FWDM")
        print("Measuring fwd match")
        self.my_instr.ask("*OPC?")
        self.my_instr.write("REVT")
        print("Measuring reverse transmission")
        self.my_instr.ask("*OPC?")
        self.my_instr.write("REVM")
        print("Measuring reverse match")
        print("waiting for instrument to calculate calibration coefficient")
        self.my_instr.ask("*OPC?")
        self.my_instr.write("TRAD")
        self.my_instr.ask("*OPC?")
        print("Transmission calibration finished")
        
        self.my_instr.write("OMII")
    
        self.my_instr.write("DONE")
        self.my_instr.write("SAV2")
        print("Calculating calibration coefficient for the full 2-port calibration")
        while True:
            try:
                self.my_instr.ask("*OPC?")
                
                break
            except VisaIOError:
                self.my_instr.ask("*OPC?")
        print("Full 2-port calibration finished")
    
    def GPIB_init(self):
        pass
