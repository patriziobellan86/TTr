# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 01:56:10 2015

@author: Patrizio
"""

print "Stimantore Sentiment Analysis"



class ClassificatoreSentimentAnalysis():
    def __init__(self):
        self.__folder="risorse\\Dati\\"
        self.__folderdialoghi=self.__folder+"\\dialoghi\\dialoghiRaw\\"
        self.SentiAnaliz=ParseCreaDatiSentimentAnalysis.ParseCreaDatiSentimentAnalysis()

        dati=self.AvviaCreazioneDati()
        print SaveLoad.SaveByte(dati