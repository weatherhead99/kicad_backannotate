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

INCH_TO_MM = 0.0393701

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
        
        units = self.get_lastunits()
        if not units:
            self.ui.mmRadio.setChecked(True)
        else:
            self.ui.inchRadio.setChecked(True)
            
        

        
    def loadBoard(self):
        lastdir = self.get_lastdir()
        filename,_ = QFileDialog.getOpenFileName(self,"select board file",
                                                 lastdir,"pcbnew board (*.kicad_pcb)")
                
        if len(filename) == 0:
            return
        
        self._model = RemapTable(filename,self.ui.sortOrder.currentIndex(),
                                 self.style())
        
        self.ui.remapView.setModel(self._model)

        
        self.settings.setValue("lastVisitedDir",os.path.dirname(filename))
        self.ui.sortOrder.currentIndexChanged.connect(self._model.resortdata)
        self.ui.prepareSchematicButton.setEnabled(True)
        self.statusBar().showMessage("Board loaded OK")        
        self.ui.remapView.resizeColumnsToContents()
        
        self.ui.remapView.selectionModel().currentChanged.connect(self.componentSelected)
        
        self.ui.inchRadio.toggled.connect(self.unitsChanged)
        self.ui.mmRadio.toggled.connect(self.unitsChanged)
        
    def prepareSchematic(self):
        lastdir = self.get_lastdir()
        filename,_ = QFileDialog.getOpenFileName(self,"select schematic file",
                                                 lastdir, "eeschema schematic (*.sch)")
        
        if len(filename) == 0:
            return
        
        self._updater = SchematicUpdater(filename)
        stremap = string_remapping(self._model.remap)
        done = self._updater.recursive_remap(stremap)
        
        if len(done) != len(stremap):
            self.statusBar().showMessage("WARNING: some symbols not found!")
            self._allsymsfound = False
        else:
            self.statusBar().showMessage("Schematic loaded OK, all symbols found")
            self._allsymsfound = True
        self.ui.loadBoardButton.setEnabled(False)
        self.ui.sortOrder.setEnabled(False)
        self._model.showSchematicStatus(stremap,done)
        self.ui.remapView.resizeColumnsToContents()
        
    def get_lastdir(self):
        lastdir_variant=self.settings.value("lastVisitedDir")
        if not lastdir_variant:
            lastdir = ""
        else:
            lastdir = str(lastdir_variant)
        
        return lastdir

    def get_lastunits(self):
        units_variant = self.settings.value("lastUnits")
        units = 0 if not units_variant else int(units_variant)
        return units
        
    def componentSelected(self,index,previous):
        props = self._model.getProperties(index)
        
        #mm
        self.x_mm = props["x"] / 1E6
        self.y_mm = props["y"] / 1E6
        
        self.x_inch = self.x_mm * INCH_TO_MM
        self.y_inch = self.y_mm * INCH_TO_MM
            
        self.unitsChanged(None)
        self.ui.timestampvalue.setNum(props["tstamp"])
        self.ui.footprintvalue.setText(str(props["libid"]))

    def unitsChanged(self,toggleval):
        if self.ui.mmRadio.isChecked():
            self.ui.xvalue.setNum( self.x_mm)
            self.ui.yvalue.setNum(self.y_mm)
            self.settings.setValue("lastUnits", 0)
        else:
            self.ui.xvalue.setNum( self.x_inch)
            self.ui.yvalue.setNum(self.y_inch)
            self.settings.setValue("lastUnits",1)
        
        



if __name__ == "__main__":
    
    
    
    app = QApplication(sys.argv)

    mw = BackAnnotateMainWindow()

    
    sys.exit(app.exec_())