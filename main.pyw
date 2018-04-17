import myParser
import urllib.request
import time
from tkinter.messagebox import askquestion,showerror,showinfo
from tkinter import Tk
from webbrowser import open_new
from hashlib import md5
import os

FAIL=0
SUCCESS=1


class stack():
    def __init__(self):
        self.sta=[]
    def push(self,item):
        self.sta.append(item)
    def pop(self):
        return self.sta.pop()
    def ifEmpty(self):
        if len(self.sta)==0:
            return True
        else:
            return False

def refresh():
    page=urllib.request.urlopen('http://www.jwc.sjtu.edu.cn/web/sjtu/198076.htm')
    pageF=page.read().decode(encoding="gb2312",errors="strict")
    getinfo=myParser.myParser()
    getinfo.feed(pageF)
    result=getinfo.getResult()
    return result

def refreshData(result):
    db=open('data','r')
    db.seek(0)
    dbMd5=db.read(32)
    k=0
    for item in result:
        if dbMd5 == md5((item[0]).encode()).hexdigest():
            break
        else:
            k+=1
    db.close()
    db=open('data','w')
    LatestMD5=md5((result[0][0]).encode()).hexdigest()
    db.write(LatestMD5+'\n')
    for items in result:
        db.write(items[0]+'\n')
        db.write(items[1]+'\n')

    return k

def main():
    init=False
    if os.path.exists('init'):
        init=True

    if not os.path.exists('data'):
        data=open('data','w')
        data.close()

    root=Tk()
    root.withdraw()
    while True:
        result=refresh()
        news=refreshData(result)
        mesgBox=stack()
        if news>0:
            i=0
            while (i < news):
                mesgBox.push(result[i])
                i+=1
            log=open('log.log',mode='a')
            log.write(str(i)+" piece(s) of news updated"+(time.strftime('%X %x '))+'\n')
            log.close()
        else:
            log=open('log.log',mode='a')
            log.write("Nothing new    "+(time.strftime('%X %x'))+'\n')
            log.close()

        while not mesgBox.ifEmpty() :
            info=mesgBox.pop()
            if init:
                flag=askquestion('教务处的新通知',info[0]+'\n'+"是否查看？",icon='info')
                if flag=='yes':
                    open_new('http://www.jwc.sjtu.edu.cn/web/sjtu/'+info[1])

        if not init:
            init_file=open('init',mode='w')
            init_file.close()
            showinfo('First Start','jwcViewer 1.1 initialized.')

        time.sleep(300)


last_status=SUCCESS

while True:
    try:
        main()
        if last_status==FAIL:
            last_status=SUCCESS
            log=open('log.log',mode='a')
            log.write("Update Success   "+(time.strftime('%X %x'))+'\n')
            log.close()
    except:
         if last_status==SUCCESS:
             showerror('Error', 'Please check your network or update this program.')
             log=open('log.log',mode='a')
             log.write("Unknown Error    "+(time.strftime('%X %x'))+'\n')
             log.close()
             last_status=FAIL
         else:
             time.sleep(300)
    
