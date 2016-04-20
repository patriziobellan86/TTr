# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 02:57:51 2015

@author: Patrizio
"""

from __future__ import unicode_literals

import PulisciSent
import SaveLoad
import PosTagger_light

import glob
import codecs


class dialoghiPosTag():
    def __init__(self):
        self.folderDialoghiClean="risorse\\tmp\\clean\\subfactory\\"
        self.folderDialoghiPosTag="risorse\\Dati\\dialoghi\\postag\\"
        
        self.__pulisci=PulisciSent.PulisciSent()
        self.unkwords=[]
    
        self.pos=PosTagger_light.PosTagger()
      
        self.allPosTag()
         
         
    def allPosTag(self):
        i=float(1)
        tot=len(glob.glob(self.folderDialoghiClean+'*'))  
        ifile=len(glob.glob(self.folderDialoghiPosTag+'*'))

        for fil in glob.glob(self.folderDialoghiClean+u'*'):
            try:
                dlg=[]
                for line in SaveLoad.LoadLines(fil):
                    if len(line.strip())>0:
                        line=unicode(line)
                        line=line.lower()
                        l=self.pos.PosTag(line)
                        dlg.append(l)
                  
                #salvo il file postaggato e senza \n inutili
                filename=str(ifile)+u'.txt'
                filename=self.folderDialoghiPosTag+filename
                #salvo il file  dei dialoghi
                if SaveLoad.SaveByte(dlg,filename):
                    ifile+=1
                    
            except:
                #potrebbero esserci errori di qualsiasi natura nei file, in questo caso ignoro il file e passo al successivo
                pass
            
            print "elaborazione file ",fil[len(self.folderDialoghiClean):], " - ",i, " / ", tot
            i+=1
        
if __name__=='__main__':
    import time
    
    t=time.asctime()
    a=dialoghiPosTag()
    print time.asctime()
    
    print 'done'