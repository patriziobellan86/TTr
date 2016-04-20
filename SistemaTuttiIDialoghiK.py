# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 05:38:55 2015

@author: Patrizio
"""


import SaveLoad

import re


print 'sistema tutti i dialoghi k'
#funzione per non correggere la classe e rifare tutti i calcoli

dlg=SaveLoad.LoadLines('tutti i dialoghi k.txt')

i=0
for line in dlg:
    
    line=re.sub('(\s){2,}',u"#",line)
    line=re.sub('(\s){,}',u"",line)
    line=re.sub('(#)',u" ",line)
    
    print line
    
    i+=1
    
    if line>3:
        break
    
    