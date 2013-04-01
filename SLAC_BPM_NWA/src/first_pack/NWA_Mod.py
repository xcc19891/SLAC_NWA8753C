'''
Created on Mar 18, 2013

@author: charliex
'''
from visa import *
from Tkinter import *
#from NetworkAnaly_GUI import *

class BPM_NWA:
    def __init__(self):
        self.name = "BPM testing module"
        self.gpib_dev = 0
        #root = Tk()
 
    
    def GPIB_fetch(self):
        manufact, model_num, ser_num, firm_ver, error = [0,0,0,0,0]
        return manufact, model_num, ser_num, firm_ver, error
        '''
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
                            self.instrument_timeout = self.gpib_dev.timeout
                        error = 0
                        break
                    except VisaIOError:
                        print("Please check connection with the HP8753C")
                        error = 1
                        break                
            if error == 0:
                break    
        return manufact, model_num, ser_num, firm_ver, error
        '''
        
    def prt_hack(self):
        msg_txt = StringVar()
        if (self.msg_ind) < (len(self.cal_messages)-1):
            self.msg_ind = self.msg_ind + 1
            self.cal_message = self.cal_messages[self.msg_ind]
            #print(self.msg_ind)
            #print(len(self.cal_messages))
            msg_txt.set(self.cal_message)
            self.prt_label = Label(self.cal_frame, textvariable=msg_txt)
            self.prt_label.pack(anchor='w')
        else:
            msg_txt.set("End of calibration.")    
    
    def NWA_cal(self):
        self.cal_frame = Toplevel()
        self.msg_ind = 0
        self.cal_messages = ("Hello","Connect OPEN to port 1, then click next","Connect SHORT to port 1, then press enter","Connect LOAD to port 1, then press enter",
                       "Connect OPEN to port 2, then press enter","Connect SHORT to port 2, then press enter","Connect LOAD to port 2, then press enter",
                       "Waiting for instrument to calculate calibration coefficient.","Reflection calibration finished.",
                       "Connect port 1 to port 2, then press enter","waiting for instrument to calculate calibration coefficient","Transmission calibration finished",
                       "Calculating calibration coefficient for the full 2-port calibration","Full 2-port calibration finished, press exit to go back")
        #print(self.gpib_dev)
        #print("Let's start the calibration!")
        print(self.cal_messages[0])
        self.cal_grt = Label(self.cal_frame,text="Network Analyzer Calibration\n Please use correct calkit for this test", font=(16))
        self.cal_grt.pack()
        #The 8753C Network Analyzer doesn't support the CALK35ME calkit, so the CALK35MM calkit is used
        self.cal_next = Button(self.cal_frame,text="Next")
        self.cal_next.bind("<Button-1>",
                           lambda event:self.prt_hack())
        self.cal_next.pack()
        #label_text = 
        #self.prt_label(label_text)
        
        '''
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
        while True:                             #Exception handling in case the calibration timesout PyVISA
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
        '''
        self.cal_quit = Button(self.cal_frame, text="Exit", bg="red", fg="white",command=self.cal_frame.destroy)
        self.cal_quit.pack()
        
    def S21_measure(self):
        print("Got you in NWA_Mod")
        #Change the timeout timer to work with marker output
        self.instrument_timeout_def = self.instrument_timeout     #save the old timeout time
        self.instrument_timeout = 20.0
        self.gpib_dev.timeout = self.instrument_timeout
        print("Changing the timeout timer to %s sec" %self.gpib_dev.timeout)
        
        # Ask about what kind of BPM is being calibrated
        #BPM_style = raw_input("What style is the BPM's processing freq? ")
        #print("Frequency %r" %(BPM_style) )
        self.cnt_messages = ("S21 Measurement","Connect port 1 to RED and port 2 to BLUE, then press enter","Connect port 1 to RED and port 2 to GREEN, then press enter",
                             "Connect port 1 to YELLOW and port 2 to BLUE, then press enter","Connect port 1 to YELLOW and port 2 to GREEN, then press enter")
        
        self.gpib_dev.write("STAR 270 MHZ; STOP 330 MHZ;OPC?")
        #self.gpib_dev.write("CENT 300 MHZ; SPAN 60 MHZ;OPC?")
        self.gpib_dev.write("S21")
        self.gpib_dev.write("LINM")
        self.gpib_dev.write("AUTO")
        self.gpib_dev.write("IFBW 100HZ")
        self.gpib_dev.write("MARK1 300MHZ")
        self.gpib_dev.ask("*OPC?")
        
        test1 = self.S_TRAN()
        test2 = self.S_TRAN()
        test3 = self.S_TRAN()
        
        raw_input("Connect port 1 to RED and port 2 to BLUE, then press enter")
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        #result = self.gpib_dev.read_values()
        #result = self.gpib_dev.read()
        #print(result)
        #test1["S21"], phase, frequency = result
        #print("magnitude is %s Unit, phase is %s degree, at %.3eHz" %(test1["S21"], phase, frequency))
        test1["S21"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test2["S21"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test3["S21"], phase, frequency = result
        time.sleep(2)
            
        raw_input("Connect port 1 to RED and port 2 to GREEN, then press enter")
        self.gpib_dev.write("MARK1 300MHZ")
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test1["S41"], phase, frequency = result 
        time.sleep(2)
        self.gpib_dev.write("WAIT")   
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test2["S41"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test3["S41"], phase, frequency = result
        time.sleep(2)
        
        raw_input("Connect port 1 to YELLOW and port 2 to BLUE, then press enter")
        self.gpib_dev.write("MARK1 300MHZ")
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test1["S23"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test2["S23"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test3["S23"], phase, frequency = result
        time.sleep(2)
                
        raw_input("Connect port 1 to YELLOW and port 2 to GREEN, then press enter")
        self.gpib_dev.write("MARK1 300MHZ")
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test1["S43"], phase, frequency = result
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test2["S43"], phase, frequency = result  
        time.sleep(2)
        self.gpib_dev.write("WAIT")
        result = self.gpib_dev.ask_for_values("OUTPMARK")
        self.gpib_dev.ask("*OPC?")
        test3["S43"], phase, frequency = result
        time.sleep(2)
        
        #Changing back the timeout timer
        self.instrument_timeout = self.instrument_timeout_def
        self.gpib_dev.timeout = self.instrument_timeout
        print("Time out timer is changed back to %s sec" %self.gpib_dev.timeout)
                  
        x1 = ((test1["S41"]-test1["S21"])-(test1["S43"]-test1["S23"]))/(test1["S21"]+test1["S41"]+test1["S43"]+test1["S23"])
        y1 = ((test1["S41"]-test1["S43"])-(test1["S21"]-test1["S23"]))/(test1["S21"]+test1["S41"]+test1["S43"]+test1["S23"])
        
        x2 = ((test2["S41"]-test2["S21"])-(test2["S43"]-test2["S23"]))/(test2["S21"]+test2["S41"]+test2["S43"]+test2["S23"])
        y2 = ((test2["S41"]-test2["S43"])-(test2["S21"]-test2["S23"]))/(test2["S21"]+test2["S41"]+test2["S43"]+test2["S23"])
        
        x3 = ((test3["S41"]-test3["S21"])-(test3["S43"]-test3["S23"]))/(test3["S21"]+test3["S41"]+test3["S43"]+test3["S23"])
        y3 = ((test3["S41"]-test3["S43"])-(test3["S21"]-test3["S23"]))/(test3["S21"]+test3["S41"]+test3["S43"]+test3["S23"])
        print("First sets of sample data: %s" %(test1))
        print("Second sets of sample data: %s" %test2)
        print("Third sets of sample data: %s" %test3)
        print("X center for 1st set: %s, 2nd set: %s, 3rd set: %s" %(x1,x2,x3))
        print("Y center for 1st set: %s, 2nd set: %s, 3rd set: %s" %(y1,y2,y3))
        
    def S_TRAN(self):
        return {"S21":0,"S41":0,"S23":0,"S43":0}