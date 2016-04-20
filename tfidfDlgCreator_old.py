# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 18:50:40 2015

@author: Patrizio
"""

import numpy as np
from math import sqrt, log
from itertools import chain, product

import collections
import SaveLoad


class tfidfDataCreator():
    def __init__(self, dlgname):
        self.extdlg='.txt'
        self.extdlgData=".dat"
        self.extdlgVoc=".voc"
        self.extdictWordScoreRow='.dictWordsScoreRows'
        
        self.folder="risorse\\Dati\\dialoghi\\"

        corpus, vocab = self.__CreaCorpus(self.folder+"\\dialoghiRaw\\"+dlgname+self.extdlg)
        
        self.data=self.__Tfidf(corpus, vocab)
        self.vocab=vocab       
        
        self.__Save(dlgname)
 

    def __Save(self, dlgname):           
        print "file Saved:", SaveLoad.SaveByte(self.data,self.folder+dlgname+self.extdlgData)
        print "file Saved:", SaveLoad.SaveByte(self.vocab,self.folder+dlgname+self.extdlgVoc)

    def __CreaCorpus(self, dlgfilename):
        all_sents=SaveLoad.LoadLines(dlgfilename)
        corpus, vocab = self.__corpus2vectors(all_sents)
        
        return corpus, vocab


    def __Tfidf(self, corpus, vocab):
        """
            Creo la matrix di data
        """
        
        def termfreq(matrix, doc, term):
            try: 
                return matrix[doc][term] / float(sum(matrix[doc].values()))
            except ZeroDivisionError: 
                
                return 0
        def inversedocfreq(matrix, term):
            try: 
                return float(len(matrix)) /sum([1 for i,_ in enumerate(matrix) if matrix[i][term] > 0])
            except ZeroDivisionError: 
                return 0
    
        matrix = [{k:v for k,v in zip(vocab, i[1])} for i in corpus]
        self.__Tfidf = collections.defaultdict(dict)
        for doc,_ in enumerate(matrix):
            for term in matrix[doc]:
                tf = termfreq(matrix,doc,term)
                idf = inversedocfreq(matrix, term)
                self.__Tfidf[doc][term] = tf*idf
    
        return [[self.__Tfidf[doc][term] for term in vocab] for doc,_ in enumerate(self.__Tfidf)]
    
    
    def __corpus2vectors(self, corpus):
        def vectorize(sent, vocab):
            return [sent.split().count(i) for i in vocab]
            
        vectorized_corpus = []
        vocab = sorted(set(chain(*[i.lower().split() for i in corpus])))
        
        for i in corpus:
            vectorized_corpus.append((i, vectorize(i, vocab)))
            
        return vectorized_corpus, vocab


if __name__=='__main__':
    dlgname="whip it"
    a=tfidfDataCreator(dlgname)
    print type(a.vocab)
    print 
    print 'done'
    