# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:00:03 2015

@author: Patrizio


                                IN RISCRITTURA
    
    
    
"""


from __future__ import division #unicode_literals, division

import Risposta
import TextToSpeechNew

import os
import time
import glob


class ChatBot():
    def _tipoClasse(self):
        return "Chat"
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
    def __init__(self):
        self.folder="risorse\\Dati\\"
        self.folderdialoghi=self.folder+"dialoghi\\"

        self.comandiChat=[u"help", u"comandi", u"esci"]#.split()        
        self.chatSymbol=u'>> '        
        self.attore=None
        self.Risposta=None
        
        #TTS        
        self.ttsRate=95
        self.ttsVol=1.0
        self.ttsEngine=TextToSpeechNew.TextToSpeechNew(rate=self.ttsRate, vol=self.ttsVol)
        self.tts=False
        
        #DIALOGO
        self.dialogoFiles=self.getDlgFiles()

                
        self.AvviaChat()
        self.Chatta()


    def getDlgFiles(self):
        files=glob.glob(self.folderdialoghi+'*.dat')
        
        files=[os.path.basename(file) for file in files]
        files=[file[:-4] for file in files]
        
        return files
        
        
    ######## COMANDI CHAT ##################
  
    def __ScegliDlgFiles(self):
        def StampaDlgFiles():
            for i in xrange(len(self.dialogoFiles)):
                print i, self.dialogoFiles[i]
              
        exit=False
        while not exit:
            StampaDlgFiles()
            risp=raw_input(self.chatSymbol)
            try:
                risp=int(risp)
                if risp>=int(0) and risp<len(self.dialogoFiles):                
                    #carico il dialogo
                    dlgname=self.dialogoFiles[risp]
                    self.Risposta=Risposta.Risposta(dlgname)
                    print "caricato script di: ", dlgname
                    
                    exit=True
            except:
                pass


    def __Comandi(self):        
        def StampaComandi():
            print
            print "COMANDI CHAT"
            print 
            print "1 - Cambia script dialogo"
            print "2 - Modifica Parametri tts"
            print "3 - Ritorna alla chat"
            print
            
        exit=False
        while not exit:
            StampaComandi()
            risp=raw_input(self.chatSymbol)
            try:
                risp=int(risp)
                if risp==1:
                    self.__ScegliDlgFiles()
                    exit=True

                elif risp==2:
                    self.__ComandiTts()
                    exit=True
                    
                elif risp==3:
                    exit=True

            except:
                pass


    def __ComandiTts(self):
        def StampaComandi():
            print
            print "COMANDI TTS"
            print 
            print "1 - Attiva o Disattiva tts"
            print "2 - imposta Volume"
            print "3 - imposta Rate"
            print "4 - Ritorana alla chat"
            
        exit=False
        
        while not exit:
            StampaComandi()
            risp=raw_input(self.chatSymbol)
            try:
                risp=int(risp)
                if risp==1:
                    self.tts=not self.tts                    
                    print 'engine tts stato:', self.tts                    
                    exit=True
                    
                elif risp==2:
                    print 
                    vol=raw_input("inserisci un valore da 1 a 100: ")
                    try:
                        if vol>=0 and vol<=100:
                            vol=float(vol)/100
                            self.setTtsEngineVol(vol)
                        else:
                            print "valore non valido, volume impostato a 100"
                            self.setTtsEngineVol(float(1))
                            
                    except:
                        print "valore non valido, volume impostato a 100"
                        self.setTtsEngineVol(float(1))
                    exit=True                        

                elif risp==3:
                    print 
                    rate=raw_input("inserisci un valore da 1 a 100: ")
                    try:
                        rate=int(rate)
                        self.setTtsEngineRate(rate)
                    except:
                        print "valore non valido, rate impostato a 95"
                        self.setTtsEngineRate(95)
                    exit=True
                    
                elif risp==4:
                    exit=True
            except:
                pass


    ######## TEXT TO SPEECH ###########    
    def setTtsEngineRate(self, rate=95):
        if rate>=0 and rate <=100:
            self.ttsEngine.setRate(rate)
        
        
    def setTtsEngineVol(self, vol=1.0):
        if vol>=float(0) and vol<=float(1):        
            self.ttsEngine.setVol(vol)
    ##################################        
            
            
    def __StampaBenvenuto(self):            
        print "benvenuto nella ScriptChatBot" 
        print
        print "Patrizio Bellan"
        print "matricola 123037"
        print
        print
        
    def __StampaIstruzioniChat(self):
        print " ISTRUZIONI ".center(75,'#')
        print 
        print "digita: help     ->  stampa a video questa schermata"
        print "digita: comandi  ->  accedi alle impostazioni della chat"
        print "digita: esci     ->  esci dalla chat"
        print

   
    def __ChiediNome(self):
        self.attore=raw_input('Ciao, come ti chiami?: ')
        self.__StampaSaluto()
       
       
    def __NonHoCapito(self):
        return "Scusa ma non ho capito"


    def __StampaSaluto(self):   
        print          
        print "ciao ", self.attore        
        print 
       
    def AvviaChat(self):    
        self.__StampaBenvenuto()
        self.__StampaIstruzioniChat()
        self.__ChiediNome()
        
        self.__ScegliDlgFiles()
        
        
    def Chatta(self):
        #ciclo infinito da cui esco solo volontariamente
        esci=False
        while not esci:
            userdlg=raw_input(self.chatSymbol)      
            try:
                userdlg=unicode(userdlg)
            except:
                userdlg=[w for w in userdlg.split() if (w.isalnum() or w==u" ")]
            
            if userdlg in self.comandiChat:
                if userdlg==u"help":
                    self.__StampaIstruzioniChat()
                    
                if userdlg==u"comandi":
                    self.__Comandi()            

                if userdlg==u'esci':
                    esci=True
            else:
                if len(userdlg)>0:
                    risp= self.Risposta.Risposta(userdlg)
                    
                    print risp                    
                    if self.tts:
                        self.ttsEngine.Read(risp)
                                
        #Fine Chat
        self.__StampaSaluto()
        
        
if __name__=='__main__':
    a=ChatBot()    
   
    