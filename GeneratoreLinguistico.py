# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 00:51:43 2015

@author: Patrizio
"""

from __future__ import unicode_literals


import SaveLoad

import nltk
import time
import random


class HMMLanguageGenerator():
    def __init__(self, dlgname=""):
        self.folder="risorse\\Dati\\"
        self.folderDialoghi="risorse\\Dati\\dialoghi\\"
        
        self.extHMMforward='.HMMforward'
        self.extHMMbackward='.HMMbackward'
        self.extdlg='.txt'
        
        if dlgname!="":
            self.CambiaDialogo(dlgname)


    def CambiaDialogo(self, dlgname):
        if not self.__Load(dlgname):
            self.__CreaModel(dlgname)
            self.__Load(dlgname)
    
    
    def __Load(self, dlgname):
        self.__dialogo=SaveLoad.LoadLines(self.folderDialoghi+"dialoghiRaw\\"+dlgname+self.extdlg)
        
        self.__modelforward=SaveLoad.LoadByte(self.folderDialoghi+dlgname+self.extHMMforward)
        self.__modelbackward=SaveLoad.LoadByte(self.folderDialoghi+dlgname+self.extHMMbackward)

        if self.__modelforward!=False and self.__modelbackward!=False:
            return True

        return False

        
    def __CreaModel(self, dlgname):
        #genero i modelli  
        self.__modelforward=self.__GeneraModel(self.__dialogo)
        self.__modelbackward=self.__GeneraModel(self.__dialogo, reverse=True)


        self.__Save(dlgname)
        
    
    def __Save(self, dlgname):
        print "file Saved:", SaveLoad.SaveByte(self.__modelbackward, self.folderDialoghi+dlgname+self.extHMMbackward)
        print "file Saved:", SaveLoad.SaveByte(self.__modelforward, self.folderDialoghi+dlgname+self.extHMMforward)

        
    def GeneraSent(self, string):
        """
            GeneraSent: genera una frase usando una stringa di partenza per i vocaboli
            
            input: string 
            output: string
            
        """
        
#        if not string.isalnum():
#            string = 'ciao'
        k=self.__modelforward.keys()
        index=random.randint(0,len(k))        
        string=k[index]

        forw= self.__GeneraRawSent(self.__modelforward, word=string, num=random.randint(1,7))        
        backw= self.__GeneraRawSent(self.__modelbackward, word=string, num=random.randint(0,5), reverse=True)        
        sent=list()
        sent.extend(backw)
        if sent!=list():
            sent.extend(forw[1:])
        else:
            sent.extend(forw)
        
        sent=u" ".join(sent)
        sent=sent.strip()

        
        return sent
        
        
    def __GeneraModel(self, dati, reverse=False):
        """
            Crea il modello della distribuzione di frequenza
            
        """
        print 'generazione del modello in corso...'
        model=list()

        if dati:
            for sent in dati:  
                sent=nltk.word_tokenize(sent)

                if reverse:
                    sent.reverse()                    
            
                sent=self.__CreaPairs(sent)
                model.extend(sent)

        model=nltk.ConditionalFreqDist(model)
        
        return model

        
    def __CreaPairs(self, dati):
        """
        genera i pairs
        
        """

        pairs=list()
        
        for i in xrange(len(dati)):
            if i<len(dati)-1:
                pairs.append(tuple([dati[i], dati[i+1]]))
        
        return pairs
        
        
    def __GeneraRawSent(self, cfd, word='word', num=10, reverse=False):     
        sent=list()
        
        sent.append(word)
        
        for i in xrange(num):         
            arr=list()          # an array with the words shown by count     
            for j in cfd[word]:             
                for k in range(cfd[word][j]):                 
                    arr.append(j)                  
                    word = arr[int((len(arr))*random.random())]   
                    if word!=sent[-1]:
                        sent.append(word)
                    
                    if len(sent)>=num:
                        break                        
                if len(sent)>=num:
                    break                        
            if len(sent)>=num:
                break                        

        if reverse:
            sent.reverse()
        
        return sent           
 

if __name__=='__main__':
    a=HMMLanguageGenerator("whip it")
    print a.GeneraSent('é')
    print 'done'
    