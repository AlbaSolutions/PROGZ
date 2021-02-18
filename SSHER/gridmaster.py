#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 08:50:29 2020

@author: AlbaSol
"""
import tkinter as tk
from tkinter import ttk
class gridmaster(tk.Toplevel):
    def __init__(self, master, data, title, groupby=None):
        super().__init__()
        self.title(title)
        self.geometry("300x500")

        if type(data)==dict:

            self.notebook = ttk.Notebook(self)
            self.tab_trees = {}
            style = ttk.Style()
            style.configure("Treeview", font=(None,10))
            style.configure("Treeview.Heading", font=(None, 10))
            groupkeys= ()
            dspvals = ()
            if groupby is not None:
                for l in groupby:
                    tab = tk.Frame(self.notebook)
                    for key,vals in data.items():
                            dspvals+=(vals,)
                            if key not in groupkeys:
                                groupkeys+=(key,)
                    tree = ttk.Treeview(tab, columns=groupkeys, show="headings")
                    for heads in groupkeys:
                        tree.heading(heads, text= heads)
                        tree.column(heads, anchor="center")

                    tree.insert("", tk.END, values=dspvals)
                    tree.pack(fill=tk.BOTH, expand=1)
                    self.tab_trees[l] = tree
                    self.notebook.add(tab, text=str(l))
                    self.notebook.pack(fill=tk.BOTH, expand=1)
                    groupkeys = ()
                    dspvals = ()

            else:
                tab = tk.Frame(self.notebook)
                for key,vals in data.items():
                    dspvals+=(vals,)
                    if key not in groupkeys:
                        groupkeys+=(key,)
                tree = ttk.Treeview(tab, columns=groupkeys, show="headings")
                for heads in groupkeys:
                    tree.heading(heads, text= heads)
                    tree.column(heads, anchor="center")
                tree.insert("", tk.END, values=dspvals)
                self.tab_trees[0] = tree
                self.notebook.add(tab, text= title)
                tree.pack()
                self.notebook.pack(fill=tk.BOTH, expand=1)
        if type(data)==list:
                self.titlebox = ttk.Label(self, text=title)
                self.testframe = ttk.Frame(self,width=200, height=200)
                self.textgen = tk.Text(self)
                self.titlebox.pack()


class dirMaster(tk.Toplevel):
    def __init__(self, master, localpath,webdata, title, groupby=None):
        super().__init__()
        self.title(title)
        self.geometry("300x500")
        self.notebook = ttk.Notebook(self)
        self.tab_trees = {}
        self.griddata =webdata
        style = ttk.Style()
        style.configure("Treeview", font=(None,10))
        style.configure("Treeview.Heading", font=(None, 10))
        tab = tk.Frame(self.notebook)
        groupkeys= ()
        dspvals = ()
        for key,vals in self.griddata.items():
            dspvals+=(vals,)
            if key not in groupkeys:
                groupkeys+=(key,)
        tree = ttk.Treeview(tab, columns=groupkeys, show="headings")
        for heads in groupkeys:
            tree.heading(heads, text= heads)
            tree.column(heads, anchor="center")
        if groupby:
            for dat in groupby:
                ct=0
                tree.insert("", tk.END, values=self.griddata[dat].items())
                tree.pack(fill=tk.BOTH, expand=1)
                self.tab_trees[ct] = tree
                self.notebook.add(tab, text=dat)
                ct+1
            self.notebook.pack(fill=tk.BOTH, expand=1)
        else:
            tree.insert("", tk.END, values=dspvals)
            self.tab_trees[0] = tree
            self.notebook.add(tab, text= title)
            tree.pack()
            self.notebook.pack(fill=tk.BOTH, expand=1)
