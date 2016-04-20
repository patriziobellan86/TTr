# -*- coding: utf-8 -*-
from time import *
import time

def LevaDApici(stringa):
    stringa=stringa.replace('"', "''")
    return stringa
    
def LevaEscape(stringa):
    #levo i caratteri di escape
    stringa=stringa.replace('\n','')
    stringa=stringa.replace('\\n','')
    stringa=stringa.replace('\t','')
    #levo i caratteri che non posso utilizzare come filename
    stringa=stringa.replace('?','_questionTag_')
    stringa=stringa.replace('\\','_backSlash_')
    stringa=stringa.replace('/','_slash_')
    stringa=stringa.replace(':','_duePunti_')
    stringa=stringa.replace(';','_puntoVirgola_')
    stringa=stringa.replace(',','_virgola_')
    stringa=stringa.replace('*','_star_')
    stringa=stringa.replace('|','_pipe_')
    stringa=stringa.replace('"','_doppiapici_')
    stringa=stringa.replace('-','_meno_')
    
    return stringa

def DataPubblicazione(data):
    #per ora gestista solo per italiano
    #registro giusto l'anno e nulla più sulla data di pubblicazione
    if len(data)>1:
        tipo=data[1]
        val=data[0]
    else:
        tipo='anni'
        val=data
        if val==u'' or val=='' or val==[]: val=0
    yy=time.localtime()
    if tipo!='anni':  val=0        
    yy=int(yy[0])-int(val)
    yy=unicode(str(yy),'utf-8')
    
    return yy