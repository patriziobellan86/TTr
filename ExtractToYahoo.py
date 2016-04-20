# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 23:00:13 2015

@author: Patrizio
"""

from __future__ import unicode_literals



import SaveLoad
import YahooAnswer

import glob
import collections
import random


class ExtractToYahoo():
    def _tipoClasse(self):
        return "estrattore di dati"
    def _statoLavorazione(self):
        return "in testing"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "05/09\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"    
    def __init__ (self):
        self.qta=155
        
        
        self.__folder="risorse\\Dati\\"
        self.__foldertaggedsents =self.__folder+"training\\paisaTagged"
        self.wordsFreqFilename=self.__folder+"wordFreq.fdist"
        self.stopWordsFilename=self.__folder+"StopWords.list"
        self.folderDialoghiPosTag=self.__folder+"dialoghi\\postag\\"
        
        self.domandeMostFreqFilename=self.__folder+"domandeMostFreq.txt"
        self.sentimentiMostFreqFilename=self.__folder+"sentimentiMostFreq.txt"
        self.emozioniMostFreqFilename=self.__folder+"emozioniMostFreq.txt"
        
        self.wordsFreq=SaveLoad.LoadByte(self.wordsFreqFilename)
#        self.stopWords=SaveLoad.LoadByte(self.stopWords)
        
        self.noun=set()
        self.verb=set() 
        
        self.SentimentiMostFreq()
        self.EmozioniMostFreq()
        #domande prese da internet come "in-cultura" popolare e keywords di google
        self.DomaneMostFreq()
        
        #keywords prese dai dialoghi e mischiate random!
        self.ElaboraDati()
        self.EstraiMostFreq()    
        
        self.EstraiYahooAnswers(self.qta)
        
        
    def ElaboraDati(self):
        files=glob.glob(self.folderDialoghiPosTag+'*')
        tot=len(files)
        i=1
        
        for file in files:
            dati=SaveLoad.LoadByte(file)
            for line in dati:
                for word in line:
                    if word[1]==u"NOUN":
                        self.noun.add(word[0])
                    elif word[1]==u"VER":
                        self.verb.add(word[0])
            print "Elaborato", i, "/",tot
            i+=1
    
    
    def DomaneMostFreq(self):        
        lines=SaveLoad.LoadLines(self.domandeMostFreqFilename)
        for line in lines:
            try:
                print line
                keyRicerca=line.strip()
                _=YahooAnswer.YahooAnswer(answer=keyRicerca, ordinamento='rillevanza', numeroRisultati=1)
            except:
                pass
     
    def SentimentiMostFreq(self):        
        lines=SaveLoad.LoadLines(self.sentimentiMostFreqFilename)
        for line in lines:
            try:
                print line
                keyRicerca=line.strip()
                _=YahooAnswer.YahooAnswer(answer=keyRicerca, ordinamento='rillevanza', numeroRisultati=3)
            except:
                pass

    def EmozioniMostFreq(self):        
        lines=SaveLoad.LoadLines(self.emozioniMostFreqFilename)
        for line in lines:
            try:
                print line
                keyRicerca=line.strip()
                _=YahooAnswer.YahooAnswer(answer=keyRicerca, ordinamento='rillevanza', numeroRisultati=1)
            except:
                pass            
        
    def EstraiMostFreq(self):
        #Estraggo i 100 nome e verbi più frequenti nei dialoghi così da andarli  a 
        #estrarre tramite YahooAnswer
    
        #associo le frequenze
        frn=collections.defaultdict(list)
        frv=collections.defaultdict(list)
        
        for noun in self.noun:
            frn[self.wordsFreq[noun]].append(noun)
        for verb in self.verb:
            frv[self.wordsFreq[verb]].append(verb)


        self.frn=frn
        self.frv=frv

    def EstraiTop(self, diz, qta):
        frkeys=diz.keys()
        frkeys=sorted(frkeys)
        frkeys.reverse()
        
        if len(frkeys)>qta:
            frkeys=frkeys[:qta]
        
        return frkeys

    def EstraiYahooAnswers(self,qta):
        #scelgo un nome e un verbo a caso della lista per effettuare la ricerca
        nkey=self.EstraiTop(self.frn, qta)
        vkey=self.EstraiTop(self.frv, qta)
        
        for k in nkey:
            n=self.frn[k]
            v=self.frv[vkey[random.randint(0, qta-1)]]
            c=self.frn[nkey[random.randint(0, qta-1)]]
            
#            print n
#            print v
#            print c
            
            n=n[random.randint(0,len(n)-1)]
            v=v[random.randint(0,len(v)-1)]
            c=c[random.randint(0,len(c)-1)]
            
#            print n
#            print v
#            print c
            
            keyRicerca=u" ".join([n,v,c])
            print "ricerca tag: ", keyRicerca
            _=YahooAnswer.YahooAnswer(answer=keyRicerca, ordinamento='rillevanza', numeroRisultati=5)
            
            keyRicerca=u" ".join([c,v,n])
            print "ricerca tag: ", keyRicerca
            _=YahooAnswer.YahooAnswer(answer=keyRicerca, ordinamento='rillevanza', numeroRisultati=5)
            
        
if __name__=='__main__':
    a=ExtractToYahoo()
    
    print 'done'    