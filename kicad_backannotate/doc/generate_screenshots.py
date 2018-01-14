from kicad_backannotate.gui.kicad_backannotate_gui import BackAnnotateMainWindow

from PyQt5.QtWidgets import QApplication
import sys
from pkg_resources import resource_filename
import os

from PyQt5.QtGui import QPainter,  QColor

BOARD_FILE=resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.kicad_pcb")
SCH_FILE=resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.sch")

PAINT_COLOR = (255, 0, 0)

def get_widget_bbox(widget):
    return (widget.x(),  widget.y(),  widget.width(),  widget.height())

def draw_rect(pixmap, box):
    painter = QPainter()
    painter.begin(pixmap)
    painter.setPen(QColor(*PAINT_COLOR))
    painter.drawRect(*box)
    pass

def highlight_widget(pixmap, widget):
    box  = get_widget_bbox(widget)
    draw_rect(pixmap, box)

def main():
    try:
        os.mkdir("screenshots")
    except OSError:
        #directory exists already
        pass
    
    app = QApplication(sys.argv)
    mw = BackAnnotateMainWindow()
    
    #main window
    ss_mainwindow = mw.grab()
    ss_mainwindow.save("screenshots/mainwindow.png")
    
    #button to click on to load board
    highlight_widget(ss_mainwindow,  mw.ui.loadBoardButton)
    ss_mainwindow.save("screenshots/mainwindow_loadboardbutton.png")
    
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
    
    highlight_widget(ss_compselected, mw.ui.commitboardbutton)
    ss_compselected.save("screenshots/mainwindow_commitboardbutton.png")
    
    ss_compselected = mw.grab()
    highlight_widget(ss_compselected, mw.ui.prepareSchematicButton)
    ss_compselected.save("screenshots/mainwindow_prepareschematicbutton.png")
    
    #load the schematic
    mw.prepareSchematic(False,SCH_FILE)
    mw.ui.remapView.selectRow(3)
    app.processEvents()
    
    ss_schemloaded = mw.grab()
    ss_schemloaded.save("screenshots/schematic_loaded.png")
    
    highlight_widget(ss_schemloaded, mw.ui.writeSchematicButton)
    ss_schemloaded.save("screenshots/mainwindow_commitschematicbutton.png")

if __name__ == "__main__":
    main()
