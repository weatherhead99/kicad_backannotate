from kicad_backannotate.gui.kicad_backannotate_gui import BackAnnotateMainWindow

from PyQt5.QtWidgets import QApplication
import sys
from pkg_resources import resource_filename
import os

BOARD_FILE=resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.kicad_pcb")
SCH_FILE=resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.sch")

if __name__ == "__main__":
    os.mkdir("screenshots")
    
    app = QApplication(sys.argv)
    mw = BackAnnotateMainWindow()
    
    #main window
    ss_mainwindow = mw.grab()
    ss_mainwindow.save("screenshots/mainwindow.png")
    
    #load a board
    mw.loadBoard(False, BOARD_FILE)
    app.processEvents()
    
    ss_boardloaded = mw.grab()
    ss_boardloaded.save("screenshots/board_loaded.png")

    #select an item
    mw.ui.remapView.selectRow(2)
    app.processEvents()
    
    ss_compselected = mw.grab()
    ss_compselected.save("screenshots/component_selected.png")
    
    #load the schematic
    mw.prepareSchematic(SCH_FILE)
    mw.ui.remapView.selectRow(3)
    app.processEvents()
    
    ss_schemloaded = mw.grab()
    ss_schemloaded.save("screenshots/schematic loaded.png")
    
