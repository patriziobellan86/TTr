# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 03:48:12 2015

@author: Patrizio
"""

from __future__ import unicode_literals


import DialogoQuestEngine
import GeneratoreLinguistico


import os
import glob


class CreatoreDlgGenLin():
    def __init__(self):
        self.folder="risorse\\Dati\\"
        self.folderDialoghiRaw=self.folder+"dialoghi\\dialoghiRaw\\"
        
        files=glob.glob(self.folderDialoghiRaw+'*')        
        files=[os.path.basename(file) for file in files]
        
        #per ogni dlg imposto risposta così mi creai i vari files
        for file in files:
            file=file[:-4]
            
            print file
            print
            print "dialogQuestEngine"
            DialogoQuestEngine.QuestEngine(file)
            print "generatoreLinguistico"
            GeneratoreLinguistico.HMMLanguageGenerator(file)
    
if __name__=='__main__':
    a=CreatoreDlgGenLin()    
    
    print 'done'