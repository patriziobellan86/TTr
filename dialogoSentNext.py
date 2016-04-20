# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 04:16:33 2015

@author: Patrizio
"""
from __future__ import unicode_literals

import SaveLoad
import AnalizzatoreSents
import PulisciSent

import time
import collections
import glob
import copy

class dialogoSentPrecendeteSuccessiva():
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
    def __init__(self, fileDialogo):
        self.soglia=1
        
        self.Analizzatore=AnalizzatoreSents.AnalizzatoreSents()
        self.pulisci=PulisciSent.PulisciSent()
        
        self.sentsentSuccessiva=collections.defaultdict(list)
        
        self.__ElaboraFile(fileDialogo)
        
        self.dlg=self.FiltraRisultati(self.soglia)
        
        
    def __ElaboraFile(self, file):        
        dlg=SaveLoad.LoadLines(file)
        if dlg:
            for j in xrange(len(dlg)-1):   #-1 perchè non devo fare l'ultima!
                k=self.getSent(dlg[j])
                v=self.getSent(dlg[j+1])
                k=u"".join(k)
                k=k.strip()
                
                v=u"".join(v)
                v=v.strip()

                self.sentsentSuccessiva[k].append(v)
            
                
    def getSent(self, sent):
        """
        
            get Tag Sent
            
            input: list(tuple(word,tag))
            output: list(word)
        
        """
        
        return [tupla[0] for tupla in sent]
    
    

    def FiltraRisultati(self, soglia):
        dlgClean=collections.defaultdict(list)        

        sents=self.sentsentSuccessiva.keys()
#        i=float(1)
#        tot=len(sents)
        for k in sents:
            try:
                tmprank=set()
#                print 'rank',i,'/',tot
                tmpvalues=list()
                if len(self.sentsentSuccessiva[k])>=soglia:
                    for sent in self.sentsentSuccessiva[k]:
                        sentence=self.Analizzatore.Analisi(sent)
                        sentence=u" ".join(sentence[0])                     
                        tmpvalues.append(sentence) 
                        
#                        tmprank=copy.deepcopy(tmpvalues)
                        tmprank=set(tmpvalues)
                    for v in enumerate(tmprank):
                        if tmpvalues.count(v[1])>=soglia:
                            dlgClean[k].append(self.sentsentSuccessiva[k][v[0]])            
            except:
                pass        
#            i+=1
#            
#            
#        print
#        print 
#        print 
#        print dlgClean
#        print
#        print
#        
        return dlgClean
        
                        
if __name__=='__main__':      
    print time.asctime()
    file="C:\\Esame TTR\\risorse\\Dati\\dialoghi\\dialoghiRaw\\american horror story.txt"
    a=dialogoSentPrecendeteSuccessiva(file)
 
    print time.asctime()
    print len(a.dlg)
        
    print 'done'