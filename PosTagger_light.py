# -*- coding: utf-8 -*-
"""
Created on Fri Aug 07 23:52:26 2015

@author: Patrizio
"""
from __future__ import unicode_literals, division

import PulisciSent
import SaveLoad

import nltk.collocations
import nltk.corpus

import os
import collections
import glob
import nltk
import pickle


class PosTagger():
    def _tipoClasse(self):
        return "PosTag"
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
        
        self.__folder="risorse\\Dati\\"
        self.__folderpaisaPosTagSent=self.__folder+"training\\paisaTagged"

        self.__unigram_taggerFileName=self.__folder+"\\"+"postag_unigramsTagger.postag"
        self.__bigram_taggerFileName=self.__folder+"\\"+"postag_bigramsTagger.postag"
             
        self.__lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
   
        self.__bigrams=None
        self.__tagged=None
        self.__trainingBound=0.9      
        self.__corpus=None        
        self.__backoff_tagger=None
        self.__unigram_tagger=None
        self.__bigram_tagger=None
        
        
        if not self.__Load():
            print u"Files *.postag mancanti...\naddestramento in corso"
            self.__Train()
            self.__Save()


    def __Train(self):
        self.__corpus=nltk.corpus.ConllCorpusReader(self.__folderpaisaPosTagSent,'.*',self.__lst_pos)      
        
        self.__bigrams= nltk.bigrams(self.__corpus.words())
        self.__tagged=self.__corpus.tagged_sents()
    
        lentag=len(self.__corpus.tagged_sents()[:])
        ln=int(self.__trainingBound*lentag)
        
        print u"len : %s    ln: %s"%(lentag,ln)
        train=self.__corpus.tagged_sents()[:ln]
        test = self.__corpus.tagged_sents()[ln:]
        
        self.__backoff_tagger=nltk.DefaultTagger('NOUN')
        self.__unigram_tagger=nltk.UnigramTagger(train, backoff=self.__backoff_tagger)
        self.__bigram_tagger = nltk.BigramTagger(train, backoff=self.__unigram_tagger)
        
        print 'unigram evaluation: ', self.__unigram_tagger.evaluate(test)
        print 'bigram evaluation: ', self.__bigram_tagger.evaluate(test)
        
        
    def __Save(self):
        SaveLoad.SaveByte(self.__unigram_tagger, self.__unigram_taggerFileName)
        SaveLoad.SaveByte(self.__bigram_tagger, self.__bigram_taggerFileName) 
         
        return True
          
            
    def __Load(self):
        self.__unigram_tagger=SaveLoad.LoadByte(self.__unigram_taggerFileName)
        self.__bigram_tagger=SaveLoad.LoadByte(self.__bigram_taggerFileName)
        
        if self.__bigram_tagger!=False and self.__unigram_tagger!=False:
            return True
        return False

  
    def PosTag(self, sent):
        """
            
            Pos Tagger
            
            input: la str(sent)
            output: list(tuple(word, tag))
        
        """
        assert(type(sent)!=type(str))
        
        sent=PulisciSent.PulisciSent().Pulisci(sent)
        taggedSent=[]        
        sent=nltk.word_tokenize(sent)
        taggedSent=self.__bigram_tagger.tag(sent)
           
        return taggedSent
   
                
if __name__=='__main__':
    import time
    
    print time.asctime()
    a=PosTagger()
    print time.asctime()
    
    sent='questa è una prova'
    print 'sent di prova: ', sent
    print a.PosTag(sent)
    print time.asctime()
    
    sent='questa è un\'altra prova di prova'
    print 'sent di prova: ', sent
    print a.PosTag(sent)
    print time.asctime()
#    
    
    print 'done'