# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 06:07:22 2015

@author: Patrizio
"""

from __future__ import unicode_literals

import SaveLoad

import nltk


class paisaWordsDataExtractor():
    def _tipoClasse(self):
        return "estrattore di dati"
    def _statoLavorazione(self):
        return "in lavorazione"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "29\08\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"
    def __init__(self):
        self.__folder="risorse\\Dati\\"
        self.__foldertaggedsents =self.__folder+"training\\paisaTagged"
        self.wordsFreqFilename=self.__folder+"wordFreq.fdist"
        self.stopWordsFilename=self.__folder+"StopWords.list"
        
        self.__lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
        self.corpus=nltk.corpus.ConllCorpusReader(self.__foldertaggedsents,'.*',self.__lst_pos)
        
        self.wordsFreq=None
        self.stopWords=None
        
        self.__EstraiDati()
        
        self.__Save()
        
        
    def __EstraiDati(self):
        #tramite self.corpus posso estrarre tutti i dati che voglio
        self.wordsFreq=nltk.FreqDist(self.corpus.words())
        
        #modificare in modo proporzionale! per ora assumo le prime 50
        self.stopWords=[w[0] for w in self.wordsFreq.most_common(100) if w[0].isalpha()]
        
    def __Save(self):
        
        print SaveLoad.SaveByte(self.wordsFreq, self.wordsFreqFilename)
        print SaveLoad.SaveByte(self.stopWords,self.stopWordsFilename)
        
        
if __name__ =='__main__':
    import time
    
    print time.asctime()
    a=paisaWordsDataExtractor()
    print time.asctime()
    s=a.wordsFreq.most_common(100)
    s=[w[0] for w in s if w[0].isalpha()]
    for i in s:
        print "%s  -  %s  "%(i,round(a.wordsFreq.freq(i),3)*100)
    
    print 'done'