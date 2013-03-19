'''
Created on Mar 14, 2013

@author: charliex
'''


if __name__ == '__main__':
    from visa import *
    from math import pow, exp
    
    myinstr = get_instruments_list()
    print(myinstr[2])
    #This is used when the script is asking the user to specify the instrument name
    #myinstr = input("What is your instrument name? ") 
    my_instrument = instrument("GPIB0::16")
    instrument_attri = my_instrument.ask("*IDN?")
    manufact, model_num, ser_num, firm_ver = instrument_attri.split(",",4)    
    print("Instrument is a %s %s, firmware version is %s. " % (manufact, model_num, firm_ver))
    
    my_instrument.write("OPC?;PRES")                        #Return instrument to preset
    
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
    
    '''
    
    # Ask about what kind of BPM is being calibrated
    #BPM_style = input("What style is the BPM's processing freq? ")
    my_instrument.write("STAR 170 MHZ; STOP 430 MHZ;OPC?")
    #my_instrument.write("CENT 300 MHZ; SPAN 60 MHZ;OPC?")
    my_instrument.write("S21")
    my_instrument.write("MARK1 300MHZ")
    #my_instrument.write("SEAMAX")
    result = my_instrument.ask_for_values("OUTPMARK")
    #result = my_instrument.read_values()
    #result = my_instrument.read()
    print(result)
    mag, phase, frequency = result
    print("magnitude is %sdB, phase is %s degree, at %.3eHz" %(mag, phase, frequency))
    
 '''   
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