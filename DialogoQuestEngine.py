# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 20:20:13 2015

@author: Patrizio
"""

import SaveLoad
import CreaDatiQuestEngine

import random


class QuestEngine():
    def __init__(self, dlgname):
        self.extdlg=".txt"
        self.extdictWordIndex='.dictWordIndex'
        self.extdictWordScoreRow='.dictWordsScoreRows'
        
        self.folder="risorse\\Dati\\dialoghi\\"
        
        self.__CaricaDlg(dlgname)        
        
        
    def __CaricaDlg(self, dlgname):
        self.dlg=SaveLoad.LoadLines(self.folder+"\\dialoghiRaw\\"+dlgname+self.extdlg)
        self.dictWordScoreRow=SaveLoad.LoadByte(self.folder+dlgname+self.extdictWordScoreRow)
        self.dictWordIndex=SaveLoad.LoadByte(self.folder+dlgname+self.extdictWordIndex)

        if not (self.dictWordScoreRow and self.dictWordIndex):
            print "file dict mancanti\ncreazione in corso..."
            CreaDatiQuestEngine.CreaDatiQuestEngine(dlgname)
            #ricarico i dati            
            self.dictWordScoreRoww=SaveLoad.LoadByte(self.folder+dlgname+self.extdictWordScoreRow)
            self.dictWordIndex=SaveLoad.LoadByte(self.folder+dlgname+self.extdictWordIndex)              
                      
    def __OneQuery(self, word):
        """
        input: word
        output:
            numero riga
            insieme di righe
            score max
            
            
        """
        
        try:
            if not word.isalnum():
                return int(0), set(), float(0)
                
            if word not in self.dictWordIndex.keys():
    #            print 'word non in vocab'
                return int(0), set(), float(0)
                
            rows=self.dictWordScoreRow[word]
            maxRow=max(rows)
            
            score=maxRow.keys()[0]
            maxRow=maxRow.values()[0]
            
            rows=[i.values()[0] for i in self.dictWordScoreRow[word]]# for r in self.dictWordScoreRow[word][i].itervalues()]
    
            return int(maxRow), set(rows), score
        except:
            return int(0), set(), float(0)
            
    
    def __MoreWordsQuery(self, words):
        res=list()
        
        for query in words:
            row, rows ,score=self.__OneQuery(query)
                   
            if rows!=set():
                res.append(rows)
        return res
    
    
    def Query(self, string):
        """
            Query: effettua una ricerca nello script e restituisce la frase
            successiva a quella più probabile
            
            input: string
            output:string
        
        """
        
        def TrovaInsiemeRisultati(resSet):
            """
            input: list(set(rows))
            """    
            #ponderando a priori l'ordine di query delle parole mi troverò la parola di 
            #valutazione di importanza maggiore come prima e quindi non devo effettuare 
            #ulteriori confronti tra insiemi
            prec=resSet[0]
            res=prec.copy()
            for s in resSet:
                #per ogni insieme
                res.intersection_update(s)
                if res==set():
                    return prec
                else:
                    prec=res.copy()            
            
            return res
    
        def RemoveRow(resSet, value):
            resSet=list(resSet)
            resSet.remove(value)
            resSet=set(resSet)
    
            return resSet
        
        def BestRes(res):        
            bestres=TrovaInsiemeRisultati(res)
            bestres=list(bestres)
            if len(bestres)>1:
                bestres=bestres[random.randint(0,len(bestres)-1)]
            else:
                bestres=bestres[0]
                
            return bestres
        
        res=self.__MoreWordsQuery(string.split())
        
        if res==list():
            return u""
            
        b=BestRes(res)
        
        if b+1>=len(self.dlg):
            res=RemoveRow(res,b)        
            b=BestRes(res)
        
        sent= self.dlg[b+1]

        return sent


def test():    
    print 'test'
    import time
    
    dlgname='the great martian war 1913 1917'    
    print dlgname
    print time.asctime()    
    a=QuestEngine(dlgname)
    print time.asctime()
    
    print a.Query('ciao')
    print a.Query('come  ti chiami ?')
    
if __name__=='__main__':
    test()

    print 'done'
    
    