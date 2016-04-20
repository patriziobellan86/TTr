# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 05:02:16 2015

@author: Patrizio
"""

from __future__ import unicode_literals, division

import collections

import time

import SaveLoad
from MyClusters import Clusterizza
from SaveLoad import SaveByte, LoadLines
from RicercaOnlineSinonimi import RicercaOnlineSinonimi

class SinonimiContrariDataExtractor():
    def __init__(self):
        self.folderpath="risorse\\Dati\\"
        self.paroleFilename=self.folderpath+"parole.list"
        
        
        self.cercatore=RicercaOnlineSinonimi()  
        
        self.sinonimi=collections.defaultdict(list)
        self.contrari=collections.defaultdict(list)
        self.parole=list()        
        
        self.__Load()
        self.__EstraiDati()        
            
        self.__Save()
        
        
        
    def __EstraiDati(self):
        print len(self.parole)
        
        cercatore=RicercaOnlineSinonimi()
        for word in self.parole:
            try:
                print "elaborando: ", word
                sin, con=cercatore.RicercaSinonimiContrari(word)
              #  print word, sin, con
                
                if sin!=[]:
                    self.sinonimi[word].append(sin)
                if con!=[]:
                    self.contrari[word].append(con)
            except:
                #i caratteri come ' , . ! ? li ignoro e continuo
                pass
        return
        
        
#        
#        print 'clusterizzando sinonimi...'
#        self.clustersSinonimi=Clusterizza(self.sinonimi)
#        print 'clusterizzando contrari'
#        self.clustersContrari=Clusterizza(self.contrari)
#        print 'clusterizzando tutto...'
        
        #istr qui sotto è errata: se dict usare update!!!
#        self.sincon=list(self.sinonimi).extend(self.contrari)
#        self.clusters=Clusterizza(self.sincon)

    def __Save(self):
        print 'Salvando i dati'
        SaveByte(self.sinonimi,"SINONIMI.dictlist")        
        SaveByte(self.contrari,"CONTRARI.dictlist")
#        SaveByte(self.clustersSinonimi,"CLUSTERS sinonimi.pickle")
#        SaveByte(self.clustersContrari,"CLUSTERS contrari.pickle")        
#        SaveByte(self.clusters,"CLUSTERS.pickle")
#        
    def __Load(self): 
        self.parole=SaveLoad.LoadByte(self.paroleFilename)
        print len(self.parole)
        self.parole=sorted({i for i in self.parole})
        print len(self.parole)
#        i=1000
#        s=5000
#        self.parole=self.parole[s:s+i]
#        print 'test su ',i,'item'
        
        
if __name__=='__main__':
    print 'start', time.asctime()
    a=SinonimiContrariDataExtractor()
    
    print 'end', time.asctime()
    print 'done'

    print "PAPA' SPEGNI PURE LA CHIAVETTA CHE HO FINITO DI ELABORARE I DATI"
    
#    print a.sinonimi.keys()
#    print 
#    print 
#    print    
#    print a.contrari.keys()