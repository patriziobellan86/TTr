# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import unicode_literals


import SaveLoad
import PulisciSent

import os
import glob
import codecs
import re

class DialogoghiRawExtractor():
    def _tipoClasse(self):
        return "estrattore di dati"
    def _statoLavorazione(self):
        return "in testing"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "25\08\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"    

    def __init__(self):
        self.folderRawSubfactory="risorse\\tmp\\subfactory\\"
        self.folderTMPClean="risorse\\Dati\\dialoghi\\dialoghiRaw\\"
        
        self.list_char_del=re.compile(u"[''']") # ? , . ' : ; - _ ! £ $ % & / ( ) = \ | ")
    
        self.CleanAllFile()
        
    def CleanAllFile(self):
        files=glob.glob(self.folderRawSubfactory+'*')
        tot=len(files)  
        print tot
        i=float(0) 
        
        for fil in files:
            print "elaborazione file ",fil[len(self.folderRawSubfactory):], " - ",i, " / ", tot

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
                
            dlg=self.CleanDialogo(dati)
           
#            filename=fil[len(self.folderRawSubfactory):-4]
#            filename="".join([w for w in filename if w.isalpha()])
#            filename=filename[:-17]

            filename=self.CleanFilenameSubFactory(fil)
            filename=self.folderTMPClean+filename+u'.txt'
    
            #salvo il file  dei dialoghi
            SaveLoad.SaveLinesA(dlg,filename)    
            
            i=i+1             

                   
            
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
                    if re.match('[0-9]{1,}:[0-9]{1,}:[0-9]{1,},[0-9]{1,}?',line)==None:
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
                                
        return dlg

    def CleanFilenameSubFactory(self, filename):
    
#        filename='risorse\\tmp\\subfactory\\100.questions.s01e01.1x01.sub.ita.subsfactory.srt'
        index=filename.rfind('\\')+1
        filename=filename[index:]
        
#        filename='100.questions.s01e01.1x01.sub.ita.subsfactory.srt'
        
        filename=re.sub('\.srt','',filename)
        filename=re.sub('\.subsfactory','',filename)
        filename=re.sub('\.sub','',filename)
        filename=re.sub('\.ita','',filename)
        
        filename=re.sub('720[pP]','',filename)
        
        filename=re.sub('(s)\d{1,}(e)\d{1,}','',filename)        
        filename=re.sub('\d{0,}([xX])\d{1,}','',filename)
        
        filename=re.sub('\[(.*)\]','',filename)
        filename=re.sub('\((.*)\)','',filename)
        
        filename=re.sub('[\.-]',' ',filename)
        
        filename=filename.strip()
        
        return filename

"""
def CleanFilenameSubFactory(self, filename):

    filename='risorse\\tmp\\subfactory\\100.questions.s01e01.1x01.sub.ita.subsfactory.srt'
    index=filename.rfind('\\')+1
    filename=filename[index:]
    filename='100.questions.s01e01.1x01.sub.ita.subsfactory.srt'
    
    filename=re.sub('\.srt','',filename)
    filename=re.sub('\.subsfactory','',filename)
    filename=re.sub('\.sub','',filename)
    filename=re.sub('\.ita','',filename)
    
    filename=re.sub('(s)\d{1,}(e)\d{1,}','',filename)
    
    filename=re.sub('\d{0,}([xX])\d{1,}','',filename)
    filename=re.sub('\.',' ',filename)
    filename=filename.strip()
    
    return filename
    
'[Ita-Sub] MastersOfHorror - 1x12 - Sub Ita (a) (Sub4All)'
>>> g=re.sub('\[(.*)\]','',f)
>>> g
' MastersOfHorror - 1x12 - Sub Ita (a) (Sub4All)'
g=re.sub('\((.*)\)','',f)
>>> g
'[Ita-Sub] MastersOfHorror - 1x12 - Sub Ita '

"""       
if __name__=='__main__':
    import time

    a=DialogoghiRawExtractor()
    
    print time.asctime()
    print 'done'
   