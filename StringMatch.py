# -*- coding: utf-8 -*-
"""
Created on Sat Aug 08 13:59:46 2015

@author: Patrizio
"""

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class StringFuzzyMatch():
    def __init__(self):
        #il cutoff è nel range (0,100)
        self.scoreCutoff=75
        
    def Ratio(self, s1,s2):
        return fuzz.ratio(s1,s2)
    
    def PartialRadio(self, s1,s2):
        return fuzz.partial_ratio(s1,s2)
        
    def TokenSortRatio(self, s1,s2):  
        return fuzz.token_sort_ratio(s1,s2,force_ascii=False)
    
    def TokenSetRatio(self, s1,s2):
        return fuzz.token_set_ratio(s1,s2)
   
    def ProcessExtract(self,word, choices):
        return process.extract(word, choices)
        
    def ProcessExtractLimitBest3(self,word, choices):
        return process.extract(word, choices, limit=3)
        
    def ProcessExtractOne(self, word, choices):
        return process.extractOne(word, choices)

    def ProcessExtractOneCutoff(self, word, choices):
        return process.extractOne(word, choices,score_cutoff=self.scoreCutoff)
        
    def ProveAll(self, s1,s2):
            
        print s1, '\n', s2, '\n'
        
        
        print 'Simple Ratio'
        print self.Ratio(s1,s2)
            
        print 'Partial Ratio'
        print self.PartialRadio(s1,s2)
            
        print 'Token Sort Ratio'
        print self.TokenSortRatio(s1, s2)
            
        print 'Token Set Ratio'
        print self.TokenSetRatio(s1,s2)
        
        print 'process extract'
        choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
        word="new york jets"
        print word
        print self.ProcessExtract(word, choices)
        
        word="xew uork jjets"
        print word
        print self.ProcessExtractOne(word, choices)
        
        word="xew uork jjets cutoff"
        print word
        print self.ProcessExtractOneCutoff(word, choices)
        
        print '\n'*3
              
if __name__=='__main__':
        
    s1=u'questa è una prova'
    s2=u'è una prova'
    
    print'prove'
    a=StringFuzzyMatch()
    
    a.ProveAll(s1,s2)
    s1=u'questa èè[]{}@#|\\^?ì una prova di difflib'
    s2=u'queste sono prove di difflib'
    a.ProveAll(s1,s2)
    
    s22=[[s2],[s1]]
    print a.Ratio(s1,s22)
    
