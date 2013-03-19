'''
Created on Mar 13, 2013

@author: charliex
'''
# File: bind1.py
from Tkinter import *

root = Tk()
def callback(event):
    print "clicked at", event.x, event.y
    
frame = Frame(root, width=100, height=100)
frame.pack()

button = Button(root, text="Hello")
button.bind("<Button-1>", callback)
button.pack()

root.mainloop()