'''
Created on Mar 18, 2013

@author: charliex
'''
from Tkinter import *
from NWA_Mod import *

class NWA_GUI():
    '''
    GUI Interface for BPM characterization test
    
    '''
    def __init__(self):  
        root = Tk()      
        self.inst=BPM_NWA()
        
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        root.config(menu=menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        frame = Frame(root)
        frame.pack()
        
        self.title = Label(frame,text="Welcome to the SLAC BPM characterization program!", fg="red", font=("Arial",20,'bold'))
        self.title.pack()
        
        self.instruct = Label(frame,text="Please follow the steps:", font =("Times", 16))
        self.instruct.config(justify="left",)
        self.instruct.pack(anchor='w')
        
        self.gpib_init = Label(frame,text="1. Initial GPIB link to the Network Analyzer (NWA)\n    Click on the button to start the process", font = (12))
        self.gpib_init.config(justify="left")
        self.gpib_init.pack(anchor='w')
        
        self.GPIB_go = Button(frame, text="Init GPIB")
        self.GPIB_go.bind("<Button-1>",self.GPIB_init)
        self.GPIB_go.pack(anchor='w')
        
        root.mainloop()

    def GPIB_init(self,event):
        print("this is frustrating")
        self.frame1 = Toplevel()
        self.instr_list = self.inst.GPIB_fetch()
        #self.instr = Label(self.frame1,text=("Here are the instruments connected to the PC:\n %s" % self.instr_list),font=(12))
        #self.instr.pack()        
        
        
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
    
    