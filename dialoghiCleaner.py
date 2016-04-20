# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import unicode_literals


import SaveLoad
import PulisciSent

import glob
import codecs
import re

class DialogoghiSubFactoryCleaner():
    def __init__(self):
        self.folderRawSubfactory="risorse\\tmp\\subfactory\\"
        self.folderTMPClean="risorse\\tmp\\clean\\subfactory\\"
        
        self.list_char_del=re.compile(u"[''']") # ? , . ' : ; - _ ! £ $ % & / ( ) = \ | ")
    
    def CleanAllFile(self):
        files=glob.glob(self.folderRawSubfactory+'*')
        tot=len(files)  
        print tot
        i=float(0) 
        
        for fil in files:
            try:
                with codecs.open(fil,'r','cp1252') as f:
                    dati=f.readlines()
                self.CleanDialogo(dati)
            except:
                try:
                    with codecs.open(fil,'r','utf-8') as f:
                        dati=f.readlines()         
                    self.CleanDialogo(dati)
                except:
                    pass
            
            print "elaborazione file ",fil[len(self.folderRawSubfactory):], " - ",i, " / ", tot
            i=i+1        
            
#            if i>2:
#                print 'tmp ext'
#                break


    def CleanDialogo(self, dati):
        dlg=[]
        tmpdlg=[]
        for line in dati:
            try:
                n=int(line)
            except:
                #se non è un numero
                if line!=u'':
                    #re -> http://pythex.org/
                    if re.match('[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}?',line)==None:
                    #if not (line[2]==line[5] and line[2]==':'):
                        if line.strip().startswith(u"-"):
                            line=line[2:]
                            line=line+u"\n"
                            line=PulisciSent.PulisciSent().Pulisci(line)
                            dlg.append(line)
                            tmpdlg=[]
                        elif line.strip().endswith(u"."):
                            #aggiungo tutto il dialogo di un attore
                            line=PulisciSent.PulisciSent().Pulisci(line)
                            tmpdlg.append(line)
                            tmp=' '.join(tmpdlg)
                            tmp=tmp+'\n'
                            tmp=PulisciSent.PulisciSent().Pulisci(tmp)                            
                            dlg.append(tmp)
                            tmpdlg=[]
                        else:
                            line=PulisciSent.PulisciSent().Pulisci(line)
                            if len(line)>0:
                                tmpdlg.append(line)    
                                                
        filename=str(len(glob.glob(self.folderTMPClean+'*')))+u'.txt'
        filename=self.folderTMPClean+filename
        #dlg=[str(line).decode('utf-8') for line in dlg]

        #salvo il file  dei dialoghi
        with codecs.open(filename,'a','utf-8') as f:
            f.writelines(dlg)

if __name__=='__main__':
    import time
    t=time.asctime()
    a=DialogoghiSubFactoryCleaner()
    a.CleanAllFile()
    print t
    print time.asctime()
    print 'done'
    