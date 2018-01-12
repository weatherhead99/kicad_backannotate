#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 03:46:34 2018

@author: danw
"""

from kicad_backannotate.board_remap import BoardRemapper, string_remapping, sort_by_x_then_y, sort_by_y_then_x
from kicad_backannotate.schematic_updater import SchematicUpdater, get_remaining

if __name__ == "__main__":
    import sys
    sys.path.append("/home/danw/Software/kicad_dist/lib/python2.7/site-packages")
    
    BOARD_FILE = "/home/danw/Documents/analog_FIR/analog_FIR.kicad_pcb"
    SCH_FILE= "/home/danw/Documents/analog_FIR/analog_FIR.sch"
    SCH_FILE_CB="/home/danw/Documents/analog_FIR/coeffs_buffer.sch"
    
    ba = BoardRemapper(BOARD_FILE)
    
    xtheny = sort_by_x_then_y(ba._boardlocations["R"])
    ythenx = sort_by_y_then_x(ba._boardlocations["R"])
    
    remap = ba.get_remapping(sort_by_y_then_x)
    stremap = string_remapping(remap)
    
    su = SchematicUpdater(SCH_FILE)
    
    
    done = su.recursive_remap(stremap)
    
    leftover = get_remaining(stremap,done)
    
    sheetcounts = su.get_sheet_counts()