# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import SaveLoad

import AnalizzatoreSents
import time


from sklearn.feature_extraction.text import TfidfVectorizer

filename="C:\\Esame TTR\\risorse\\Dati\\dialoghi\\dialoghiRaw\\Burn_Notice.txt"

dlg=SaveLoad.LoadLines(filename)

#analiz=AnalizzatoreSents.AnalizzatoreSents()

print time.asctime()
print 'creo copia in analiz'
#copia per analiz
dlgcopy=dlg#analiz.Analisi(dlg)
print time.asctime()


tfidf = TfidfVectorizer()
print time.asctime()
print 'creo tfidf'
tfidfdata = tfidf.fit_transform(dlgcopy)
vocab=tfidf.get_feature_names()
print type(vocab)

print SaveLoad.SaveByte(tfidfdata,"C:\\Esame TTR\\risorse\\Dati\\dialoghi\\Burn_Notice.dat")
print SaveLoad.SaveByte(vocab,"C:\\Esame TTR\\risorse\\Dati\\dialoghi\\Burn_Notice.voc")
#   voc=SaveLoad.LoadByte("C:\\Esame TTR\\risorse\\Dati\\dialoghi\\whip it.voc")
print time.asctime()
print 'done'

