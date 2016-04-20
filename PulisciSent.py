# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 00:21:39 2015

@author: Patrizio
"""

from __future__ import unicode_literals


import SaveLoad
import re

class PulisciSent():
    def __init__(self):
        self.__folder="risorse\\Dati\\"
        self.stopWordFilename=self.__folder+"StopWords.list"
        self.stopWords=SaveLoad.LoadByte(self.stopWordFilename)
        
    def Pulisci(self, sent):
        #nelle sent tengo solo i caratteri ' , . : ; ! ?        
        ls=list(u"',.:;!?")        
        sent=unicode(sent)
        for k in ls:
            sent=sent.replace(k,u" "+k+u" ")
        for s in sent:
            if not s.isalpha():
                if not s in ls and s not in str(range(10)):
                    sent=sent.replace(s,u" ")
        sent=re.sub(r'[\s]{2,}',u" ",sent)
        sent=sent.lower()
        sent=sent+u"\n"
        return sent    

    def PulisciStopWords(self, sent):
        sent=self.Pulisci(sent) 
        sent=[w for w in sent.split() if (w not in self.stopWords)]
        sent=u" ".join(sent)
        sent=sent.strip()
        return sent
        
        
    def PulisciFilename(self, filename, nchar=100):
        ####fallo proporzionale con la discesa della frequenza.
        ####più sono frequenti contestualmente più le elimino per arrivare ad una lunghezza prefissata
        ####la lunghezza la devo rapportare ad un massimo di caratteri come nome file
        ####di default: 100
        filename=self.Pulisci(filename)
        for i in xrange(len(filename)):
            if not filename[i].isalpha():        
                if not filename[i] in str(range(10)) or filename[i]==u",":
                    filename=filename.replace(filename[i],u" ")
                
        filename=re.sub(r'[\s]{2,}',u" ",filename)
        filename=filename.lower().strip()
        
        return filename
    
if __name__=='__main__':
    a=PulisciSent()
    s=u"sentenc51734!e.di:prova--*/!£$%&/()=?^"
    print a.Pulisci(s)  
    print 'ora test stop words'

    s='casso sid di si sid dis di e la in si è sono io cioasdiooja oiaiofn iosdfio f cassa sono sonno'
    print a.PulisciStopWords(s)           
    
    filename=u'risorse\\Dati\\answers\\perch\xe9 alcune persone comprano fiat fanno finta capire o capiscono comprare fiat equivale comprare italiano , comprare italiano equivale far crescere nostra economia invece molta gente no , sbatte lamenta , chiama sua patria 39 39 itaglia 39 39 poi va vedersi prime americanate comprarsi macchine tedesche , francesi giapponesi questa gente forse sa comprare prodotti nostrani equivale far aumentare nostra economia , perch\xe9 vende deve produrre.yahootopic'
    
    filename="12,3. e il eeee fff f55454: ?"    
    f=a.PulisciFilename(filename)
    print len(f)
    print f
    