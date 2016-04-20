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

import paisaWordsDataExtractor



__folder="risorse\\Dati\\"
__stopWordsFilename=__folder+"StopWords.list"
__stopWords=list()


__pulisci=PulisciSent.PulisciSent()

__sentTokenize=SentenceTokenize.SentsTokenize()        
__PosTagger=PosTagger_light.PosTagger()
__Parse=ParseIt.ParseIt()        
__Stem=StemmerIt.StemmerIt()
    

    
tagtoexclude=[u"PUNC",u"SYM",u"NUM",u"ART",u"PRE"]
WordsInvertiSent=[u"no",u"non"]


#carico le liste di dati
pos=SaveLoad.LoadLines(__folder+"SentiPos.txt")
neg=SaveLoad.LoadLines(__folder+"SentiNeg.txt")
        
dictsentiScore={word.strip():float(1) for word in pos}
dictsentiScore.update({word.strip():float(-1) for word in neg})

sentiPos=[word.strip() for word in pos]
sentiNeg=[word.strip() for word in neg]
    
def Analisi(sents):
    """
        
        Analisi frase
    
        input: string
        output: 
    sentiScore
    """
    def PreAnalisi(sent):
        for word in sent:
            if (word in sentiPos) or (word in sentiNeg):
                return True
    
    #per prima cosa pulisco la sent a livello di char
    sents=__pulisci.Pulisci(sents)
    #tokenizzo in sent
    sents=__sentTokenize.SplitSents(sents)
       
    frasi=[]
    trees=[]
    
    for sent in sents:
        if len(__pulisci.Pulisci(sent))>0:
            
            if not PreAnalisi(sent.split()):
                return False, False
                
            pt=__PosTagger.PosTag(sent)
    
            tagsent=__DelStopWords(pt)
            tagsent=__ExcludeTag(tagsent)
            print "TAGSENT", tagsent
            tree=__Parse.ParseSent(tagsent)
            if tree:
#                tree.draw()
                trees.append(tree)
            sent=__Stem.StemSent(tagsent)
            frasi.append([word[0] for word in tagsent])
                            
    return frasi, trees
    


def __ExcludeTag(sent):
    return [wt for wt in sent if wt[1] not in tagtoexclude]
    
    
def __DelStopWords(sent):
    """
        DelStopWords: elimina le stop words dalla frase
        
        input:list(tuple(word,tag))
        output:list(tuple(word,tag))
        
    """
    
    ssent=list()
    
    for wt in sent:
        if wt[0] not in __stopWords:
            ssent.append(wt)
            
    return ssent


def __Load():
    __stopWords=SaveLoad.LoadByte(__stopWordsFilename)
    if not __stopWords:
        print "file stopwords mancante...\nestrazione in corso"
        paisaWordsDataExtractor.paisaWordsDataExtractor()
 
        if not __Load():
            print "processo di estrazione corrotto\nimpossibile procedere..."
            return False
    return True



  
def traverse(t, lista,d=0):
    try:
        if len (t.leaves())==1:
            d+=1            
#            print t.leaves(),d
            lista.append(tuple([t.leaves(),d]))
    except AttributeError:
        pass
    else:                 
#        if len (t.leaves())==1:
#            d+=1            
#            print t.leaves(),d
#            b.append(tuple([t.leaves(),d]))
        for child in t:
            d+=1
            traverse(child,lista,d)
            

def SentiParse(lista):
    polarita=0    
    inverti=False
    score=0
    
    for d, ele in enumerate(lista):
        print ele[1][0]
        if ele[1][0] in dictsentiScore.keys():
            #ho una parola di sentimento
            score=dictsentiScore[ele[1][0]]

        if ele[1][0] in WordsInvertiSent:
            if inverti:
                inverti=False
            else:
                inverti=True
        
        if inverti:
                score=score*-1
        polarita+=score
        score=0
        
    print polarita
    if polarita>0:
        return u"Positiva"
    elif polarita<0:
        return u"Negativa"
    
    return u"Neutra"
    
sentence="amore non ci sei mai a casa avarizia"

sents, trees=Analisi(sentence)
trees=trees[0]
print 
print 

lista=list()
traverse(trees,lista)
lista=lista[:-1]

print 'lista', lista
l=[([v,w]) for (w,v) in lista]
l.sort()

print SentiParse(l)



print 'done'
           