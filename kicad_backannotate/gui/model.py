#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 07:30:24 2018

@author: danw
"""

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt


import sys
sys.path.append("/home/danw/Software/kicad_backannotate/")

import pcbnew
print("pcbnew: %s" % pcbnew.__file__)

from kicad_backannotate.board_remap import BoardRemapper,sort_by_x_then_y, sorted_string_remapping, sort_by_y_then_x


class RemapTable(QAbstractTableModel):
    def __init__(self,board_file,sortindex):
        super(RemapTable,self).__init__()
        self._remapper = BoardRemapper(boardfile=board_file)
        self.resortdata(sortindex)
        
        
    def resortdata(self,sortindex):
        self.beginResetModel()
        if sortindex == 0 :
            sortfun = sort_by_x_then_y
        else:
            sortfun = sort_by_y_then_x
        self.remap = self._remapper.get_remapping(sortfun)
        self._oldvals, self._newvals = sorted_string_remapping(self.remap)
        self.endResetModel()

        
    def flags(self,index):
        return Qt.ItemFlags(32 | 1)

        
    def headerData(self,section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return QVariant("old reference")
            elif section == 1:
                return QVariant("new reference")
        elif orientation == Qt.Vertical:
            return None
        
    def rowCount(self,parent):
        return len(self._oldvals)
    
    def columnCount(self,parent):
        return 2
    
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._oldvals[index.row()]
            elif index.column() == 1:
                return self._newvals[index.row()]
            
            raise IndexError("invalid index supplied")
        else:
            return None