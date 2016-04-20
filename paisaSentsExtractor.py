# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 16:20:20 2015


    CLASSE FINITA IL 06/08/2015

@author: Patrizio
"""

from __future__ import unicode_literals

import PulisciSent

import os
import codecs
import glob


def ConverterISST_to_MorphIt(cpos):
    converter= {'A':'ADJ',
                'B':'ADV',
                'C':'CON',
                'D':'DET',
                'E':'PRE',
                'F':'PUNC',
                'I':'INT',
                'N':'NUM',
                'P':'PRO',
                'R':'ART',
                'S':'NOUN',
                'T':'ADJ',
                'V':'VER',
                'X':'WH'}
    
    try:
        tipo= converter[cpos]
        return tipo
    except KeyError:
        print 'TIPO: ', cpos,'Non Implementato'
        return False
        
class PaisaSentsExtractor():
    """ 
    questa classe si occupa di estrarre i dati dal file paisa e di salvarli \
    in files separati. uno per ogni frase
    """
    def _tipoClasse(self):
        return "estrattore di dati"
    def _statoLavorazione(self):
        return "in testing"
    def _todo(self):
        return "nothing"
    def _dataUltimazione(self):
        return "25\08\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-a"
    def __init__(self):
        #per i conteggi uso i float per evitare overflow
        self.__folderPeriodi="paisa\\periods\\"
        self.__folderFrasi="risorse\\Dati\\training\\paisaTagged\\"
        
        self.__SeparaInFrasiIFiles()
        
        print "estrazione di sents da periods in paisa"
        
    
    def __SeparaInFrasiIFiles(self):
        """
        LEGGO OGNI SINGOLO FILE E LO DIVISO IN FILES DI FRASI
        """
        pulisci=PulisciSent.PulisciSent()
        filetosave=int(len(glob.glob(self.__folderFrasi+'*')))
        i=float(1)
        tot=len(glob.glob(self.__folderPeriodi+'*'))
        for fil in glob.glob(self.__folderPeriodi+'*'):
            print "sents extractor - file:", fil," - ",i,"/", tot            

            with codecs.open(fil, 'r','utf-8') as f:
                strfile=f.readlines()
            frase=[]
            
            for line in strfile:
                if line!='\n':
                    line=line[:-1]+"\t_\t_\n"
                    frase.append(line)        
                elif frase!=[]:
                    
                    filetosave+=1                   
                    filename2=self.__folderFrasi+str(filetosave)+'.conlltaggedsent'
                    
                    print "saving file: ", filename2
                    with codecs.open(filename2, mode='a', encoding='utf-8') as f:
                        for linea in frase:
                            linea=linea.split(u'\t')
                            if len(pulisci.Pulisci(linea[1].strip()))>0:
                                linea[1]=linea[1].lower()
                                linea[2]=linea[2].lower()
                                linea[3]=ConverterISST_to_MorphIt(linea[3])
                                linea[4]=linea[3]
                                linea=u"\t".join(linea)
                            f.writelines(linea)
                    frase=[]
                else:
                    frase=[]
            
            try:
                os.remove(fil)
            except:
                pass
        
            i+=1
#            
#            if i>3:
#                break
            if filetosave==50000:
                print "50000 files estratti\n exit"
            
if __name__=='__main__':

    a=PaisaSentsExtractor()
    
    print 'done'
    