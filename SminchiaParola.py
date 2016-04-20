# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 14:00:17 2015

@author: Patrizio
"""

import collections

class SminchiaParola(object):
    
    def __init__(self):
        """
        questa classe deframmenta le parole
        da tecno a tcn, tecn, teno, tcno
        #così ho dei riferimenti se scrivo male una parola, riesco a ricollegarla velocemente
        
        """
        self.parolasminchiata=[]
        
    def Sminchia(self, parola):
        self.parola=parola
        
        parola=parola.lower()
        vocali=u'aeiou'
        lettere=[l for l in parola]
        
        #levo una vocale per volta
        for voc in vocali:
            parolasminchiata=parola.replace(voc,u'')
            if parolasminchiata!=parola:
                self.parolasminchiata.append(parolasminchiata)
        

        #levo tutte le vocali
        parolasminchiata=parola
        for voc in vocali:
            parolasminchiata=parolasminchiata.replace(voc, u'')
        self.parolasminchiata.append(parolasminchiata)

        #levo una lettera alla volta
        for l in lettere:
            parolasminchiata=parola.replace(l,u'')
            self.parolasminchiata.append(parolasminchiata)
            
        return self.parolasminchiata

    def SminchiaDict(self, parola):
        self.Sminchia(parola)
        spd=collections.defaultdict(list)
        spd[parola]=self.parolasminchiata
        
        return spd
            
if __name__=='__main__':
    a=SminchiaParola()
    c=a.Sminchia('zoofilo')
    
    print c
    
    d=a.SminchiaDict('erogatore')
    
    print d