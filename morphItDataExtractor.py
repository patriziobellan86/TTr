#-*- encoding:utf-8 -*-
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


"""

from __future__ import unicode_literals, with_statement, division


import SaveLoad

import re
import codecs
import collections

class MorphItDataExtractor(object):
    """
    questa classe si occupa di estrarre i dati da morphIt
    li registra e li ragruppa
    
    """    
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
        
        self.folderpath="risorse\\Dati\\"
        self.MorphItFileName=self.folderpath+"morphIt\\"+"morphitUtf8.txt"
        

        self.__InizializzaVarInterne()
        
        #compila subito i pattern per re
        self.__CompilaRe()
        
        self.__LeggiMorphIt()
        self.__CreaRadiciSuffissi()


        self.Save()
            
            
    def __InizializzaVarInterne(self):
#        self.paroleFilename=self.folderpath+"parole.list"
#        self.parole=[]
        self.suffissiTagFilename=self.folderpath+"suffissiTag.dictset"
#        
#        self.lemmaFilename=self.folderpath+"lemma.defdict"
#        self.radiciListFilename=self.folderpath+"radiciList.defdict"
#    
#        self.lemmaRadiceFilename=self.folderpath+"lemmaRadice.dict"
#        self.lemmaSuffissoFilename=self.folderpath+"lemmaSuffisso.dict"
#        
#        self.lemmaTipoFilename=self.folderpath+"lemmaTipo.defdict"
#        self.lemmaTipoEstesoFilename=self.folderpath+"lemmaTipoEsteso.defdict"
#        self.lemmaTipolistLemmaFilename=self.folderpath+"lemmaTipoListLemma.defdict"
#        self.lemmaTipoListVocaboloFilename=self.folderpath+"lemmaTipoListVocabolo.defdict"
#    
#        self.tipoListFilename=self.folderpath+"tipoList.defdict"

 
        #lemma[lemma]=[elenco vocaboli con stesso lemma di partenza]
        self.lemma=collections.defaultdict(list)
        #radiciList[lemma]=[elenco di tutte le radici estratte per quel lemma]        
        self.radiciList=collections.defaultdict(list)
        
        #dizionario contentente come key il lemma e come value la radice del vocabolo
        self.lemmaRadice=dict()
        #dizionario contentente come key il lemma e come value il suffisso del vocabolo
        self.lemmaSuffisso=dict()

#        #dizionario che usa il vocabolo come key e restituisce i tipi di quel vocabolo
        self.lemmaTipo=collections.defaultdict(list)
#        
         
         #dizionario che usa il vocabolo come key e restituisce la lista di tuple (lemma, tipo)
#        self.lemmaTipoEsteso=collections.defaultdict(list)
#        
#        #dizionario contentente per key tuple(lemma, tipo)
#        self.lemmaTipoListLemma=collections.defaultdict(list)
#        
#        #dizionario contentente per key tuple(vocabolo, tipo)
#        self.lemmaTipoListVocabolo=collections.defaultdict(list)
#        
#        
#        #dizionario key tipo parola, values list vocaboli di quel tipo
        self.tipoList=collections.defaultdict(list)
        
        
        
        
        
        #USO QUESTA VAR PER LO STEMMER, LE ALTRE NON MI SERVONO
        self.suffissiFilename=self.folderpath+"SUFFISSI.dictset"
        self.suffissiTag=collections.defaultdict(set)
        
        
        
        
        

    
        
    def __CompilaRe(self):        
        #compilazione re
        self.__pattern_noun = r'^NOUN+'
        self.__pat_noun = re.compile(self.__pattern_noun)
        
        self.__pattern_art = r'^ART+'
        self.__pat_art = re.compile(self.__pattern_art)
        
        self.__pattern_pro = r'^PRO+'
        self.__pat_pro = re.compile(self.__pattern_pro)
        
        self.__pattern_det = r'^DET+'
        self.__pat_det = re.compile(self.__pattern_det)
        
        self.__pattern_pre = r'^PRE+'
        self.__pat_pre = re.compile(self.__pattern_pre)
        
        self.__pattern_npr = r'^NPR+'
        self.__pat_npr = re.compile(self.__pattern_npr)

        self.__pattern_verb = r'^VER|^AUX|^MOD|^CAU|^ASP+'
        self.__pat_verb = re.compile(self.__pattern_verb)

        self.__pattern_adj = r'^ADJ+'
        self.__pat_adj = re.compile(self.__pattern_adj)
        
        self.__pattern_adv = r'^ADV+'
        self.__pat_adv = re.compile(self.__pattern_adv)
        
        self.__pattern_sym = r'^SYM|^SMI|^SENT+'
        self.__pat_sym = re.compile(self.__pattern_sym)
        
        self.__pattern_pon = r'^PON+'
        self.__pat_pon = re.compile(self.__pattern_pon)
        
        self.__pattern_abl = r'^ABL+'
        self.__pat_abl = re.compile(self.__pattern_abl)
        
        self.__pattern_con = r'^CON+'
        self.__pat_con = re.compile(self.__pattern_con)
        
        self.__pattern_num = r'^INT|DET-NUM-CARD|PRO-NUM+'
        self.__pat_num = re.compile(self.__pattern_num)
        
        self.__pattern_wh = r'^WH+'
        self.__pat_wh = re.compile(self.__pattern_wh)
        
        
        
#        
#        #informazioni morfologiche lemma
#        self.__pattern_singolare = r':s+'
#        self.__pat_singolare = re.compile(self.__pattern_singolare)
#       
#        self.__pattern_plurale = r':p+'
#        self.__pat_plurale = re.compile(self.__pattern_plurale)
# 
#        self.__pattern_maschile = r'-M+'
#        self.__pat_maschile = re.compile(self.__pattern_maschile)
#       
#        self.__pattern_femminile = r'-F+'
#        self.__pat_femminile = re.compile(self.__pattern_femminile)
#       
#       
         
    def __LeggiMorphIt(self):
        try:
            with codecs.open(self.MorphItFileName,'r', 'utf-8') as f:
                g=f.readlines()
            for l in g:    
                tmp=l.split()
                if len(tmp)==3:
                    self.__OrganizzaTipi(tmp)
            return True
        
        except IOError:
            print "Errore: File "+ self.MorphItFileName + " MANCANTE!\n impossibile procedere"
            return False
            
    def __OrganizzaTipi(self, testo):
        #uso match perchè cerco all'inizio della stringa e non c'è bisogno di 
        #cercare nell'intera stringa
#        print testo[0], testo[1], testo[2]
        

        vocabolo=testo[0]            
        lemma=testo[1]
        

        #questa var mi salva i dati per la classe SinonimiContrariDataExtractor        
#        self.parole.append(vocabolo)
        
        ##############  Ricerca tipo con Re  ##################
    
        #noun - nome
    
        match=re.match(self.__pat_noun, testo[2])
        if match:
#            self.parole.append(vocabolo)
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_noun[1:-1])
            return 
        #art - articolo
        match=re.match(self.__pat_art, testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_art[1:-1])
            return 
        #pro - proposizione
        match=re.match(self.__pat_pro, testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_pro[1:-1])
            return 
        #det - determinativo
        match=re.match(self.__pat_det, testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_det[1:-1])
            return 
        #pre - preposizione  
        match=re.match(self.__pat_pre, testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_pre[1:-1])
            return 
        #npr - 
        match=re.match(self.__pat_npr,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_npr[1:-1])
            return 
        #verb - verbo
        match=re.match(self.__pat_verb,testo[2])
        if match:
#            self.parole.append(vocabolo)
            self.__popolaVarDict(vocabolo, lemma, "VER")      #self.__pattern_verb[1:-1]
            return 
        #adj - aggettivo
        match=re.match(self.__pat_adj,testo[2])
        if match:
#            self.parole.append(vocabolo)
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_adj[1:-1])
            return 
        #adv - avverbio
        match=re.match(self.__pat_adv,testo[2])
        if match:
#            self.parole.append(vocabolo)
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_adv[1:-1])
            return 
        #num - numero
        match=re.match(self.__pat_num,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, "NUM")   #self.__pattern_num[1:-1]
            return 
        #sym - simbolo
        match=re.match(self.__pat_sym,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, "SYM")   #self.__pattern_sym[1:-1]
            return 
        #pon -  
        match=re.match(self.__pat_pon,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_pon[1:-1])
            return 
        #abl - 
        match=re.match(self.__pat_abl,testo[2])     
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_abl[1:-1])
            return 
        #con -
        match=re.match(self.__pat_con,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_con[1:-1])
            return 
        #wh - wh 
        match=re.match(self.__pat_wh,testo[2])
        if match:
            self.__popolaVarDict(vocabolo, lemma, self.__pattern_wh[1:-1]) 
            return 
     
     
    def __popolaVarDict(self, vocabolo, lemma, tipo):
        self.lemma[lemma].append(vocabolo)
#                            
        self.lemmaTipo[vocabolo].append(tipo) 
#        self.lemmaTipoEsteso[vocabolo].append(([lemma, tipo])) 
#        
#        self.lemmaTipoListLemma[(lemma, tipo)].append([vocabolo,  tipo]) 
#        self.lemmaTipoListVocabolo[(vocabolo, tipo)].append([lemma,  tipo]) 
#
        self.tipoList[tipo].append(vocabolo)


    def __CreaRadiciSuffissi(self):
        self.__CreaRadici()
        self.__CreaSuffissi()
        
        
    def __CreaRadici(self):
        """
        questa funzione itera su self.lemma per estrarre le radici dei nomi
        
        """
    
        # creo i dizionari con le radici estratte da uno stesso lemma
        for k in self.lemma.keys():
            for w in self.lemma[k]:
                radice=self.__EstraiRadice(k,w)
                if radice !=None:
                    self.radiciList[k].append(radice)
                    
        #raggruppo le radici di ogni lemma ed estraggo la radice comune
        for k in self.radiciList.keys():      
            minlen=min(self.radiciList[k])
            maxlen=max(self.radiciList[k])

            r=self.__EstraiRadice(minlen, maxlen)

            #creo il dizionario self.lemmaRadice -> diz[lemma]=radice
            for w in self.lemma[k]:
                self.lemmaRadice[w]=r   


    def __EstraiRadice(self, lemma=u'', vocabolo=u''):
        r,s=self.ListSub(lemma, vocabolo)
        
        return r


    def __CreaSuffissi(self):
        for k in set(self.lemma.keys()):
            for w in self.lemma[k]:
                s=self.__EstraiSuffisso(self.lemmaRadice[w],w)
                self.lemmaSuffisso[w]=s
#############NEEEEEEEEWWWWWWWWWWWWWWWWW#########################      
                for tipo in self.lemmaTipo[k]:
                    if len(s)>0:
                        self.suffissiTag[tipo].add(s)      
      
      
    def __EstraiSuffisso(self, radice=u'', vocabolo=u''):
         r,s=self.ListSub(vocabolo, radice)
         return s


#    def __EstraiRadiciSuffissi(self, voc, lem, tipo):
##        print voc, lem, tipo
#        radice, suffisso=self.ListSub(voc, lem)
#        
#        #New
#        
#        if suffisso!=u"":
#            self.suffissiTag[tipo].add(suffisso)
#        
##        if radice !=u'':
##            radice=tuple([radice, tipo])
##            self.radici.append(radice)
##            suffisso=tuple([suffisso, tipo])
##            self.suffissi.append(suffisso)
#        
    
    def ListSub(self, s1=u'',s2=u''):
        """
        questa funzione effettua una sottrazione di liste
        
        return s1 - s2
        """
        
        s1=list(s1)
        s2=list(s2)
        
        lens1=len(s1)
        lens2=len(s2)    
        
        if lens1>lens2:
            #devo completare s2 per farla diventare lunga uguale
            tmp=list(u' '*lens1)
            s2=s2+tmp[lens2:]
    
        elif lens2>lens1:
            #devo completare s1 per farla diventare lunga uguale        
            tmp=list(u' '*lens2)
            s1=s1+tmp[lens1:]
        lens1=len(s1)
        
        radice=[]
        
        for i in xrange(lens1):
            if s1[i]!=s2[i]:
                break
            radice.append(s1[i])
        
        suffisso=s1[len(radice):]
        
        radice=u''.join(radice)
        suffisso=u''.join(suffisso)
        
        return radice, suffisso   
    
    
    def Save(self):
        try:        
#            SaveLoad.SaveByte(self.lemma, self.lemmaFilename)
#            SaveLoad.SaveByte(self.radiciList, self.radiciListFilename)
#        
#            SaveLoad.SaveByte(self.lemmaRadice, self.lemmaRadiceFilename)
#            SaveLoad.SaveByte(self.lemmaSuffisso, self.lemmaSuffissoFilename)
#
#            SaveLoad.SaveByte(self.lemmaTipo, self.lemmaTipoFilename)
#            SaveLoad.SaveByte(self.lemmaTipoEsteso, self.lemmaTipoEstesoFilename)
#            
#            SaveLoad.SaveByte(self.lemmaTipoListLemma, self.lemmaTipolistLemmaFilename)
#        
#            SaveLoad.SaveByte(self.lemmaTipoListVocabolo, self.lemmaTipoListVocaboloFilename)
#        
#            SaveLoad.SaveByte(self.tipoList, self.tipoListFilename)
#            
#            
#            
#            #sicuro da tenere            
#            SaveLoad.SaveByte(self.parole,self.paroleFilename)
#  
#            self.SalvaRadici()
#            
            self.SalvaAbrev()
            print SaveLoad.SaveByte(self.suffissiTag,self.suffissiTagFilename)
            
            return True
        except:
            
            return False
            
#    def SalvaRadici(self):
#        suffissiTag=collections.defaultdict(set)
#        for tupla in self.lemmaTipoListVocabolo.keys():
#            voc=tupla[0]
#            tipo=tupla[1]
#            
#            radici=self.lemmaSuffisso[voc]
#            suffissiTag[tipo].add(radici)
#            
#        SaveLoad.SaveByte(suffissiTag, self.suffissiTagFilename)
#        
#        return True

    def SalvaAbrev(self):
        abl=self.tipoList[u"ABL"]
        #SaveLoad.SaveByte(abl, "risorse\\Dati\\abbrev_.abl")
        abl=u"\n".join(abl)
        SaveLoad.SaveLinesA(abl,"risorse\\Dati\\abl.abl")
            
            
                  
#    def Load(self):
#        try:
#            self.lemma=SaveLoad.LoadByte(self.lemma)
#            self.radiciList=SaveLoad.LoadByte(self.radiciList)
#        
#            self.lemmaRadice=SaveLoad.LoadByte(self.lemmaRadice)
#            self.lemmaSuffisso=SaveLoad.LoadByte(self.lemmaSuffisso)
#
#            self.lemmaTipo=SaveLoad.LoadByte(self.lemmaTipo)
#            self.lemmaTipoEsteso=SaveLoad.LoadByte(self.lemmaTipoEsteso)
#            
#            self.lemmaTipoListLemma=SaveLoad.LoadByte(self.lemmaTipoListLemma)
#        
#            self.lemmaTipoListVocabolo=SaveLoad.LoadByte(self.lemmaTipoListVocabolo)
#
#            self.tipoList=SaveLoad.LoadByte(self.tipoList)
#
#            return True
#        except:
#             
#             return False


if __name__=='__main__':
    print 'start'
    a=MorphItDataExtractor()
       
    print 'done'