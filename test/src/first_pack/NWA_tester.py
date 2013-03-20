'''
Created on Mar 14, 2013

@author: charliex
'''
def S_TRAN():
    return {"S21":0,"S41":0,"S23":0,"S43":0}
    

if __name__ == '__main__':
    from visa import *
    from math import pow, exp
    import time
    
    myinstr = get_instruments_list()
    print(myinstr)
    #This is used when the script is asking the user to specify the instrument name
    #myinstr = input("What is your instrument name? ") 
    my_instrument = instrument("GPIB0::16")
    instrument_attri = my_instrument.ask("*IDN?")
    manufact, model_num, ser_num, firm_ver = instrument_attri.split(",",4)    
    print("Instrument is a %s %s, firmware version is %s. " % (manufact, model_num, firm_ver))
    
    my_instrument.write("OPC?;PRES")                        #Return instrument to preset
    
    instrument_timeout = my_instrument.timeout
    print("Time out timers is %s second" %instrument_timeout)
    '''
    #Instrument calibration code
    #cal_dictionary = {"Yes":1, "No":0}
    #The 8753C Network Analyzer doesn't support the CALK35ME calkit, so the CALK35MM calkit is used
    my_instrument.write("CALK35MM;CLES,ESE64")
    my_instrument.write("CALIFUL2")                         #Performing a full 2-port cal
    my_instrument.write("REFL")                             #Reflection calibration
    raw_input("Connect OPEN to port 1, then press enter")
    my_instrument.write("CLASS11A")
    raw_input("Connect SHORT to port 1, then press enter")
    my_instrument.write("CLASS11B")
    raw_input("Connect LOAD to port 1, then press enter")
    my_instrument.write("CLASS11C")
    raw_input("Connect OPEN to port 2, then press enter")
    my_instrument.write("CLASS22A")
    raw_input("Connect SHORT to port 2, then press enter")
    my_instrument.write("CLASS22B")
    raw_input("Connect LOAD to port 2, then press enter")
    my_instrument.write("CLASS22C")
    print("Waiting for instrument to calculate calibration coefficient.")
    my_instrument.write("OPC?;REFD")
    while True:                             #Exception handling incase the calibration timesout PyVISA
        try:
            my_instrument.ask("*OPC?")
            
            break
        except VisaIOError:
            my_instrument.ask("*OPC?")
            
    print("Reflection calibration finished.")
    
    my_instrument.write("TRAN")                                 #Transmission calibration
    raw_input("Connect port 1 to port 2, then press enter")
    my_instrument.write("FWDT")
    print("Measuring fwd transmission")
    my_instrument.ask("*OPC?")
    my_instrument.write("FWDM")
    print("Measuring fwd match")
    my_instrument.ask("*OPC?")
    my_instrument.write("REVT")
    print("Measuring reverse transmission")
    my_instrument.ask("*OPC?")
    my_instrument.write("REVM")
    print("Measuring reverse match")
    print("waiting for instrument to calculate calibration coefficient")
    my_instrument.ask("*OPC?")
    my_instrument.write("TRAD")
    my_instrument.ask("*OPC?")
    print("Transmission calibration finished")
    
    my_instrument.write("OMII")

    my_instrument.write("DONE")
    my_instrument.write("SAV2")
    print("Calculating calibration coefficient for the full 2-port calibration")
    while True:
        try:
            my_instrument.ask("*OPC?")
            
            break
        except VisaIOError:
            my_instrument.ask("*OPC?")
    print("Full 2-port calibration finished")
    '''
    
    #Change the timeout timer to work with marker output
    instrument_timeout_def = instrument_timeout     #save the old timeout time
    instrument_timeout = 20.0
    my_instrument.timeout = instrument_timeout
    print("Changing the timeout timer to %s sec" %my_instrument.timeout)
    
    # Ask about what kind of BPM is being calibrated
    #BPM_style = raw_input("What style is the BPM's processing freq? ")
    #print("Frequency %r" %(BPM_style) )
    my_instrument.write("STAR 270 MHZ; STOP 330 MHZ;OPC?")
    #my_instrument.write("CENT 300 MHZ; SPAN 60 MHZ;OPC?")
    my_instrument.write("S21")
    my_instrument.write("LINM")
    my_instrument.write("AUTO")
    my_instrument.write("IFBW 100HZ")
    my_instrument.write("MARK1 300MHZ")
    my_instrument.ask("*OPC?")
    
    test1 = S_TRAN()
    test2 = S_TRAN()
    test3 = S_TRAN()
    
    raw_input("Connect port 1 to RED and port 2 to BLUE, then press enter")
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    #result = my_instrument.read_values()
    #result = my_instrument.read()
    #print(result)
    #test1["S21"], phase, frequency = result
    #print("magnitude is %s Unit, phase is %s degree, at %.3eHz" %(test1["S21"], phase, frequency))
    test1["S21"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test2["S21"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test3["S21"], phase, frequency = result
    time.sleep(2)
        
    raw_input("Connect port 1 to RED and port 2 to GREEN, then press enter")
    my_instrument.write("MARK1 300MHZ")
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test1["S41"], phase, frequency = result 
    time.sleep(2)
    my_instrument.write("WAIT")   
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test2["S41"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test3["S41"], phase, frequency = result
    time.sleep(2)
    
    raw_input("Connect port 1 to YELLOW and port 2 to BLUE, then press enter")
    my_instrument.write("MARK1 300MHZ")
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test1["S23"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test2["S23"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test3["S23"], phase, frequency = result
    time.sleep(2)
            
    raw_input("Connect port 1 to YELLOW and port 2 to GREEN, then press enter")
    my_instrument.write("MARK1 300MHZ")
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test1["S43"], phase, frequency = result
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test2["S43"], phase, frequency = result  
    time.sleep(2)
    my_instrument.write("WAIT")
    result = my_instrument.ask_for_values("OUTPMARK")
    my_instrument.ask("*OPC?")
    test3["S43"], phase, frequency = result
    time.sleep(2)
    
    #Changing back the timeout timer
    instrument_timeout = instrument_timeout_def
    my_instrument.timeout = instrument_timeout
    print("Time out timer is changed back to %s sec" %my_instrument.timeout)
              
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
    
    
    '''
    if cal_dictionary["Yes"]:
        print("Python counts 1 as true")    
    else:
        print("Python doesn't read 1 as true")
    #print(mag,phase,frequency)
    #my_instrument.write("S12")
    #time.sleep(3)
    #my_instrument.write("S21")
    #time.sleep(3)
    #my_instrument.write("S22")
    #print(my_instrument.read())
    '''