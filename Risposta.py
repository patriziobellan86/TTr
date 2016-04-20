# -*- coding: utf-8 -*-
"""
Created on Thu Sep 03 16:54:52 2015

@author: Patrizio
"""

from __future__ import unicode_literals

import DialogoQuestEngine
import GeneratoreLinguistico
import SentiAnalysis

class Risposta():
    def __init__(self, dlgname="coscienza"):
#        print dlgname, type(dlgname)
        self.dlgQuest=DialogoQuestEngine.QuestEngine(dlgname)
        self.generatore=GeneratoreLinguistico.HMMLanguageGenerator(dlgname)
        self.sentiAnal=SentiAnalysis.SentiAnalysis()
        
    
    def Risposta(self, string):
        
        
        
        risp=self.dlgQuest.Query(string)
        risp=risp.strip()
        
        if risp==u"":
        #la risp è vuota quindi
        #genero una frase a caso con hmm
            
            #tmp        
            string=string.split()
            string=string[0]
            risp=self.generatore.GeneraSent(string)
        
        try:
            sentimento=self.sentiAnal.ParseSent(risp)
        except:
            sentimento=u" :-| "
            
        risp=sentimento+u"  "+risp             
        return risp

if __name__=='__main__':
    a=Risposta()

    print 'done'