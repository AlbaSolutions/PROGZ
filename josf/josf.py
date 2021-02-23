#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:55:04 2020

@author: AlbaSol
"""


import os
import sys
#import wrker.utils as util
import wrker.dber as dber
import wrker.webber as webber
import tkinter as tk
from wrker.gridmaster import gridmaster as GM
from tkinter import ttk
import tkinter.messagebox as msg
from tkinter import filedialog as DIA
from os import path


class josf(tk.Tk):
    def __init__(self):

        if path.exists("wrker/.josfcfg"):
            super().__init__()
            dber.setDB("wrker/.josfcfg")
            self.userinfo = dber.get_userinfo()
            if self.userinfo == None:
                self.showUsergen()
            else:
                self.title(self.userinfo["uname"] + " OSF Client")
                self.geometry("800x600")
                self.resizable(False, False)
                self.userdata = dber.get_userinfo()
                self.text = tk.Text(self)
                self.loading = True
                self.prjUrl= ""#self.userinfo["baseurl"]+"nodes/*PRJID*/files/osfstorage/"
                self.userPrjsURL = self.userinfo["baseurl"]+ "users/"+self.userinfo["osfUID"]+"/nodes/"
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
                self.menubar = tk.Menu(self, bg="lightgrey", fg="navy")
                self.prj_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
                self.prj_menu.add_command(label="view attributes", command=self.show_proj_windowATT)
                self.prj_menu.add_command(label="view links", command=self.show_proj_windowLink)
                self.prj_menu.add_command(label="view all", command=self.show_proj_windowLIST)
                self.user_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
                self.user_menu.add_command(label="View Userinfo", command=self.show_user_window, accelerator="Ctrl+U")
                self.menubar.add_cascade(label="ProjectLog", menu=self.prj_menu)
                self.menubar.add_cascade(label="User", menu=self.user_menu)
                self.configure(menu=self.menubar)
                #MainFrames
                self.topFrame = tk.Frame(self, width=500, height=600, bg="lightgrey")


                #Layout
                self.grid_rowconfigure(1, weight=1)
                self.columnconfigure(0,weight=1)

                self.topFrame.grid_rowconfigure(4,weight=1)
                self.topFrame.columnconfigure(0,weight=1)
                self.topFrame.grid(row=0,column=0,sticky="ew")




                #widget create
                       #Main Container Creations
                #MenuBar
                self.menubar = tk.Menu(self.topFrame, bg="lightgrey", fg="navy")
                self.prj_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
                self.prj_menu.add_command(label="view attributes", command=self.show_proj_windowATT)
                self.prj_menu.add_command(label="view links", command=self.show_proj_windowLink)
                self.prj_menu.add_command(label="view all", command=self.show_proj_windowLIST)
                self.user_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
                self.user_menu.add_command(label="View Userinfo", command=self.show_user_window, accelerator="Ctrl+U")
                self.menubar.add_cascade(label="ProjectLog", menu=self.prj_menu)
                self.menubar.add_cascade(label="User", menu=self.user_menu)
                self.configure(menu=self.menubar)
                #MainFrames
                self.prj_name_label = ttk.Label(self.topFrame, text="ProjectID:")
                self.prj_name_entry = ttk.Combobox(self.topFrame, font=(None, 16))
                self.refreshDB_but = ttk.Button(self.topFrame, command=self.dbref,text="JSONrefresh",  style="B.TButton")
                self.fetchPrj_but = ttk.Button(self.topFrame, command=self.testUP,text="PutProjectFile",  style="B.TButton")
                self.FilesInPrj_label = ttk.Label(self.topFrame, text="20", style="B.TLabel")


                self.NBFrame= tk.Frame(self)


                self.abspath = os.path.abspath(os.getcwd())

                #widget layout
                self.prj_name_label.grid(row=0, column=0,sticky="ew")
                self.prj_name_entry.grid(row=1, column=0,sticky="ew")
                self.refreshDB_but.grid(row=2, column=0,sticky="ew")
                self.fetchPrj_but.grid(row=3,column=0,sticky="ew")
                self.FilesInPrj_label.grid(row=4,column=0,sticky="ew")
                NBheadings = ("File","LocalSize","WebSize","LocalModified","WebModified")

                self.NBTree = ttk.Treeview(self,columns=NBheadings,show="headings")
                for heads in NBheadings:
                    self.NBTree.heading(heads,text=heads)
                    self.NBTree.column(heads,anchor="center")




                self.NBTree.grid(row=1,column=0,sticky="ew")
                self.NBFrame.grid(row=1,column=0,sticky="ew")


                self.prj_name_entry.bind("<<ComboboxSelected>>", self.dirchanger)



                self.bind("<Control-l>", self.show_proj_window)

                self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

                self.prj_name_entry.focus_set()
                if self.userinfo["osfUID"]=="NOTSET":
                    self.checkOSFID()
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

                if self.dbfilecheck():
                    self.usrprjsDB = dber.jread("wrker/dsource/prjs.json")
                else:
                    self.dbjsoncheck(False)
                self.prj_name_entry['values'] = self.genProList()
                self.prj_name_entry.focus_set()
                self.prj_name_entry.current(0)
                self.loading=False



        else:


            self.showUsergen()

    def testDown(self):
        filedict={}
        tempdict =dber.jread("wrker/dsource/"+self.prj_name_entry.get().split("_")[0]+".json")['data']
        for i in tempdict:
            filedict[i['attributes']['name']]=i['links']['download']
        sessGet = webber.webber(self.userinfo["baseurl"]+"files/")
        sessGet.basic_auth(self.userinfo["uname"],self.userinfo["pw"])

        for j,k in filedict.items():
            sessGet.DLfile(k,"tests/"+j)

    def testUPnew(self):
        pth= "tests/genesInCV19.csv"
        sessGet = webber.webber(self.userinfo["baseurl"])
        sessGet.basic_auth(self.userinfo["uname"],self.userinfo["pw"])
        with open(pth,"r") as localfile:
            data =localfile.read()
        sessGet.ULnewfile("genesInCV19.csv",self.prj_name_entry.get().split("_")[0],data)

    def testUP(self):
        fileupdate =""
        pth= "tests/genesInCV19.csv"
        tempdict =dber.jread("wrker/dsource/"+self.prj_name_entry.get().split("_")[0]+".json")['data']
        for i in tempdict:
            if i['attributes']['name']=="genesInCV19.csv":#pth.split("/")[len(pth.split("/"))]:
                fileupdate=i['links']['upload']
        sessGet = webber.webber(self.userinfo["baseurl"])
        sessGet.basic_auth(self.userinfo["uname"],self.userinfo["pw"])
        with open(pth,"r") as localfile:
            data =localfile.read()
        print(sessGet.put(fileupdate,data))

    def checkOSFID(self):
        if self.userinfo["osfUID"]=="NOTSET":
            msgbox= msg.askyesno(title="Missing osf web id", message="we need to get this from OSF, do you want to do this now?",parent=self)
            if msgbox:
                myid = self.getUserID()
                dber.updateOSFUID(self.userinfo["id"],myid)
            if not msgbox:
                msg.showinfo(title="Exiting app", message ="we need that ID for projects")
                sys.exit()
    def getUserID(self):

        path=self.userinfo["userurl"]

        sessGet= webber.webber(path)
        sessGet.basic_auth(self.userinfo["uname"],self.userinfo["pw"])
        bucky = dber._json(sessGet.get(sessGet.build_url('', '')), 200)

        return bucky['data']['id']
#
    def genProList(self):
        if self.dbfilecheck:
            lister =()
            for k in self.usrprjsDB['data']:
                lister+=(str(k['id'])+'_'+str(k['attributes']['title']),)
        return lister

    def show_proj_window(self, event=None):
        passdict =dber.jread("wrker/dsource/"+self.test_entry.get()+".json")['data']
        #self.testwindowPopulate(passdict)
        GM(self,passdict,"Project")

    def show_proj_windowATT(self):

        passdict ={}
        tempdict =dber.jread("wrker/dsource/"+self.prj_name_entry.get().split("_")[0]+".json")['data']
        ctr=0
        for i in tempdict:
            for key, val in i.items():
                if key == 'attributes':
                    for a, b in val.items():
                        passdict[str(ctr) +'-'+ a] = b
            ctr+=1

        GM(self,passdict,"Project Attributes",ctr)
        #self.testwindowPopulate(passdict)

    def show_proj_windowLIST(self):

        passdict ={}
        tempdict =self.usrprjsDB['data']
        ctr=0
        for i in tempdict:
            for key, val in i.items():
                if key == 'attributes':
                    for a, b in val.items():
                        passdict[str(ctr) +'-'+ a] = b
            ctr+=1

        GM(self,passdict,"All projects",ctr)

    def show_proj_windowLink(self):
        passdict ={}
        tempdict =dber.jread("wrker/dsource/"+self.prj_name_entry.get().split("_")[0]+".json")['data']
        ctr=0
        for i in tempdict:
            for key, val in i.items():
                if key == 'links':
                    for a, b in val.items():
                        passdict[str(ctr) +'-'+ a] = b
            ctr+=1

        GM(self,passdict,"Project links",ctr)

    def show_user_window(self, event=None):
        if self.userinfo["osfUID"]=="NOTSET":
            self.checkOSFID()
        GM(self,self.userinfo,self.userinfo["uname"])

    def dbref(self):
        for k in self.usrprjsDB['data']:
             self.lastprjUrl =self.userinfo["baseurl"]+"nodes/"+str(k['id'])+"/files/osfstorage/"
             dber.jdump(self.fetchjson(self.lastprjUrl),"wrker/dsource/"+str(k['id'])+".json")

    def dbfilecheck(self):
        good = True
        if os.path.exists("wrker/dsource/"):
                if os.path.exists("wrker/dsource/prjs.json"):
                    pass
                else:
                    good = False
        if not os.path.exists("wrker/dsource"):
            os.mkdir("wrker/dsource")
        return good




    def dbjsoncheck(self,refreshbit):
        if refreshbit:
            self.dbref()
        else:
            if os.path.exists("wrker/dsource/"):
                if os.path.exists("wrker/dsource/prjs.json"):
                    pass
                else:
                    dber.jdump(self.fetchjson(self.userPrjsURL),"wrker/dsource/prjs.json")
                self.usrprjsDB = dber.jread("wrker/dsource/prjs.json")
                for k in self.usrprjsDB['data']:
                    if os.path.exists("wrker/dsource/"+str(k['id'])+".json"):
                        pass
                    else:
                        self.lastprjUrl =self.userinfo["baseurl"]+"nodes/"+str(k['id'])+"/files/osfstorage/"
                        dber.jdump(self.fetchjson(self.lastprjUrl),"wrker/dsource/"+str(k['id'])+".json")







    def fetchjson(self,urltouse):
        print(urltouse)
        sessGet = webber.webber(urltouse)
        sessGet.basic_auth(self.userinfo["uname"],self.userinfo["pw"])
        return dber._json(sessGet.get(sessGet.build_url('', '')), 200)






    def showUsergen(self):
        userinfoWind = tk.Tk()
        userinfoWind.title("OSF Authentication Creds")
        userinfoWind.geometry("400x300")
        lblUN = ttk.Label(userinfoWind, text ="Username for OSF")
        unbox = ttk.Entry(userinfoWind, show=None, font=('Arial',14))
        lblPW = ttk.Label(userinfoWind, text ="Password")
        pwbox = ttk.Entry(userinfoWind, show='*', font=('Arial',10))
        lblOSFID= ttk.Label(userinfoWind, text ="OSF web user")
        boxOSFID = ttk.Entry(userinfoWind, textvariable="NOTSET", show=None, font=('Arial',10))
        boxOSFID.insert(0,"NOTSET")
        boxOSFID.config(state='disabled')
        lblurl= ttk.Label(userinfoWind, text ="BaseURL")
        urlbox = ttk.Entry(userinfoWind, show=None, font=('Arial',10))
        urlbox.insert(0,"https://api.osf.io/v2/")
        urlbox.config(state='disabled')
        def submitcommand():
            dber.firstTimeDB("wrker/.josfcfg")
            dber.insertUser("0",str(unbox.get()),str(pwbox.get()),str(boxOSFID.get()),str(urlbox.get()))
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        gotopon = ttk.topon(userinfoWind, text="Submit", command=submitcommand, state="enabled", style="B.Ttopon")
        #gotopon["command"]= insertUser(0,unbox.get(0),pwbox.get(0),tok1box.get(0),tok2box.get(0))
        #tok2box.bind("<Enter>",dber.insertUser(0,unbox.get(),pwbox.get(),tok1box.get(),tok2box.get()))
        lblUN.pack()
        unbox.pack()
        lblPW.pack()
        pwbox.pack()
        lblOSFID.pack()
        boxOSFID.pack()
        lblurl.pack()
        urlbox.pack()
        gotopon.pack()
        userinfoWind.protocol("WM_DELETE_WINDOW", userinfoWind.destroy )
        userinfoWind.mainloop()


    def process_directory(self, parent, path):
        treein = ()
        webitems = self.webgetattribs()
        with os.scandir(path) as dir_entries:
            for entry in dir_entries:
                abspath = os.path.join(path,entry)
                isdir = os.path.isdir(abspath)
                info = entry.stat()
                if not isdir:
                    if entry.name in webitems:
                        treein+=(entry.name,info.st_size,info.st_mtime,)

                #oid = self.dirtree.insert(parent, 'end', text=str(entry.name)+"-----SIZE:"+str(info.st_size/1024),open=False)
                #if isdir:
                  # self.process_directory(oid,abspath)


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


#        for p in os.listdir(path):
#            abspath = os.path.join(path, p)
#            isdir = os.path.isdir(abspath)
##            fileinfo = os.stat(p)
##            print(str(fileinfo))
#            oid = self.dirtree.insert(parent, 'end', text=p, open=False)
#            if isdir:
#                self.process_directory(oid, abspath)
    def dirchanger(self,args=None):
        dirpath = dber.getPrjdir(str(self.prj_name_entry.get().split("_")[0]))

        #print(dirpath)
        self.NBTree.delete(*self.localdir.get_children())
        if len(dirpath) > 0:
            self.NBlocaldir
            self.abspath = os.path.abspath(dirpath['localPath'])
            self.root_node = self.dirtree.insert('', 'end', text=self.abspath, open=True)
            self.process_directory(self.root_node, self.abspath)



        else:
            newpath = DIA.askdirectory()
            self.abspath = os.path.abspath(newpath)
            self.root_node = self.insert('', 'end', text=self.abspath, open=True)
            self.process_directory(self.root_node, self.abspath)
            dber.insertPrj(self.prj_name_entry.get().split("_")[0],newpath)


    def webgetattribs(self,args=None):
        coldata =[]
        passdict={}
        tempdict =dber.jread("wrker/dsource/"+self.prj_name_entry.get().split("_")[0]+".json")['data']

        for i in tempdict:
            for key, val in i.items():
                if key == 'attributes':
                    for a, b in val.items():
                        if a in ('name','size','date_modified'):
                            coldata.append([a,b])
        for i in coldata:
            if i[0] not in passdict.keys():
                passdict[i[0]]=i[1:]


        return passdict





    def safe_destroy(self):
        if hasattr(self, "worker"):
            self.worker.force_quit = True
            self.after(100, self.safe_destroy)
        else:
            self.destroy()

if __name__ == "__main__":
    app = josf()
    app.mainloop()
