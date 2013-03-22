'''
Created on Mar 18, 2013

@author: charliex
'''
from Tkinter import *
from NWA_Mod import *
import sys

class NWA_GUI():
    '''
    GUI Interface for BPM characterization test
    
    '''
    def __init__(self):
        #Initialize Tk and the BPM_NWA  
        root = Tk()      
        self.inst=BPM_NWA()
        
        #Create menu for exit
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        root.config(menu=menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        
        frame = Frame(root)
        frame.pack()
        #Title
        self.title = Label(frame,text="Welcome to the SLAC BPM characterization program!", fg="red", font=("Arial",20,'bold'))
        self.title.pack()
        
        self.instruct = Label(frame,text="Please follow the steps:", font=("Times", 16))
        self.instruct.config(justify="left",)
        self.instruct.pack(anchor="w")
        
        self.gpib_init = Label(frame,text="1. Initial GPIB link to the Network Analyzer (NWA)\n", font = (12))
        self.gpib_init.config(justify="left")
        self.gpib_init.pack(anchor="w")
        
        #NWA Calibration
        self.NWA_cal_label = Label(frame, text="2. Calibrating the NWA", font=(12))
        self.NWA_cal_label.pack(anchor="w") 
        self.NWA_cal_label.pi=self.NWA_cal_label.pack_info()
        self.NWA_cal_label.pack_forget()
        
        self.NWA_S21_label = Label(frame, text="3. Measuring S21", font=(12))
        self.NWA_S21_label.pack(anchor="w")
        self.NWA_S21_label.pi=self.NWA_S21_label.pack_info()
        self.NWA_S21_label.pack_forget()
        
        # S21 button
        self.NWA_S21_btn = Button(frame, text="Start S21 measurement", bg="green")
        self.NWA_S21_btn.bind("<Button-1>",
                              lambda event, GUI_list=[self.NWA_S21_label]:self.NWA_S21(GUI_list))
        self.NWA_S21_btn.pack()
        self.NWA_S21_btn.pi = self.NWA_S21_btn.pack_info()
        self.NWA_S21_btn.pack_forget()
        
        # Cal buttons
        self.NWA_cal_yes = Button(frame, text="Start Calibration", bg="green")
        self.NWA_cal_yes.bind("<Button-1>",
                              lambda event, GUI_list=[self.NWA_S21_label,self.NWA_S21_btn]:
                                self.NWA_Cal(GUI_list))
        self.NWA_cal_yes.pack()
        self.NWA_cal_yes.pi=self.NWA_cal_yes.pack_info()
        self.NWA_cal_yes.pack_forget()
        
        self.NWA_cal_no = Button(frame, text="Skip Calibration", bg="red", fg="white")
        self.NWA_cal_no.bind("<Button-1>",
                              lambda event, GUI_list=[self.NWA_S21_label,self.NWA_S21_btn]:
                                self.NWA_Calpass(GUI_list))
        self.NWA_cal_no.pack()
        self.NWA_cal_no.pi=self.NWA_cal_no.pack_info()
        self.NWA_cal_no.pack_forget()
        
        # Button to GPIB Init
        self.GPIB_go = Button(frame, text="Init GPIB", bg="red", fg="white")
        self.GPIB_go.bind("<Button-1>",
                          lambda event, GUI_list=[self.NWA_cal_label,self.NWA_cal_yes,self.NWA_cal_no]:
                          self.GPIB_init(GUI_list))
        self.GPIB_go.pack(anchor="center")
        root.mainloop()
    
    def GPIB_init(self,GUI_list):
        '''
        Pop up window to show if the HP8753C is found
        '''
        self.frame1 = Toplevel()
        self.manufact, self.model_num, self.ser_num, self.firm_ver, error = self.inst.GPIB_fetch()
        if error != 1:
            self.instr = Label(self.frame1, text=("GPIB device GPIB0::16 found.  \n Instrument is a %s %s, firmware version is %s. " % (self.manufact, self.model_num, self.firm_ver)))
            self.instr.pack()
        else:
            self.inst = Label(self.frame1, text=("HP8753C not found. \nPlease check connection with the HP8753C"))
            self.instr.pack()
        self.init_quit = Button(self.frame1, text="Exit", bg="red", fg="white",command=self.frame1.destroy)
        self.init_quit.pack()
        self.toggle(GUI_list)
            
    def NWA_Cal(self,GUI_list):
        '''
        Start the network analyzer calibration
        '''
        print("Let's start the calibration!")
        self.inst.NWA_cal()
        
        self.toggle(GUI_list)      
    
    def NWA_Calpass(self, GUI_list):
        '''
        Warn user about skipping calibration, give a choice to calibrate
        '''
        self.frame1 = Toplevel()
        self.calwarn_label = Label(self.frame1, text=("Calibration is needed for first time use!\n \
        Are you sure you want to skip the calibration?"), justify='center', fg='red',font=('bold',20))
        self.calwarn_label.pack()
        self.calwarn_skip = Button(self.frame1, text=("Yes"),bg="green", command=self.frame1.destroy)
        self.calwarn_skip.bind("<Button-1>",lambda event: self.toggle(GUI_list))
        self.calwarn_skip.pack(side=LEFT)
        self.calwarn_back = Button(self.frame1, text="I want to calibrate",bg="red",fg="white",command=self.frame1.destroy)
        self.calwarn_back.bind("<Button-1>",self.NWA_Cal)
        self.calwarn_back.pack(side=LEFT)

    def NWA_S21(self, GUI_list):
        print("Got you in NWA_S21")
        self.inst.S21_measure()        

    
    def toggle(self,GUI_obj_list):
        for GUI_handle in GUI_obj_list:
            GUI_handle.pack(GUI_handle.pi)   
        
        '''
        task_option = ("GPIB Init", "Network Analyzer Calibration", "S21 Measurement")
        var = StringVar()
        var.set("GPIB Init")
        self.dropoption = OptionMenu(frame, var, *task_option )
        self.dropoption.pack()
        
        def ok(tsk):
            tsk = var.get()
        self.tsk = 1
            
        self.task_confirm = Button(frame, text="Execute",command=(ok(self.tsk)))
        self.task_confirm.pack()
        '''
        
          


'''
        self.cal = Label(frame, text="1. Do you want to run the calibration process on the network analyzer?")
        self.cal.config(font = "12",justify="left",anchor="w")
        self.cal.pack(anchor="w")
        
        
        self.cal_sel = Button(frame, text="Yes", bg="green")
        self.cal_sel.pack(side = LEFT)
        
        self.cal_sel = Button(frame, text="No", fg="white", bg="red")
        self.cal_sel.pack(side = LEFT)
        
        '''
    
    