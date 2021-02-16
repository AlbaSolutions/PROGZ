#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:02:58 2020

@author: mfry5
"""

#import wrker.utils as util
import serial as SER

import tkinter as tk



class scanny(tk.Tk):
    def __init__(self):
        
                self.title("SCANNY")
                self.geometry("800x600")
                self.resizable(False, False)
                self.loading = True
    
                #topon/Label Styles
                style = tk.ttk.Style()
                style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
                style.configure("L.Label", foreground="purple", background="lightgrey", font=(None, 16), anchor="left")
                style.configure("B.TLabel", font=('Arial', 40))
                style.configure("B.Tbutton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
                style.configure("TEntry", foregound="black", background="white")
                style.configure("Treeview", font=(None,10))
                style.configure("Treeview.Heading", font=(None, 10))
                #Main Container Creations
      
                #MainFrames
                self.topFrame = tk.Frame(self, width=500, height=600, bg="lightgrey")
                
                self.topFrame.pack()
             
                self.loading=False

    def selectUSB(self):
        pass
    def listComm(self):
       
        port = "\\\\.\\CNCA0"
        s = SER.Serial(port, 38400, timeout=0)

        while True:
            data = s.read(9999)
            if len(data) > 0:
                print('Got:', data)

            sleep(0.5)
            print('not blocked')

        s.close()
if __name__ == "__main__":
    app = scanny()
    app.mainloop()