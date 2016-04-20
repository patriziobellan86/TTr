# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 04:02:51 2015

@author: Patrizio
"""


def Features(dati):
    features=list()

    for dato in dati:
        if len(dato[0])>3:
            i=dato[0][:2]
            fs=dato[0][-1:]
            fd=dato[0][-2:]
            ft=dato[0][-3:]
            
            feature={'i':i,'fs':fs,'fd':fd,'ft':ft}
            features.append([feature, dato[1]])
        
    return features
    
 
def Feature(dato):
    i=dato[:2]
    fs=dato[-1:]
    fd=dato[-2:]
    ft=dato[-3:]
           
    return {'i':i,'fs':fs,'fd':fd,'ft':ft}
    
import SaveLoad

svm=SaveLoad.LoadByte("SVM_mf.tmp")
dt=SaveLoad.LoadByte("NLTK_DTP_mf.tmp")
word='caschereste'

w=Feature(word)
print svm.classify(w)