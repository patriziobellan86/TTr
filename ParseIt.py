# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 23:53:51 2015

@author: Patrizio
"""

import SaveLoad

import nltk
import time


class ParseIt():
    """
            classe chart parser
            
            il parser è creato ad ogni occorrenza così ho meno regole da memorizzare
                
    """
    def _tipoClasse(self):
        return "Chart Parser"
    def _statoLavorazione(self):
        return "in testing"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "29\08\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"
    def __init__(self):       
        self.folder="risorse\\Dati\\"
        self.__grammarsFilename=self.folder+"grammars.list"
        
        self.__InitializeVar()
        
        self.__Load()        

        
    def __InitializeVar(self):
        self.__parser=None
        self.__grammars=None

        self.NoTdict={
            u"START":nltk.grammar.Nonterminal(u"S0"),
            u"S":nltk.grammar.Nonterminal(u"S"),
            u"NP":nltk.grammar.Nonterminal(u"NP"),
            u"VP":nltk.grammar.Nonterminal(u"VP"),
            
            u"VER":nltk.grammar.Nonterminal(u"VER"),
            u"NOUN":nltk.grammar.Nonterminal(u"NOUN"),
            u"ADJ":nltk.grammar.Nonterminal(u"ADJ"),
            u"ADV":nltk.grammar.Nonterminal(u"ADV"),
            u"ART":nltk.grammar.Nonterminal(u"ART"),
            u"PRE":nltk.grammar.Nonterminal(u"PRE"),
            u"DET":nltk.grammar.Nonterminal(u"NP"),
            u"PRO":nltk.grammar.Nonterminal(u"PRO"),
            u"WH":nltk.grammar.Nonterminal(u"WH"),
            u"INT":nltk.grammar.Nonterminal(u"INT"),
            u"NUM":nltk.grammar.Nonterminal(u"NUM"),
            u"PUNC":nltk.grammar.Nonterminal(u"PUNC"),
            u"CON":nltk.grammar.Nonterminal(u"CON")
         }  

         
    def addRules(self, rules):
        """

            input: le regole da aggiungere        
            hidden: aggiunge le regole alla grammatica interna
            output: True se il processo termina correttamente
        
        """
        
        for rule in rules:
            self.__grammars.append(rule)    
        
        return True
    def addRule(self, rule):
        self.__grammars.append(rule)
        return True
        
        
    def addTerminalRules(self, terminals):
        """
            add Terminal Rules
            
            input: list(tuple(word,tag))
            hidden: aggiunge la regola alla grammatica  interna
            output: True se il processo termina correttamente
            
        """
        for terminal in terminals:
            self.addTerminalRule(terminal)
        return True
    def addTerminalRule(self, terminal):
        t_0,t_1=terminal
        rule=nltk.grammar.Production(self.NoTdict[t_1],[t_0])
        self.addRule(rule)
        
        return True


    def ParseSent(self, sent):
        """
            Parse Sent
            
            input: list(tuple(word,tag))       
            output: l'albero della frase parserizzata
            
        """
        
        for token in sent:
            #token è la tupppla(word, tag)
            #aggiungo ogni token come regola terminale alla grammatica interna
            self.addTerminalRule(token)
        
        #ora che ho impostato tutte le regole posso creare il chartparser
        self.__CreaParser()
        
        #ora che ho impostato il parser parserizzo la sent e restituisco l'albero ottenuto
        #la sent deve essere composta di sole word, quindi la trasformo
        sent=[i[0] for i in sent]
        chart=self.__parser.chart_parse(sent)
        parses=list(chart.parses(self.__CFGrammar.start()))
        for tree in parses:
            #usato per operazioni varie
            #tree.draw()
            #per ora pass            
            pass
        try:
            return tree
            
        except UnboundLocalError:
            return False        
                
        
    def __CreaParser(self):  
        #come parser utilizzo BottomUpLeftCornerChartParser
    
        #creo laCFG
        self.__CFGrammar=nltk.CFG(self.NoTdict[u"START"],self.__grammars)
        #creo il parser
        self.__parser=nltk.parse.BottomUpLeftCornerChartParser(self.__CFGrammar)
        
        return True
                
        
    def __Load(self):
        """
            
            Load
            
            input: None
            hidden: carica i dati 
            output:  True se il processo termina correttamente
        
        """
        
        self.__grammars=SaveLoad.LoadByte(self.__grammarsFilename)
        if not self.__grammars:
            import GrammarExtractor
            GrammarExtractor.GrammarExtractor()
            self.__grammars=SaveLoad.LoadByte(self.__grammarsFilename)
        return True
    
        
            
if __name__=='__main__':
    print time.asctime()    
    g=ParseIt()
    print time.asctime()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    