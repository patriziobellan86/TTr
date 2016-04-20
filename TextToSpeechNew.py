# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 02:37:00 2015

@author: Patrizio
"""

from __future__ import unicode_literals

import pyttsx

class TextToSpeechNew():
    def _tipoClasse(self):
        return "tts"
    def _statoLavorazione(self):
        return "testata"
    def _dataUltimazione(self):
        return "23\06\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-b"
    
    def __init__(self, rate=95, vol=1.0):
        #parametrizzo il motore tts
        self.engine = pyttsx.init()
        self.setRate(rate)
        self.setVolume(vol)
                    
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    
    def Read(self, sent):
        self.engine.say(sent)
        self.engine.runAndWait()

        
    def setRate(self, rate):
        self.engine.setProperty('rate', rate)


    def setVolume(self, vol):
        self.engine.setProperty('volume', 1.0)
                
                
if __name__=='__main__':
    print 'test classe'
    a=TextToSpeechNew()
    a.Read('prova di lettura')