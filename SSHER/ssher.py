#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 16:02:49 2020

@author: mfry5
"""

#import tkinenter as tk
import tkinter as tk
from tkinter import ttk
from pystassh import session as COMM
from gridmaster import gridmaster as GM
from os import path
import numbers
import json
#import getpass
#import sys
#import telnetlib


class ssher(tk.Tk):
    def __init__(self):  
        super().__init__()
        self.title("SSHER tool for SSH stuff")
        self.geometry("800x800")
        self.DB = dber(".sshercache")
        self.text = tk.Text(self)
        self.loading = True
        
        #topon/Label Styles
        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("L.Label", foreground="purple", background="lightgrey", font=(None, 16), anchor="left")
        style.configure("B.TLabel", font=('Arial', 40))
        style.configure("B.Tbutton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("TEntry", foregound="black", background="white")
        style.configure("Treeview", font=(None,10))
        style.configure("Treeview.Heading", font=(None, 10))
        #Main Container Creations
        #MenuBar
        self.menubar = tk.Menu(self, bg="lightgrey", fg="black")

        self.config_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
        self.config_menu.add_command(label="HostConfig", command=self.showdataConfig, accelerator="Ctrl+L")
        self.menubar.add_cascade(label="Config", menu=self.config_menu)

        self.configure(menu=self.menubar)
       
        #MainFrames
        self.selectiondata = {}
        self.currentCOMM_label = ttk.Label(self, text="DISCONNECTED")
        self.COMM_entry = ttk.Combobox(self, font=(None, 16))
        self.refreshDB_but = ttk.Button(self, command=self.dbref,text="refresh DB",  style="B.TButton")
        self.connect_but = ttk.Button(self, command=self.testbutt,text="Connect",  style="B.TButton")
        self.dconnect_but = ttk.Button(self, command=self.exitSess,text="Disconnect",  style="B.TButton")
        self.host_label = ttk.Label(self, text="Host:")
        self.port_label = ttk.Label(self, text="Port:")
        self.test_entry = ttk.Entry(self, font=(None, 16))
        self.currentCOMM_label.pack(fill=tk.X, padx=50)
        self.COMM_entry.pack(fill=tk.X, padx=50)
        self.refreshDB_but.pack(fill=tk.X, padx=50)
        self.connect_but.pack(fill=tk.X, padx=50)
        self.dconnect_but.pack(fill=tk.X, padx=50)
        self.host_label.pack(fill=tk.X, padx=50)
        self.port_label.pack(fill=tk.X, padx=50)
        self.test_entry.pack(fill=tk.X, padx=50)
        self.COMM_entry["values"]=self.retbetterlist(self.DB.data)
        
        self.COMM_entry.bind("<<ComboboxSelected>>", self.setselection)
        
    def showdataConfig(self):
        passtup =[]
        for  k in self.DB.data.keys():
            passtup.append(k)

  
        GM(self,self.DB.data,"COMM",passtup)
     
    def sesscreate(self):
       
        self.Sess = COMM.Session(self.selectiondata["host"],self.selectiondata["UN"],self.selectiondata["PW"],'',self.selectiondata["port"])
        self.Sess.connect()
              
    def commandpass(self,command):
        
    
        self.text.insert(tk.END, self.Sess.execute(command).stdout)
        
        self.text.pack()
    def exitSess(self):
        self.Sess.disconnect()
    
    def dbref(self):
        self.DB.jread(self.DB.path)
        
    def retbetterlist(self,dicttoret):
        retlist=[]
        for k,j in dicttoret.items():
            retlist.append(k)
        return retlist
        
        
    def setselection(self,args=None):
        self.host_label["text"] = self.DB.data[self.COMM_entry.get()]["host"]
        self.port_label["text"] = self.DB.data[self.COMM_entry.get()]["port"]

    def testbutt(self):
        self.testwindowPopulate(self.selectiondata)
            
    
    def testwindowPopulate(self, mydict):
        self.text.delete(1.0, tk.END)
        if type(mydict)==dict:
            for i,j in mydict.items():
                self.text.insert(tk.END, str(i) +"---"+str(j)+"\n")
        if type(mydict)==tuple:
            for i, j in mydict:
                for k, l in j.items():
                    self.text.insert(tk.END, str(k) +"---"+str(l)+"\n")
        if type(mydict)==list:
            for i in mydict:
                for j, k in i.items():
                    self.text.insert(tk.END, str(j) +"---"+str(k)+"\n")
        self.text.pack()    
    def showConfig(self):
        userinfoWind = tk.Tk()
        userinfoWind.title("SSH host data")
        userinfoWind.geometry("400x300")
        lblconnName = ttk.Label(userinfoWind, text ="ConnectionName")
        connNamebox = ttk.Entry(userinfoWind, show=None, font=('Arial',14))
        typeBox = ttk.Combobox(userinfoWind,font =('Arial',14))
        typeBox["values"]=['SSH','TELNET','SERIAL']
        lblUN = ttk.Label(userinfoWind, text ="Username")
        unbox = ttk.Entry(userinfoWind, show=None, font=('Arial',14))
        lblPW = ttk.Label(userinfoWind, text ="Password")
        pwbox = ttk.Entry(userinfoWind, show='*', font=('Arial',10))
        lblhost= ttk.Label(userinfoWind, text ="HOST")
        hostbox = ttk.Entry(userinfoWind, show=None, font=('Arial',10))
        lblport= ttk.Label(userinfoWind, text ="PORT")
        portbox = ttk.Entry(userinfoWind, show=None, font=('Arial',10))
        portbox.insert(0,"22")
        lblbaud =ttk.Label(userinfoWind,text="BAUD")
        baudbox = ttk.Entry(userinfoWind, show=None, font=('Arial',10))
        lblcport =ttk.Label(userinfoWind,text="COMMport")
        cportBOX = ttk.Entry(userinfoWind, show=None, font=('Arial',10))
        
        typeIndex=0
        
        def addhostdata(connName,newhostdata):
            if typeIndex == 0:
                newhostdata["commType"]=0
                newhostdata["commport"]=""
                newhostdata["buad"]=""
            if typeIndex == 1:
                newhostdata["commType"]=1
                newhostdata["UN"]=""
                newhostdata["PW"]=""
                newhostdata["commport"]=""
                newhostdata["buad"]=""
            if typeIndex == 2:
                newhostdata["commType"]=2
                newhostdata["host"]=""
                newhostdata["port"]=0
                newhostdata["UN"]=""
                newhostdata["PW"]=""
                newhostdata["commport"]=cportBOX.get()
                newhostdata["buad"]=baudbox.get()
                
            self.DB.jappend(connName,newhostdata)

        gobutton = ttk.Button(userinfoWind, text="Submit", command=lambda: addhostdata(connNamebox.get(),{"commType":0,"host":str(unbox.get()),"UN":str(pwbox.get()),"PW":str(hostbox.get()),"port":str(portbox.get()),"buad":0,"commPort":0}), state="enabled", style="B.TButton")
        #gobutton["command"]= insertUser(0,unbox.get(0),pwbox.get(0),tok1box.get(0),tok2box.get(0))
        #tok2box.bind("<Enter>",dber.insertUser(0,unbox.get(),pwbox.get(),tok1box.get(),tok2box.get()))
        lblconnName.pack()
        connNamebox.pack()
        typeBox.pack()
        lblUN.pack()
        unbox.pack()
        lblPW.pack()
        pwbox.pack()
        lblhost.pack()
        hostbox.pack()
        lblport.pack()
        portbox.pack()
        lblbaud.pack()
        baudbox.pack()
        lblcport.pack()
        cportBOX.pack()
        gobutton.pack()
        
        def hideVisual():
            if typeBox.get()=="TELNET":
                 unbox.config(state='disabled')
                 pwbox.config(state='disabled')
                 cportBOX.config(state='disabled')
                 baudbox.config(state='disabled')
                 typeIndex = 1
            if typeBox.get()=="TELNET":
                 unbox.config(state='enabled')
                 pwbox.config(state='enabled')
                 typeIndex = 0
            if typeBox.get()=="Serial":
                 unbox.config(state='disabled')
                 pwbox.config(state='disabled')
                 cportBOX.config(state='enabled')
                 baudbox.config(state='enabled')
                 typeIndex = 2
        
        typeBox.bind("<<ComboboxSelected>>",  hideVisual())
        notebook = ttk.Notebook(userinfoWind)
        tab_trees = {}
        
        
        
        style = ttk.Style()
        style.configure("Treeview", font=(None,10))
        style.configure("Treeview.Heading", font=(None, 10))
        tab = tk.Frame(notebook)
        groupkeys= ()
        dspvals = ()
        for key,vals in self.data.items():
            dspvals+=(vals,)
            if key not in groupkeys:
                groupkeys+=(key,)
        tree = ttk.Treeview(tab, columns=groupkeys, show="headings") 
        for heads in groupkeys:
            tree.heading(heads, text= heads)
            tree.column(heads, anchor="center")
        
            tree.insert("", tk.END, values=dspvals)
            tab_trees[0] = tree
            notebook.add(tab, text= "host"+heads)
            tree.pack()
            notebook.pack(fill=tk.BOTH, expand=1)
        userinfoWind.protocol("WM_DELETE_WINDOW", userinfoWind.destroy)
        userinfoWind.mainloop() 
        hideVisual()
        


            
            


class dber():
    def __init__(self,dbloc):
        self.path = dbloc
        if path.exists(dbloc):            
            self.data = self.jread(dbloc)
        else:
            self.firstTimeDB()
    
    def firstTimeDB(self):
        newdict = {}
        newdict["localSSH"]= {"commType":0,"host":"127.0.0.1","UN":"","PW":"","port":22,"baud":"","commPort":""}
        self.jdump(newdict,self.path)
        self.data = self.jread(self.path)
        
 
    #JSON data work
    
    def _json(self,response, status_code):
        """Extract JSON from response if `status_code` matches."""
        if isinstance(status_code, numbers.Integral):
            status_code = (status_code,)
    
        if response.status_code in status_code:
            return response.json()
        else:
            raise RuntimeError("Response has status "
                               "code {} not {}".format(response.status_code,
                                                       status_code))
    def jdump(self,jsondict, path):
        with open(path,"w") as jdumper:
            json.dump(jsondict, jdumper)
    
    def jread(self,path):
        with open(path) as jreader:
            return json.load(jreader)

    def jappend(self,connName,data1):
        self.data[connName] = data1
        self.jdump(self.data,self.path)
        self.data = self.jread(self.path)
        
if __name__ == "__main__":
    app = ssher()
    app.mainloop()


