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

class dialoghiSentPrecendeteSuccessiva():
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
        self.soglia=3
        
        self.__SEPATATORE=u"\n[SEPARATORE]\n"
        self.Analizzatore=AnalizzatoreSents.AnalizzatoreSents()
        self.pulisci=PulisciSent.PulisciSent()
        
        self.__folder="risorse\\Dati\\"
        self.folderDialoghiPosTag=self.__folder+"dialoghi\\postag\\"
        self.folderDialoghi=self.__folder+u"dialoghi\\dlg\\"
        self.extFile=u".dialogo"
        
        self.SentSentFilename=self.__folder+"SentSent.dictlist"
        self.SentTagFilename=self.__folder+"SentTag.dictlist"
        
        #registro i tag delle frasi
        self.senttagSuccessiva=collections.defaultdict(list)
        #registro le sents
        self.sentsentSuccessiva=collections.defaultdict(list)
        
        self.__ElaboraFiles() 
   
    
        self.rankRes=self.RakingResults(self.soglia)
        
        
        self.__Save()
        
        
        
    def __ElaboraFiles(self):
        #elabora tutti i file
    
        #le frasi con solo i tag
        self.tagsent=list()
        #le frasi con solo le words
        self.sentsent=list()
        
        i=float(1)
        #files=glob.glob(self.folderDialoghiPosTag+u'*')
        files=["C:\\Esame TTR\\tutti i dialoghi.txt"]
        tot=len(files)  
        
        print tot
        for fil in files:
            print "elaborazione file ",fil[len(self.folderDialoghiPosTag):], " - ",i, " / ", tot
            
            #to del self.
            #self.dlg=SaveLoad.LoadByte(fil)
            self.dlg=SaveLoad.LoadLines(fil)
            if self.dlg:
                for j in xrange(len(self.dlg)-1):   #-1 perchè non devo fare l'ultima!
                    k=self.getSent(self.dlg[j])
                    v=self.getSent(self.dlg[j+1])
                    k=u" ".join(k)
                    k=k.strip()
                    
                    v=u" ".join(v)
                    v=v.strip()

                    self.sentsentSuccessiva[k].append(v)
            i+=1

#            if i>55:
#                break
            
    def RakingResults(self, soglia):
        dlgClean=collections.defaultdict(list)        

        sents=self.sentsentSuccessiva.keys()
        i=float(1)
        tot=len(sents)
        for k in sents:
            try:
                tmprank=set()
                print 'rank',i,'/',tot
                tmpvalues=list()
                if len(self.sentsentSuccessiva[k])>=3:
                    for sent in self.sentsentSuccessiva[k]:
                        sentence=self.Analizzatore.Analisi(sent)
                        sentence=u" ".join(sentence[0])                     
                        tmpvalues.append(sentence) 
                        
                        tmprank=copy.deepcopy(tmpvalues)
                        tmprank=set(tmprank)
                    for v in enumerate(tmprank):
                        if tmpvalues.count(v[1])>=soglia:
                            dlgClean[k].append(self.sentsentSuccessiva[k][v[0]])            
            except:
                pass        
            i+=1
            
            
        print
        print 
        print 
        print dlgClean
        print
        print
        
        return dlgClean
        
        
        
    def getTagSent(self, sent):
        """
        
            get Tag Sent
            
            input: list(tuple(word,tag))
            output: list(tag)
        
        """
        return [tupla[1] for tupla in sent]
        
        
    def getSent(self, sent):
        """
        
            get Tag Sent
            
            input: list(tuple(word,tag))
            output: list(word)
        
        """
        return [tupla[0] for tupla in sent]
    
    
    def __Save(self):
        print SaveLoad.SaveByte(self.rankRes,"self.rankRes")
        
	for i in self.rankRes.iteritems():
            for v in i:
		v=v+u"\n"
                SaveLoad.SaveLinesA(v, 'tutti i dialoghi k.txt')
        
        return
        
        
        #old 
        for k in self.rankRes.keys():        
            i=0
            try:
                for v in self.rankRes[k]:
                    try:
                        dati=k+self.__SEPATATORE+v
                        k=self.pulisci.PulisciFilename(k)
                        
                        #per evitar problemi con la lunghezza dei file                
                        if len(k)>90:
                            k=k[:90]
                        filename=self.folderDialoghi+k+str(i)+self.extFile                                
                        print "file: ", filename, "Saved:", SaveLoad.SaveLines(dati, filename)
                    
                        i+=1
                    except :
                        pass            
            except:
                pass        
        
        
        
#        print SaveLoad.SaveByte(self.sentsentSuccessiva,self.SentSentFilename)
#        print SaveLoad.SaveByte(self.senttagSuccessiva, self.SentTagFilename)
#            
#        for k in self.sentsentSuccessiva.keys():
#            i=0
#            try:
#                for v in self.sentsentSuccessiva[k]:
#                    try:
#                        dati=k+self.__SEPATATORE+v
#                        k=self.pulisci.PulisciFilename(k)
#                        
#                        #per evitar problemi con la lunghezza dei file                
#                        if len(k)>220:
#                            k=k[:220]
#                        filename=self.folderDialoghi+k+str(i)+self.extFile                                
#                        print "file: ", filename, "Saved:", SaveLoad.SaveLines(dati, filename)
#                    
#                        i+=1
#                    except :
#                        pass            
#            except:
#                pass

                        
if __name__=='__main__':      
    print time.asctime()
    
    a=dialoghiSentPrecendeteSuccessiva()
 
    print time.asctime()
    
        
    print 'done'