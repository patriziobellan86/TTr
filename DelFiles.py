# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:28:11 2015

@author: Patrizio
"""
import os
import glob
import time

class DelFiles():
    def __init__(self):
        folder="risorse\\Dati\\dialoghi\\dlg_to del\\"
        files=glob.glob(folder+'*')
        tot=len(files)
        i=float(1)
        for fil in files:
            try:
                os.remove(fil)
                print "removed ",i," - ",tot
            except:
                print "Error file: ", file
            i+=1
        
        
if __name__ =='__main__':
    print time.asctime()
    a=DelFiles()
    print time.asctime()
    print 'done'