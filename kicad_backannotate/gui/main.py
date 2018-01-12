#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 06:28:53 2018

@author: danw
"""

from ui_main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtCore import pyqtSlot, QMetaObject, QSettings
import sys
sys.path.append("/home/danw/Software/kicad_dist/lib/python2.7/site-packages")
import os
from model import RemapTable

sys.path.append("/home/danw/Software/kicad_backannotate/")
from kicad_backannotate.schematic_updater import SchematicUpdater, get_remaining
from kicad_backannotate.board_remap import string_remapping

class BackAnnotateMainWindow(QMainWindow):
    def __init__(self):
        super(BackAnnotateMainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.loadBoardButton.clicked.connect(self.loadBoard)
        self.ui.prepareSchematicButton.clicked.connect(self.prepareSchematic)

        self.settings = QSettings("kicad_backannotate","kicad_backannotate")
        
        self.ui.prepareSchematicButton.setEnabled(False)
        self.ui.writeSchematicButton.setEnabled(False)
        self.show()
        

        
    def loadBoard(self):
        lastdir = self.get_lastdir()
        filename,_ = QFileDialog.getOpenFileName(self,"select board file",
                                                 lastdir,"pcbnew board (*.kicad_pcb)")
                
        if len(filename) == 0:
            return
        
        self._model = RemapTable(filename,self.ui.sortOrder.currentIndex())
        self.ui.remapView.setModel(self._model)
        
        self.settings.setValue("lastVisitedDir",os.path.dirname(filename))
        
        self.ui.sortOrder.currentIndexChanged.connect(self._model.resortdata)
        
        self.ui.prepareSchematicButton.setEnabled(True)
        self.statusBar().showMessage("Board loaded OK")
        
        
    def prepareSchematic(self):
        lastdir = self.get_lastdir()
        filename,_ = QFileDialog.getOpenFileName(self,"select schematic file",
                                                 lastdir, "eeschema schematic (*.sch)")
        
        if len(filename) == 0:
            return
        
        self._updater = SchematicUpdater(filename)
        stremap = string_remapping(self._model.remap)
        done = self._updater.recursive_remap(stremap)
        
        
    def get_lastdir(self):
        lastdir_variant=self.settings.value("lastVisitedDir")
        if not lastdir_variant:
            lastdir = ""
        else:
            lastdir = str(lastdir_variant)
        
        return lastdir



if __name__ == "__main__":
    
    
    
    app = QApplication(sys.argv)

    mw = BackAnnotateMainWindow()

    
    sys.exit(app.exec_())