# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:32:52 2015

@author: Patrizio
"""

from __future__ import unicode_literals,division

import SaveLoad
import PulisciSent
import SentenceTokenize
import PosTagger_light
import ParseIt
import StemmerIt

import paisaWordsDataExtractor


class AnalizzatoreSents():
    def __init__(self):
        self.__folder="risorse\\Dati\\"
        self.__stopWordsFilename=self.__folder+"StopWords.list"
        self.__stopWords=list()
        self.__Load()
        
        self.__pulisci=PulisciSent.PulisciSent()
        
        self.__sentTokenize=SentenceTokenize.SentsTokenize()        
        self.__PosTagger=PosTagger_light.PosTagger()
        self.__Parse=ParseIt.ParseIt()        
        self.__Stem=StemmerIt.StemmerIt()
        
        self.tagtoexclude=[u"PUNC",u"SYM",u"NUM",u"ART",u"PRE"]
        
    def Analisi(self, sents):
        """
            
            Analisi frase
        
            input: string
            output: list(word)
        
        """
        #per prima cosa pulisco la sent a livello di char
        sents=self.__pulisci.Pulisci(sents)
        #tokenizzo in sent
        sents=self.__sentTokenize.SplitSents(sents)
       
        frasi=[]
#        trees=[]
        
        for sent in sents:
            if len(self.__pulisci.Pulisci(sent))>0:
                pt=self.__PosTagger.PosTag(sent)

                tagsent=self.__DelStopWords(pt)
                tagsent=self.__ExcludeTag(tagsent)
#                print "TAGSENT", tagsent
#                tree=self.__Parse.ParseSent(tagsent)
#                if tree:
#                    tree.draw()
#                    trees.append(tree)
                sent=self.__Stem.StemSent(tagsent)
                frasi.append([word[0] for word in tagsent])
                                
        return frasi


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
        self.__stopWords=SaveLoad.LoadByte(self.__stopWordsFilename)
        if not self.__stopWords:
            print "file stopwords mancante...\nestrazione in corso"
            paisaWordsDataExtractor.paisaWordsDataExtractor()
 
            if not self.__Load():
                print "processo di estrazione corrotto\nimpossibile procedere..."
                return False
        return True
        
        
if __name__=='__main__':
    import time
    
    print time.asctime()
    a=AnalizzatoreSents()
    print time.asctime()
    s=u"ti il piace giocare al pc"
    print 
    print a.Analisi(s)
    print time.asctime()
    print 'done'