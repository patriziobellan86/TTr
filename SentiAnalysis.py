# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 10:56:21 2015

@author: Patrizio
"""

from __future__ import unicode_literals, division

import SaveLoad

import SentenceTokenize
import PosTagger_light
import ParseIt
import StemmerIt
import AnalizzatoreSents

import nltk
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

import random


class SentiAnalysis():
    def __init__(self):
        self.soglia=float(0.8)
        
        self.folder="risorse\\Dati\\"
        self.__SentimTrainsetFilename=self.folder+"SentiTrainSet.list"
        self.classificatoreSentiFilename=self.folder+"Senti.classifier"
        self.classificatoreSenti=None
        self.__Stem=StemmerIt.StemmerIt()
        self.__PosTagger=PosTagger_light.PosTagger()

        if not self.Load():
            print "file del classificatore s.a. mancante\naddestramento in corso..."
            self.__CreaClassificatore()


    def __CreaClassificatore(self):
        dati=SaveLoad.LoadByte(self.__SentimTrainsetFilename)            
        
        self.classificatoreSenti=self.SKClassifierSVM(dati)
        
        self.Save()
         
         
    def __CreaDatasetTrainTest(self, featuresets):
        featuresets=self.Features(featuresets)
        random.shuffle(featuresets)
        
        q=len(featuresets)*self.soglia
        q=int(q)
        
        return featuresets[q:], featuresets[:q]
    
    
    def SKClassifierSVM(self, dati):
        
        try:
            train, test=self.__CreaDatasetTrainTest(dati)
            classifier=SklearnClassifier(LinearSVC()).train(train)
            
            print "ACCURACY SVM:", nltk.classify.accuracy(classifier, test)
      
            return classifier
            
        except Exception, e:
            print 'errore in SVM'
            for i in e:
                print i
            print
            
    
    def Features(self, sents):
        """
            input: list(word)
            output: dict(feaures)
        """
        
        res=list()
        
        for sent in sents:
            words=[self.__PosTagger.PosTag(ele)[0] for ele in sent[0].split()]
          
            s=list()                
            for word in words:
                if word!=tuple():
                    word=self.__Stem.StemWord(word)
                    if word:
                        s.append(word[0])

            feat=dict()    
            for word in s:
                feat[word]=True
            res.append(tuple([feat, sent[1]]))
            
            
        return res
        

    def ParseSent(self, sent):
        """
        
            ParseSent: parser della frase per il calcolo della polarità
            
            input: list(word)
                    
            output: polarità, grado
        
        """
        dictsent={u"Positiva":u" :-) ",u"Neutra":u" :-| ", u"Negativa":u" :-( " }
                           
        senti= self.classificatoreSenti.classify_many(self.Feature(sent))
        
        return dictsent[senti[0]]
        
        
    def Save(self):
        return SaveLoad.SaveByte(self.classificatoreSenti, self.classificatoreSentiFilename)
        
        
    def Load(self):
        self.classificatoreSenti=SaveLoad.LoadByte(self.classificatoreSentiFilename)
        
        if self.classificatoreSenti:
            return True
            
        return False
        

    def Feature(self, sent):
        """
            input: list(word)
            output: dict(feaures)        
        """

        r=list()
        feat=dict()    
        
        for ele in sent.split():
#            print 'ele',ele
            word=self.__PosTagger.PosTag(ele)
            if word!=tuple():
#                print 'word tup', word
                word=self.__Stem.StemWord(word[0])
                if word:
                    r.append(word[0])         
            
            for word in r:
                feat[word]=True

#            print 'feat',feat
            
        return feat
               
            
if __name__=='__main__':
    a=SentiAnalysis()
    sent="ti odio"
    
    print a.ParseSent(sent)

