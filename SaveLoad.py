# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 00:04:34 2015

@author: Patrizio
"""

import codecs
import pickle
import os

def SaveLines(dati, filename):
    try:
        os.remove(filename)
    except:
        pass
    try:
        with codecs.open(filename, 'a', 'utf-8') as f:
            f.writelines(dati)
        return True
    except:
       return False


def SaveLinesA(dati, filename):
    try:
        with codecs.open(filename, 'a', 'utf-8') as f:
            f.writelines(dati)
        return True
    except:
        return False
        
def SaveByte(dati, filename):
    try:
        os.remove(filename)
    except:
        pass
    try:        
        out = open(filename,"wb")
        pickle.dump(dati, out)
        out.close()
        return True
    except:
        return False

  
def LoadLines(filename):
    try:
        with codecs.open(filename, 'r', 'utf-8') as f:
            dati_=[]            
            for line in f.readlines():
                dati_.append(line)
        return dati_
    except:
        return False
        
def LoadByte(filename):
    try:
        in_s=open(filename,'rb')
        dati=pickle.load(in_s)
        in_s.close()
        
        return dati    
    except IOError:
        return False
  
            
            
if __name__=='__main__':
    a=LoadLines('risorse\\Dati\\parole.txt')
    print a            
            
            
            