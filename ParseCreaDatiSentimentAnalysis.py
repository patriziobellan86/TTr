# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 23:40:37 2015

@author: Patrizio
"""
from __future__ import unicode_literals, division


import copy

import SaveLoad
import PulisciSent
import SentenceTokenize
import PosTagger_light
import ParseIt
import StemmerIt
import AnalizzatoreSents

import paisaWordsDataExtractor

class ParseCreaDatiSentimentAnalysis():
    def __init__(self):
    
        self.__folder="risorse\\Dati\\"
        self.__stopWordsFilename=self.__folder+"StopWords.list"
        self.__stopWords=list()
        
        
        self.__pulisci=PulisciSent.PulisciSent()
        
        self.__sentTokenize=SentenceTokenize.SentsTokenize()        
        self.__PosTagger=PosTagger_light.PosTagger()
        self.__Parse=ParseIt.ParseIt()        
        self.__Stem=StemmerIt.StemmerIt()
        self.__AnalizzatoreSent=AnalizzatoreSents.AnalizzatoreSents()            
        
            
        self.tagtoexclude=[u"PUNC",u"SYM",u"NUM",u"ART"]
        
        self.WordsInvertiSent=[u"no",u"non"]
        
        self.__Load()
        
        
  
    def Analisi(self, sents):
        """
            
            Analisi frase
        
            input: string
            output: 
        sentiScore
        """
        def PreAnalisi(sent):
            for word in sent:
                word=self.__PosTagger.PosTag(word)
                if word!=list():
                    word=self.__Stem.StemWord(word[0])
                    if word:
                        if (word[0] in self.sentiPos) or (word[0] in self.sentiNeg):
                            return True
        
        #per prima cosa pulisco la sent a livello di char
        sents=self.__pulisci.Pulisci(sents)
        #tokenizzo in sent
        sents=self.__sentTokenize.SplitSents(sents)
           
        frasi=[]
        trees=[]
        
        for sent in sents:
            if len(self.__pulisci.Pulisci(sent))>0:
                
                if not PreAnalisi(sent.split()):
                    return False, False
                    
                pt=self.__PosTagger.PosTag(sent)
        
                tagsent=self.__DelStopWords(pt)
                tagsent=self.__ExcludeTag(tagsent)
                tree=self.__Parse.ParseSent(tagsent)
                if tree:
#                    tree.draw()
                    trees.append(tree)
                sent=self.__Stem.StemSent(tagsent)
                frasi.append([word[0] for word in tagsent])
                                
        return frasi, trees
        

    
    def __ExcludeTag(self, sent):
        return [wt for wt in sent if wt[1] not in self.tagtoexclude]
        
        
    def __DelStopWords(self, sent):
        """
            DelStopWords: elimina le stop words dalla frase
            
            input:list(tuple(word,tag))
            output:list(tuple(word,tag))
            
        """
        
        ssent=list()
        
        for wt in sent:
            if wt[0] not in self.__stopWords:
                ssent.append(wt)
                
        return ssent

    
    def __Load(self):
        #carico le liste di dati
        pos=SaveLoad.LoadLines(self.__folder+"SentiPos.txt")
        neg=SaveLoad.LoadLines(self.__folder+"SentiNeg.txt")
                
        self.dictsentiScore={}
        
        self.sentiPos=list()
        for word in pos:
            word=word.strip()
            word=self.__PosTagger.PosTag(word)
            if word!=list():            
                word=self.__Stem.StemWord(word[0])
                self.dictsentiScore[word[0]]=float(1)
                self.sentiPos.append(word[0])
            
                
        self.sentiNeg=list()
        for word in neg:
            word=word.strip()
            word=self.__PosTagger.PosTag(word)
            if word!=list():
                word=self.__Stem.StemWord(word[0])
                self.dictsentiScore[word[0]]=float(-1)
                self.sentiNeg.append(word[0])
        
        self.__stopWords=SaveLoad.LoadByte(self.__stopWordsFilename)
        if not self.__stopWords:
            print "file stopwords mancante...\nestrazione in corso"
            paisaWordsDataExtractor.paisaWordsDataExtractor()
     
            if not self.__Load():
                print "processo di estrazione corrotto\nimpossibile procedere..."
                return False
        return True
    

    
      
    def traverse(self, t, lista,d=0):
        try:
            if len (t.leaves())==1:
                d+=1            
                lista.append(tuple([t.leaves(),d]))
        except AttributeError:
            pass
        else:                 
            for child in t:
                d+=1
                self.traverse(child,lista,d)
                
    
    def SentiParse(self, lista):
        polarita=0    
        inverti=False
        score=0
        
        for d, ele in enumerate(lista):
            if ele in self.dictsentiScore.keys():
                #ho una parola di sentimento
                if d>float(0):
                    score=self.dictsentiScore[ele]*float(1/d)
                else:
                    score=self.dictsentiScore[ele]

                    
            if ele in self.WordsInvertiSent:
                if inverti:
                    inverti=False
                else:
                    inverti=True
            
            if inverti:
                    score=score*-1
            polarita+=score
            score=0
            
        if polarita>0:
            return u"Positiva"
        elif polarita<0:
            return u"Negativa"
        
        return u"Neutra"

    def StimaSentimentoFrase(self, sent):        
        sents, trees=self.Analisi(sent)
        
        sentiments=list()
        
        if trees:
            for tree in trees:
                trees=trees[0]
                lista=list()
                self.traverse(trees,lista)
                lista=lista[:-1]
                
                l=[([v,w]) for (w,v) in lista]
                l.sort()

                words=[self.__PosTagger.PosTag(word[1][0]) for word in l ]
                
                l=list()
                for word in words:
                    if word!=tuple():
                        word=self.__Stem.StemWord(word[0])
			if word!=False:
	                    l.append(word[0])
                if l!=list():
	            sentimento=self.SentiParse(l)
                    print sentimento
                    sentiments.append(tuple([sent, sentimento]))
            	else:
                    sentiments.append(tuple([sent, u"Neutra"]))

        return sentiments#,sent

if __name__=='__main__':
    a=ParseCreaDatiSentimentAnalysis()
    sent="ti odio"
    c= a.StimaSentimentoFrase(sent)
    print c
    
    
    
    print 'done'
           