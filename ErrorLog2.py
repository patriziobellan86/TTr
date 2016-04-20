# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:14:46 2015

@author: Patrizio
"""
import time

class ErrorLog():
    def _tipoClasse(self):
        return "error log"
    def _statoLavorazione(self):
        return "testata"
    def _dataUltimazione(self):
        return "23\06\2015"
    def __author__(self):
        return "Patrizio Bellan \n patrizio.bellan@gmail.com"
    def __version__(self):
        return "0.1-b"

    def __init__(self, className='classe in errore', functionName='funzione in errore', errorDescription=[]):
        """ questa classe si occupa della registrazione degli errori ottenuti a run-time
        """
        self.__pathFile='risorse\\dati\\'
        self.__extFile='.errorLog'
        
        self.__fileName=self.__pathFile+'ErrorLog'+self.__extFile
    
        self.__errorClassName=str(className)
        self.__errorFunctionName=str(functionName)
        self.__errorDescription=errorDescription
    
    
        self.__SalvaErroreFile()
        
    def __SalvaErroreFile(self):    
        try:
            with file(self.__fileName,'a')as f:
                f.write('<error>\n')
                datetime=time.localtime()
                s='date time           : yy_'+str(datetime.tm_year)+' mm_'+str(datetime.tm_mon)+' dd_'+str(datetime.tm_mday)+ \
                  ' hh_'+str(datetime.tm_hour)+' mm_'+str(datetime.tm_min)+'\n'
                s=str(s)
                f.write(s) 
                s='class               : '+ self.__errorClassName+'\n'
                s=str(s)
                f.write(s)
                s='    function        : '+ self.__errorFunctionName+'\n'
                s=str(s)
                f.write(s)
                s='  error information :\n'
                f.write(s)
                s='-'*75+'\n'
                f.write(s)
                for err in self.__errorDescription:
                    s=str(err)
                    f.write(s)
                    s='\n'+'-'*75+'\n'
                    f.write(s)
                    
                f.write('</error>\n')
            return True
            
        except IOError, e:
            print 'ERRORE NELLA CLASSE ErrorLog'
            for err in e:
                print err
            return False
            
if __name__=='__main__':
    print 'test classe'
    a=ErrorLog('test classe', 'funzione test classe',['errore generico n','descrizione errore'])