# -*- coding: utf-8 -*-
"""

>>> pattern =
... ^                   # beginning of string
... M{0,4}              # thousands - 0 to 4 M's
... (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
...                     #            or 500-800 (D, followed by 0 to 3 C's)
... (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
...                     #        or 50-80 (L, followed by 0 to 3 X's)
... (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
...                     #        or 5-8 (V, followed by 0 to 3 I's)
... $                   # end of string


>>> re.search(pattern, 'M', re.VERBOSE)

self.lemmaTipoListLemma[(lemma, tipo)].append([vocabolo,  tipo]) 

        
        
Created on Thu Aug 27 02:41:14 2015


        
        
        classe di Stem




@author: Patrizio
"""
from __future__ import unicode_literals, division

import SaveLoad
import ErrorLog2
import morphItDataExtractor

import collections

class StemmerIt():
    def _tipoClasse(self):
        return "estrattore di dati"
    def _statoLavorazione(self):
        return "in fitting con il progetto"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "01/09/2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"
        
    def __init__(self):       
        self.__InizializzaCostantiClasse()
        self.__InizializzaVariabiliClasse()
        
        
    def __InizializzaCostantiClasse (self):
        """
        inizializzo tutte le costanti di classe
        """
        self.folder="risorse\\Dati\\"
        
        self.escludiTag=[u"SYM",u"NUM",u"PUNC"]
    
    def __InizializzaVariabiliClasse(self):
        """
        inizializza le variabili interne della classe
        
        inizializzo TUTTE le variabili interne
        """
#        self.wordsFreqFilename=self.folder+"wordsFreq.dictlist"
        
        self.suffissiTagFilename=self.folder+"suffissiTag.dictset"
        
#        self.suffissiStemFilename=self.folder+"Stemmer.dat"
        
        if not self.Load():
            print "file di dati mancante\nestrazione in corso..."
            morphItDataExtractor.MorphItDataExtractor()
            if not self.Load():
                print "estrazione dati non corretta....\n impossibile continuare"
    
    def StemSents(self, sents):
        """
            
            StemSents: effettua le stem di frasi
            
            input:list(list(tuple(word,tag)))
            output:list(list(tuple(word,tag)))
        """
        return [self.StemSent(sent) for sent in sents]
        
        
    def StemSent(self, sent):
        """
            StemSent: effettua lo stem di un intera frase
            
            input: list(tuple(word,tag))
            output: list(tuple(word,tag))
            
        """
        
        ssent=list()
        for wordTag in sent:
            wordTag=self.StemWord(wordTag)
            if wordTag:
                ssent.append(wordTag)
            
        return ssent
        
        
    def StemWord(self, wordTag):
        """
            
            StemWordTag: effettua lo stem di una parola
            
            input: tuple(word,tag)
            outpu: tuple(Stemword, tag)
        
        """
        
        word=wordTag[0]
        tag=wordTag[1]        
        lsuff=list()
        maxsuff=u""
        
        if tag not in self.escludiTag:
            for suff in self.suffissiTag[tag]:
                if word.endswith(suff):
                    lsuff.append(suff)
                    if len(suff)>len(maxsuff):
                        maxsuff=suff

            if maxsuff==word:
                return wordTag
            return tuple([word[:-len(maxsuff)], tag])
        
        return False
        
        
    def Save(self):
        
        
        return True
        
        
    def Load(self):
        self.suffissiTag=SaveLoad.LoadByte(self.suffissiTagFilename)
        if self.suffissiTag:
            return True
            
        return False

        
if __name__=='__main__':
    import time
    
    print time.asctime()
    a=StemmerIt()
    print time.asctime()
    
    sent=[tuple(['sei','VER']),tuple(['giochiamo','NOUN']), tuple(['!','PUNC'])]
    print sent
    print a.StemSent(sent)
    print time.asctime()
    
    print 'done'












