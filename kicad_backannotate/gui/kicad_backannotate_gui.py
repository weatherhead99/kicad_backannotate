#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#    This file is part of kicad_backannotator
#
#    kicad_backannotator is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kicad_backannotator is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kicad_backannotator.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Fri Jan 12 06:28:53 2018

@author: danw
"""


from Ui_main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,  QInputDialog
from PyQt5.QtCore import QSettings
import sys
import os
from model import RemapTable
from kicad_backannotate.schematic_updater import SchematicUpdater
from kicad_backannotate.board_remap import string_remapping

INCH_TO_MM = 0.0393701

_KICAD_BOARD_FILTER = "pcbnew board (*.kicad_pcb)"
_KICAD_SCHEM_FILTER = "eeschema schematic (*.sch)"

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
        
        self.ui.schGroup.hide()
        
        self.ui.commitboardbutton.setEnabled(False)
        self.ui.writeSchematicButton.setEnabled(False)
        self.ui.commitboardbutton.pressed.connect(self.commitBoard)
        self.ui.writeSchematicButton.pressed.connect(self.commitSchematic)
        
        self.ui.inchRadio.toggled.connect(self.unitsChanged)
        self.ui.mmRadio.toggled.connect(self.unitsChanged)
        
        
        units = self.get_lastunits()
        if not units:
            self.ui.mmRadio.setChecked(True)
        else:
            self.ui.inchRadio.setChecked(True)
        
    def loadBoard(self, checked, filename=None):
        print(filename)
        lastdir = self.get_lastdir()
        if filename is None:
            filename,_ = QFileDialog.getOpenFileName(self,"select board file",
                                                    lastdir,_KICAD_BOARD_FILTER)
                
        if len(filename) == 0:
            return
        
        self._model = RemapTable(filename,self.ui.sortOrder.currentIndex(),
                                 self.style())
        
        self.ui.remapView.setModel(self._model)
        self.ui.remapView.selectionModel().currentChanged.connect(self.componentSelected)

        
        self.settings.setValue("lastVisitedDir",os.path.dirname(filename))
        self.ui.sortOrder.currentIndexChanged.connect(self._model.resortdata)
        self.ui.prepareSchematicButton.setEnabled(True)
        self.statusBar().showMessage("Board loaded OK")        
        self.ui.remapView.resizeColumnsToContents()
        self.ui.commitboardbutton.setEnabled(True)
        
    def prepareSchematic(self,  filename=None):
        lastdir = self.get_lastdir()
        
        if filename is None:
            filename,_ = QFileDialog.getOpenFileName(self,"select schematic file",
                                                 lastdir, _KICAD_SCHEM_FILTER)
        
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
            self.ui.writeSchematicButton.setEnabled(True)
            
        self.ui.loadBoardButton.setEnabled(False)
        self.ui.sortOrder.setEnabled(False)
        self._model.showSchematicStatus(stremap,done)
        self.ui.remapView.resizeColumnsToContents()
        self.ui.schGroup.show()
        
        self.ui.commitboardbutton.setEnabled(True)
        
        
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
        if not hasattr(self, "_model"):
            return
        
        props = self._model.getProperties(index)
        
        #mm
        self.x_mm = props["x"] / 1E6
        self.y_mm = props["y"] / 1E6
        
        self.x_inch = self.x_mm * INCH_TO_MM
        self.y_inch = self.y_mm * INCH_TO_MM
            
        self.unitsChanged(None)
        self.ui.timestampvalue.setNum(props["tstamp"])
        self.ui.footprintvalue.setText(str(props["libid"]))
        
        desig = self._model._oldvals[index.row()]
        if hasattr(self,"_updater"):
            if desig in self._updater.found_in_schematic_file:
                fname = os.path.basename(self._updater.found_in_schematic_file[desig])
                self.ui.schfilevalue.setText(fname)
            else:
                self.ui.schfilevalue.setText("")
        

    def unitsChanged(self,toggleval):
        if not hasattr(self, "x_mm"):
            return
        
        if self.ui.mmRadio.isChecked():
            self.ui.xvalue.setNum( self.x_mm)
            self.ui.yvalue.setNum(self.y_mm)
            self.settings.setValue("lastUnits", 0)
        else:
            self.ui.xvalue.setNum( self.x_inch)
            self.ui.yvalue.setNum(self.y_inch)
            self.settings.setValue("lastUnits",1)
        
    def commitBoard(self):
        lastdir = self.get_lastdir()
        self._model._remapper.change_board_references(self._model.remap)
        
        savename, _ = QFileDialog.getSaveFileName(self,"select output board file",
                                                  lastdir,_KICAD_BOARD_FILTER)
                                                  

        self._model._remapper.save_board(savename)
        self.statusBar().showMessage("saved output board %s" % savename)

    def commitSchematic(self):
        lastdir = self.get_lastdir()
        ext, ok = QInputDialog.getText(self, "extension",  "select updated schematic name append",  0, "_remapped")
        if not ok:
            return
        self._updater.save_changes(ext)
        
        self.statusBar().showMessage("saved output schematic")
        
        

def main():
    app = QApplication(sys.argv)
    mw = BackAnnotateMainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
