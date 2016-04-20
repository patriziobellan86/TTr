# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:40:11 2015


    CLASSE FINITA IL 06/08/2015

@author: Patrizio
"""
        
from __future__ import unicode_literals
        
import SaveLoad
      
import nltk
import time

class SentsTokenize():
    """
    questa classe modella il sents tokenizer, ne addestra uno e lo utilizza 
    [italiano di default]
    
    """
    def _tipoClasse(self):
        return "sents splitter"
    def _statoLavorazione(self):
        return "completato e testato"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "25\08\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"

    def __init__(self):
        self.__Inizializzavar()
        
        if not self.__Load():
            print 'SentsTokenize not load - creazione in corso...'
            #il file non è stato caricato quindi addestro il tokenize e lo salvo
            self.__Train()
            self.__Save()
            
        self.s=self.__sentsTokenizer   
         
         
    def __Inizializzavar(self):
        self.__abbrvFilename="risorse\\Dati\\abl.abl"
        self.__textforTrainFilename="risorse\\Dati\\sents.txt"
        self.__sentsTokenFileName="risorse\\Dati\\sentsTokenize.pickle"
        self.__folder="risorse\\Dati\\"
        self.__foldertaggedsents =self.__folder+"training\\paisaTagged"

        self.__lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
        self.__corpus=None
        self.__sentsTokenizer= None
        
        
    def __Train(self):
        try:
            abl=SaveLoad.LoadLines(self.__abbrvFilename)
            train=self.__corpus.tagged_sents()[:]
            
            if abl!=False:
            
                punkt_param = nltk.tokenize.punkt.PunktParameters()
                punkt_param.abbrev_types = abl
                        
                self.__sentsTokenizer= nltk.tokenize.punkt.PunktSentenceTokenizer(punkt_param)
                
                self.__sentsTokenizer.train(train)       
            
                return True
            else:
                self.__DefaultSentTokenize()
                
        except:
            #carico il tokenizer di default
            self.__DefaultSentTokenize()
                    
           
    def __DefaultSentTokenize(self):
        print 'file di training mancante...\nimpostato tokenize di default'
        self.__sentsTokenizer = nltk.data.load('tokenizers/punkt/italian.pickle')
       
        return True
       
       
    def __Save(self):
        """
            
            Save
            
            input: None
            hidden: salva il tokenize
            output: True se il processo termina correttamente
            
        """
        
        try:
            SaveLoad.SaveByte(self.__sentsTokenizer,self.__sentsTokenFileName)
            
            return True
        except:
            return False
            
            
    def __Load(self):
        """
            
            Load
            
            input: None
            hidden: carica il tokenize
            output: True se il processo termina correttamente
            
        """
        
        self.__sentsTokenizer=SaveLoad.LoadByte(self.__sentsTokenFileName)
        if not self.__sentsTokenizer:
            self.__corpus=nltk.corpus.ConllCorpusReader(self.__foldertaggedsents,'.*',self.__lst_pos)
            return False
        return True
        
        
        
    def SplitSents(self, sents):
        """
            Split sents in sent
            
            input: str(sents)
            output: list(sent)
            
        """
            
        sents=self.__sentsTokenizer.tokenize(sents)
        
        return sents
            
if __name__=='__main__':
    print time.asctime()
    a=SentsTokenize()
    print time.asctime()
    print 'done'
        
 
    
