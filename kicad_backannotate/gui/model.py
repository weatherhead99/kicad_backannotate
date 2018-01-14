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
Created on Fri Jan 12 07:30:24 2018

@author: danw
"""



from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QModelIndex
from PyQt5.QtWidgets import QStyle

import sys
sys.path.append("/home/danw/Software/kicad_backannotate/")

import pcbnew
print("pcbnew: %s" % pcbnew.__file__)

from kicad_backannotate.board_remap import BoardRemapper,sort_by_x_then_y, sorted_string_remapping, sort_by_y_then_x, string_remapping


class RemapTable(QAbstractTableModel):
    def __init__(self,board_file,sortindex,style=None):
        super(RemapTable,self).__init__()
        self._remapper = BoardRemapper(boardfile=board_file)
        self.resortdata(sortindex)
        self._style = style
        
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
        return Qt.ItemFlags(128 |32 | 1)
        
        
    def headerData(self,section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return QVariant("old reference")
            elif section == 1:
                return QVariant("new reference")
            elif section == 2:
                if hasattr(self,"_donemap"):
                    return QVariant("found in schematic")
        
        elif orientation == Qt.Vertical:
            return None
        
    def rowCount(self,parent):
        return len(self._oldvals)
    
    def columnCount(self,parent):
        if not hasattr(self,"_donemap"):
            return 2
        else:
            return 3
    
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._oldvals[index.row()]
            elif index.column() == 1:
                return self._newvals[index.row()]
            elif index.column() == 2:                
                return None
            raise IndexError("invalid index supplied")
        elif role == Qt.CheckStateRole:
            if self._style is not None:
                return None
            if index.column() == 2:
                if self._oldvals[index.row()] in self._donemap:
                    return 2
                return 0
            else:
                return None
        elif role == Qt.DecorationRole:
            if self._style is None:
                return None
            if index.column() == 2:
                if self._oldvals[index.row()] in self._donemap:
                    return self._style.standardIcon(QStyle.SP_DialogApplyButton)
                else:
                    return self._style.standardIcon(QStyle.SP_DialogCancelButton)
        else:
            return None
        
    def showSchematicStatus(self,remap, done):
        if self.columnCount(None) == 2:
            self.beginInsertColumns(QModelIndex(),2,2)
            self._donemap = done
            self.endInsertColumns()
            
        else:
            self.beginResetModel()
            self._donemap = done
            self.endResetModel()
            
    
    def getProperties(self,index):
        oldval = self._oldvals[index.row()]
        x,y = self._remapper.get_location(oldval)
        tstamp = self._remapper.get_tstamp(oldval)
        libid = self._remapper.get_libitem(oldval)
        
        props = {"x" : x, "y" : y, "tstamp" : tstamp,
                 "libid" : libid}
        
        return props

    def sort(self,column,sortorder):

        if column == 0:
            self.beginResetModel()
            self._oldvals = sorted(self._oldvals)
            if sortorder == Qt.DescendingOrder:
                self._oldvals = self._oldvals[::-1]
            stremap = string_remapping(self.remap)
            self._newvals = [stremap[_] for _ in self._oldvals]
            self.endResetModel()

        elif column == 1:
            self.beginResetModel()
            self._newvals = sorted(self._newvals)
            if sortorder == Qt.DescendingOrder:
                self._newvals = self._newvals[::-1]
            stremap = {v:k for k,v in string_remapping(self.remap).items()}
            self._oldvals = [stremap[_] for _ in self._newvals]
