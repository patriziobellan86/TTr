# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 18:50:40 2015

@author: Patrizio
"""

from sklearn.feature_extraction.text import TfidfVectorizer

import SaveLoad


class tfidfDataCreator():
    def __init__(self, dlgname):
        self.extdlg='.txt'
        self.extdlgData=".dat"
        self.extdlgVoc=".voc"
        self.extdictWordScoreRow='.dictWordsScoreRows'
        
        self.folder="risorse\\Dati\\dialoghi\\"

        dlg=SaveLoad.LoadLines(self.folder+"dialoghiRaw\\"+dlgname+self.extdlg)

        if dlg:
            self.__Tfidf(dlg)
            self.__Save(dlgname)
        else:
            print "file di dialogo mancante\nimpossibile procedere..."

    def __Save(self, dlgname):           
        print "file Saved:", SaveLoad.SaveByte(self.data,self.folder+dlgname+self.extdlgData)
        print "file Saved:", SaveLoad.SaveByte(self.vocab,self.folder+dlgname+self.extdlgVoc)


    def __Tfidf(self, dlg):
        """
            Creo la matrix di data
        """
                
        tfidf = TfidfVectorizer()
        self.data = tfidf.fit_transform(dlg)
        self.vocab=tfidf.get_feature_names()
        

if __name__=='__main__':
    
    dlgname="tutti i dialoghi"
    a=tfidfDataCreator(dlgname)
   
    print 'done'
    