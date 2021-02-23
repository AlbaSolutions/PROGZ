
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 08:11:58 2020

@author: AlbaSol
"""
import json
import numbers
import sqlite3

sql_create_user_table = """CREATE TABLE IF NOT EXISTS tbluser (
                            id integer PRIMARY KEY,
                            uname text,
                            pw text,
                            osfUID text,
                            baseurl text,
                            userurl text
                            );"""

sql_create_prjPath_table = """CREATE TABLE IF NOT EXISTS tblprjpath (
                            id integer PRIMARY KEY,
                            prjID text,
                            localPath text
                            );"""


def updateLocalPrjPath(ID, path):
    upq = "Update tblprjpath set localPath = ? where prjPathid = ?"
    runQuery(upq,(path,ID))


def insertPrj(prjid,path):
    sql = "insert into tblprjpath values (?,?,?)"
    runQuery(sql,(getnextKey("tblprjpath"),prjid,path))

def get_userinfo():
    return goodRows("Select * from tbluser")

def getPrjdir(prjid):
    selectPrj = "Select localPath from tblprjpath where prjID = ?"
    return goodRows(selectPrj,(prjid,))



def getnextKey(tbl):
    maxKey=0
    anyKey = goodRows("select max(id) as LastID from "+tbl)
    if anyKey['LastID'] is not None:
        maxKey= anyKey['LastID'] + 1
    return maxKey


def goodRows(sql,data=None):
    retRows ={}
    conn = sqlite3.connect(db)
    if data:
        cursor = conn.execute(sql,data)
    else:
        cursor = conn.execute(sql)
    columnz = [description[0] for description in cursor.description]
    rowz = cursor.fetchall()

    for rw in rowz:
        ct = 0
        while ct < len(columnz):
            retRows[columnz[ct]] =rw[ct]
            ct+=1
        ct =0

    return retRows
    conn.close()

def updateOSFUID(ID, OSFid):
    upq = "Update tbluser set osfUID = ? where id = ?"
    runQuery(upq,(OSFid,ID))

def insertUser(unid,UN,PW,OSFID,url):
    adduser = "INSERT INTO tbluser VALUES (?, ?, ?, ?, ?, ?)"
    runQuery(adduser,(unid, UN, PW, OSFID,url,url+"users/me"))

def setDB(dbloc):
    global db
    db = dbloc


def firstTimeDB(dbloc):
    setDB(dbloc)
    runQuery(sql_create_user_table)
    runQuery(sql_create_prjPath_table)


def runQuery(sql, data=None, receive=False):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    if data:
        cursor.execute(sql, data)
    else:
        cursor.execute(sql)

    if receive:
        return cursor.fetchall()
    else:
        conn.commit()

    conn.close()

#JSON data work

def _json(response, status_code):
    """Extract JSON from response if `status_code` matches."""
    if isinstance(status_code, numbers.Integral):
        status_code = (status_code,)

    if response.status_code in status_code:
        return response.json()
    else:
        raise RuntimeError("Response has status "
                           "code {} not {}".format(response.status_code,
                                                   status_code))
def jdump(jsondict, path):
    with open(path,"w") as jdumper:
        json.dump(jsondict, jdumper)

def jread(path):
    with open(path) as jreader:
        return json.load(jreader)
