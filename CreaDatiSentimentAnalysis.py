# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 23:40:37 2015

@author: Patrizio
"""
from __future__ import unicode_literals, division


import ParseCreaDatiSentimentAnalysis
import SaveLoad

import glob

class CreaDatiSentimentAnalysis():
    def __init__(self):
    
        self.__folder="risorse\\Dati\\"
        self.__folderdialoghi=self.__folder+"\\dialoghi\\dialoghiRaw\\"
        self.SentiAnaliz=ParseCreaDatiSentimentAnalysis.ParseCreaDatiSentimentAnalysis()
        self.__SentimTrainsetFilename=self.__folder+"SentiTrainSet.list"
        
        
        dati=self.AvviaCreazioneDati()
        
        print SaveLoad.SaveByte(dati,self.__SentimTrainsetFilename)
        
        
    def AvviaCreazioneDati(self):
        sentWithSentimento=list()
        
        i=0
        files=glob.glob(self.__folderdialoghi+'*')
        for file in files:
            
            print file
            
            dlg=SaveLoad.LoadLines(file)
            for line in dlg:
                line=self.SentiAnaliz.StimaSentimentoFrase(line)
                if line!=list():
                    for l in line:
                        if l!=list():
                            sentWithSentimento.append(l)
            
#            print 'file', i
            i+=1
            
            if i>50:
                return sentWithSentimento
                
                
        return sentWithSentimento

if __name__=='__main__':
    
    a=CreaDatiSentimentAnalysis()

    print 'done'
           