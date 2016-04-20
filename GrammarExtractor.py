# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 23:53:51 2015

@author: Patrizio
"""

from __future__ import unicode_literals, division


import SaveLoad

import os
import copy
import time

import nltk


class GrammarExtractor():
    def _tipoClasse(self):
        return "estrattore di dati"
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
        self.__folder="risorse\\Dati\\"
        self.__foldertaggedsents =self.__folder+"training\\paisaTagged"
        
        self.__InizializzaVar()
        self.__EstraiDati()
    
        self.__Save()
    
#        self.__testing()
        

    def __testing(self):    
        print "in testing\nfile della grammatica non salvato"
        try:        
            os.remove(self.__grammarsFilename)
        except:
            pass
        
        
    def __InizializzaVar(self):
#        self.__nprulesFilename=self.folder+"nprules.list"
#        self.__vprulesFilename=self.folder+"vprules.list"
        self.__grammarsFilename=self.__folder+"grammars.list"
        self.__grammars=list()
        self.__nprules=list()
        self.__vprules=list()
        
        self.__lst_pos=['ignore','words','ne','ignore','pos','srl','chunk','tree','ignore','ignore']
        self.__corpus=nltk.corpus.ConllCorpusReader(self.__foldertaggedsents,'.*',self.__lst_pos)
                
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
         
        
    def __defaultgrammar(self):
        
        grammars=list()
        grammars.append(nltk.grammar.Production(self.NoTdict[u"START"],[self.NoTdict[u"S"]]))
        grammars.append(nltk.grammar.Production(self.NoTdict[u"S"],[self.NoTdict[u"VP"]]))
        grammars.append(nltk.grammar.Production(self.NoTdict[u"S"],[self.NoTdict[u"NP"]]))
        grammars.append(nltk.grammar.Production(self.NoTdict[u"S"],[self.NoTdict[u"NP"],self.NoTdict[u"VP"]]))
        grammars.append(nltk.grammar.Production(self.NoTdict[u"S"],[self.NoTdict[u"VP"],self.NoTdict[u"NP"]]))
        print 'ricordati la regola impostata di prova in grammatica VP->VP S'        
        #prova
        grammars.append(nltk.grammar.Production(self.NoTdict[u"VP"],[self.NoTdict[u"VP"],self.NoTdict[u"S"]])) 
        
        return grammars

        
    def __EstraiDati(self):
        for sent in self.__corpus.tagged_sents():     
            self.__EstraiRegole(sent)
   
        np=nltk.grammar.Nonterminal(u"NP")
        vp=nltk.grammar.Nonterminal(u"VP")
        
        self.__nprules=self.__Set(self.__nprules)
        self.__vprules=self.__Set(self.__vprules)
        
        taglio=2
        self.__nprules=self.__riduciNp(taglio=taglio)        
        self.__vprules=self.__riduciVp(taglio=taglio)
                
        #ora le list diventeranno list di production
        self.__nprules=self.__addTypeRules(u"NP",self.__nprules)        
        self.__nprules=self.__RulesCleaner(self.__nprules, np)  
        
        self.__vprules=self.__addTypeRules(u"VP",self.__vprules)
        self.__vprules=self.__RulesCleaner(self.__vprules, vp)
        
        return True

    
    def __Set(self, rules):     
        lista=set()
#        for i in rules:
#            lista.add(i)
        #non potendo usare i set come sopra, trasformo in str, uso i set e poi
        #ritrasformo in lista
        l={u"#".join(l) for l in rules}
        lista=[r.split(u"#") for r in l]
        
        return list(lista)

        
    def __EstraiRegole(self, sent):
        frase=self.__sentCleaner(sent)
        np,vp=self.__NpVpExtractor(frase)
        np=self.sentoftag(np)
        vp=self.sentoftag(vp)

        self.__nprules.extend(self.__estraiNpRules(np))
        self.__vprules.extend(self.__estraiVpRules(vp))
        
        
    def __sentCleaner(self, sent):
        #pulisco la frase dalle parole inutili
        elimina=['SYM']
        fraseclean=[]    
        for tupla in sent:
            if tupla[1] not in elimina:
                fraseclean.append(tupla)
        return fraseclean
        
        
    def __NpVpExtractor(self, sent):
        i=0
        for tupla in sent:
            if tupla[1]==u'VER':
                break
            i+=1
            
        np=sent[:i]
        vp=sent[i:]

        return np, vp

    
    def sentoftag(self,sent):
        return [tupla[1] for tupla in sent]
    
    
    def __estraiNpRules(self, np):
        rules=[]
        rulz=[]

        for i in xrange(len(np)):
            if u"CON" in np:
                rulz.append(np[i])
                rules.append(rulz)
                rulz=[]
            elif np[i]==u'NOUN':
                rulz.append(np[i])
                rules.append(rulz)
                rulz=[]
            else:
                rulz.append(np[i])
        if rulz!=[]:
            rules.append(rulz)
        return rules
         
    
    def __estraiVpRules(self, vp):
        rules=[]
        rulz=[]
         
        for i in xrange(len(vp)):
            if u"CON" in vp:
                rulz.append(vp[i])
                rules.append(rulz)
                rulz=[]
            elif vp[i]==u'VER':
                rulz.append(vp[i])
                rules.append(rulz)
                rulz=[]
            else:
                rulz.append(vp[i])
        if rulz!=[]:
            rules.append(rulz)
        return rules
                 
      
    def __nNp(self, n):
        return [p for p in self.__nprules if len(p)==n]
    
    def __cnotnNp(self, n):
        return [p for p in self.__nprules if len(p)<n]
    
    def __notnNp(self, n):
        return [p for p in self.__nprules if len(p)>n]
 
         
    def __nVp(self, n):
        return [p for p in self.__vprules if len(p)==n]
    
    def __cnotnVp(self, n):
        return [p for p in self.__vprules if len(p)<n]
    
    def __notnVp(self, n):
        return [p for p in self.__vprules if len(p)>n]
       
    
    def __addTypeRules(self, type_, rules):
        """
            add type alle regoel
            
            input: il tipo da aggiungere e la lista di regole
            output: la lista con il tipo aggiunto
            
        """
######################################here#############        
        r=copy.deepcopy(rules)
        for i in xrange(len(rules)):           
            rules[i].extend([type_])
            rules
        for rul in r:
            rules.append(rul)

        return rules
  
    
    def __riduciVp(self,tipo=u"NP", taglio=int(2)):
        """
            
            Riduci rules
            
            input: il tipo di rules e lunghezza min della regola
            output: le regole Vp ridotte
            
            questa funzione si occupa di ridurre le regole np cercando le ricorrenze
            più corte all'interno delle regole più lunghe
            
            modifcando opportunamente questa funzione potrei trasformarle in chomskyiane
            
            
            modifica da fare elim vp-> n or something it isn't a verb
            
            
        """

        riduz=[r for r in self.__nVp(taglio)]
                 #regole da sanificare
        sanificate=[r for r  in self.__notnVp(taglio)]
        
#CONTROLLARE LA RIGA DI CODICE QUI SOTTO!!!!!!!!!!!!!!!!!!!
        #elimino tutte le vp che non contengono un verbo

        maxlen=0
        for ele in sanificate:
            if len(ele)>maxlen:
                maxlen=len(ele)
#        print maxlen, taglio, int(maxlen/taglio)

        #cicli di sanificazione
        ciclisanificazione=int(maxlen/taglio)
        for i in range(ciclisanificazione):
            if len(sanificate)==0:
                break
            sanificate=self.__SanificatoreRules(sanificate, riduz, u"VP", False)
            if len(sanificate)==0:
                break
            sanificate=self.__SanificatoreRules(sanificate, riduz, u"VP", True)

        #aggiungo le regole mancanti 
        sanificate.extend(riduz)
        sanificate.extend(self.__cnotnVp(taglio))
        
        rules=list()
        for r  in sanificate:
            try:
                sanificate.index(u"VER")
                rules.append(r)
            except ValueError:
                pass
            
        return rules
  
        
    def __riduciNp(self,tipo=u"NP", taglio=int(2)):
        """
            
            Riduci rules
            
            input: il tipo di rules e lunghezza min della regola
            output: le regole Np ridotte
            
            questa funzione si occupa di ridurre le regole np cercando le ricorrenze
            più corte all'interno delle regole più lunghe
            
            modifcando opportunamente questa funzione potrei trasformarle in chomskyiane
            
        """
    
        riduz=[r for r in self.__nNp(taglio)]
        #regole da sanificare
        sanificate=[r for r  in self.__notnNp(taglio)]
        
        
        maxlen=0
        for ele in sanificate:
            if len(ele)>maxlen:
                maxlen=len(ele)
#        print maxlen, taglio, int(maxlen/taglio)
                
        #cicli di sanificazione
        ciclisanificazione=int(maxlen/taglio)
        for i in range(ciclisanificazione):
            if len(sanificate)==0:
                break
            sanificate=self.__SanificatoreRules(sanificate, riduz, u"NP", False)
            if len(sanificate)==0:
                break
            sanificate=self.__SanificatoreRules(sanificate, riduz, u"NP", True)

        #aggiungo le regole mancanti 
        sanificate.extend(riduz)
        sanificate.extend(self.__cnotnNp(taglio))
        
        return sanificate
        
        
    def __SanificatoreRules(self, listSanit, listRiduz,tipo, reverse=False):
        sanificate=list()
        #sanifico le regole
        if reverse:
            listSanit.reverse()
            listRiduz.reverse()
            
        for tosaniz in listSanit:
            for ridz in listRiduz:                
                if  ridz !=None and tosaniz !=None:
                    #con questa istruzione posso usare la funzione per i cvp                                
                    if len(ridz)<len(tosaniz):
                        ls=self.ListSub(tosaniz, ridz)
#                        print 'ls', ls, tosaniz, ridz
                        if ls!=None:
                            rulz=list(tipo).extend(ls)
                            sanificate.append(rulz)

        return sanificate
        

    def __RulesCleaner(self, rules, tipo):
        rulez=set()
        for rule in rules:
            rhs=[nltk.grammar.Nonterminal(r) for r in rule] 
            s=nltk.grammar.Production(tipo, rhs)
            rulez.add(s)
        rulez=list(rulez)
        return rulez        


    def __Save(self):
        grammars=self.__defaultgrammar()
        grammars.extend(self.__vprules)
        grammars.extend(self.__nprules)
    
        print 'saved:', SaveLoad.SaveByte(grammars, self.__grammarsFilename)

        
   
    def ListSub(self, s1=u'',s2=u''):
        """
            List Sub questa funzione effettua una sottrazione di liste
            
            input: le due list() la maggiore a cui sottrarre la minore
            output: la fine della list maggiore
        
        """
        for j in xrange(len(s2)):
#            print j,s1[j],s2[j],s1[j]==s2[j]
            diverso=False                
            if s1[j]!=s2[j]:
                diverso=True
                break
        if diverso:
            return None
        else:
            return s1[j+1:]
        
        
    def Print(self, lst):
        for i in lst:
            print i
        
    def Len(self):
        return int(len(self.__nprules))+int(len(self.__vprules))
        
        
if __name__=='__main__':

    print time.asctime()
    a=GrammarExtractor()
    print time.asctime()
   
    print 'len grammars', a.Len()    
    
    print 'done'

    
    
    