# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 20:42:36 2015

@author: Patrizio
"""
import glob
import SaveLoad

print "accorpo tutti i dialoghi in uno solo"

fileunicoFilename="risorse\\Dati\\dialoghi\\dialoghiRaw\\tutti i dialoghi.txt"

files=glob.glob("risorse\\Dati\\dialoghi\\dialoghiRaw\\"+'*')
dlg=list()

for file in files:
    dialogo=SaveLoad.LoadLines(file)
    dlg.extend(dialogo)
    
print "salvataggio file unico"
print SaveLoad.SaveLines(dlg, fileunicoFilename)

print 'done'