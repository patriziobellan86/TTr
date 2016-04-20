# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 18:47:10 2015

@author: Patrizio
"""

import SaveLoad
import tfidfDlgCreator

import collections


class CreaDatiQuestEngine():
    def __init__(self, dlgname):
        self.extdlg=".txt"
        self.extdlgData=".dat"
        self.extdlgVoc=".voc"
        self.extdictWordIndex='.dictWordIndex'
        self.extdictWordScoreRow='.dictWordsScoreRows'
        
        self.folder="risorse\\Dati\\dialoghi\\"

        dlg=SaveLoad.LoadLines(self.folder+"\\dialoghiRaw\\"+dlgname+self.extdlg)
        #dlgfilename="C:\\Esame TTR\\risorse\\Dati\\dialoghi\\dialoghiRaw\\Black Mirror  dvdrip.txt"
       
        dlgdata=SaveLoad.LoadByte(self.folder+dlgname+self.extdlgData)
        vocab=SaveLoad.LoadByte(self.folder+dlgname+self.extdlgVoc)
        
        try:
            dlgdata.mean()
        except:    
            print "file .dat mancante\ncreazione in corso..."
            #creo il file con tdidft cosine ecc...
            tfidfDlgCreator.tfidfDataCreator(dlgname)
               
            #ricarico i dati
            dlgdata=SaveLoad.LoadByte(self.folder+dlgname+self.extdlgData)
            vocab=SaveLoad.LoadByte(self.folder+dlgname+self.extdlgVoc)

        dictIndexWord=dict()
        for i in xrange(len(vocab)):
            dictIndexWord[i]=vocab[i]

        #dictPosWordsReverse
        self.dictWordIndex=dict()
        #[word]=index in dictIndexWord
        for k,v in dictIndexWord.iteritems():
            self.dictWordIndex[v]=k
        
        self.dictWordScoreRow=collections.defaultdict(list)
        #[word][score in row][Row] -> per max
        
#        print dlgdata.shape[0]
#        print dlgdata.shape[1]
       
        for row in xrange(dlgdata.shape[0]):
            for col in xrange(dlgdata.shape[1]):
                indice=tuple([row, col])
                prob=dlgdata[indice]
                if prob!=float(0):
#                    print row, col, prob
        
                    scoreRow=dict()
                    
                    word=dictIndexWord[col]                    
                    count=dlg[row].split()
                    count=count.count(word)                    
                    count=count*prob#dlgdata[row][col]
                                        
                    scoreRow[count]=row
                    self.dictWordScoreRow[word].append(scoreRow)
                    
        
        del dlgdata

        print "file Saved:", SaveLoad.SaveByte(self.dictWordScoreRow,self.folder+dlgname+self.extdictWordScoreRow)
        print "file Saved:", SaveLoad.SaveByte(self.dictWordIndex, self.folder+dlgname+self.extdictWordIndex)


if __name__=='__main__':
    dlg="bones"
    a=CreaDatiQuestEngine(dlg)