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



'''
Documentation, License etc.

@package kicad_backannotate
'''


import pcbnew
import re


class BoardRemapper(object):
    def __init__(self,boardfile=None):  
        
        if boardfile is None:
            self._board = pcbnew.GetBoard()
            if self._board is None:
                raise RuntimeError("couldn't get pcbnew board. Perhaps it is not running?")
        else:
            self._board = pcbnew.LoadBoard(boardfile)
        self._load_original_board_geometry(lambda m : m.GetCenter())
    
    def _load_original_board_geometry(self,locfun):
        self._boardlocations = {}
        self._boardtstamps = {}
        self._boardlibnames = {}
        modtypes = set([])
        modules = self._board.GetModules()
        for mod in modules:
            centre = locfun(mod)
            tstamp = mod.GetTimeStamp()
            libitem = mod.GetFPID().GetLibItemName()
            modtype, modnumber = _parse_reference(mod.GetReference())
            if modtype is not None:
                modtypes.add(modtype)
                if modtype not in self._boardlocations:
                    self._boardlocations[modtype] = {}
                    self._boardtstamps[modtype] = {}
                    self._boardlibnames[modtype] = {}
                self._boardlocations[modtype][modnumber] = centre[0],centre[1]
                self._boardtstamps[modtype][modnumber] = tstamp
                self._boardlibnames[modtype][modnumber]= libitem

    def get_remapping(self,sortfun):
        mapping = {}
        for modtype,modules in self._boardlocations.items():            
            geomsort = sortfun(modules)
            numsort = sorted(geomsort)
            mapping[modtype] = {_ : __ for _, __ in zip(geomsort,numsort)}
        
        return mapping
    
    def get_location(self,designator):
        if isinstance(designator,unicode):
            mt,mn = _parse_reference(designator)
            return self._boardlocations[mt][mn]
        else:
            raise TypeError("require unicode not %s" % type(designator)) 
            
    def get_tstamp(self,designator):
        if isinstance(designator,unicode):
            mt,mn = _parse_reference(designator)
            return self._boardtstamps[mt][mn]
        else:
            raise TypeError("require unicode not %s" % type(designator)) 
    
    def get_libitem(self,designator):
        if isinstance(designator,unicode):
            mt,mn = _parse_reference(designator)
            return self._boardlibnames[mt][mn]
        else:
            raise TypeError("require unicode not %s" % type(designator))
            
    def change_board_references(self,mapping):
        for modtype in mapping:
            for oldnum,newnum in mapping[modtype].items():
                print(_reference_to_str(modtype,oldnum))
                print(_reference_to_str(modtype,newnum))
                boardmod = self._board.FindModule(_reference_to_str(modtype,int(oldnum)))
                boardmod.SetReference(_reference_to_str(modtype,int(newnum)))
                boardmod.SetModified()
    
    def save_board(self,fname):
        self._board.Save(fname)
    
    
    
def sorted_string_remapping(mapping):
    out_old = []
    out_new = []
    
    for modtype in sorted(mapping.keys()):
        modmap = mapping[modtype]
        out_old.extend(_reference_to_str(modtype,_) for _ in modmap.keys())
        out_new.extend(_reference_to_str(modtype,_) for _ in modmap.values())
    
    return out_old, out_new
    
def string_remapping(mapping):
    out = {}
    for modtype, modulemapping in mapping.items():
        dct = {_reference_to_str(modtype,_) : _reference_to_str(modtype,__)
            for _, __ in modulemapping.items()}
        out.update(dct)
    return out
        
modmatch = re.compile("([a-zA-Z]*)([0-9]*)")
            
def _parse_reference(reference):
    tp,num = modmatch.match(reference).groups()
    if len(tp) == 0 or len(num) == 0:
        return None,None
    return tp,int(num)

def _reference_to_str(tp,num):
    return "%s%d" %(tp,num)


def getx(module_locations):
    def f(a):
        return module_locations[a][0]
    return f

def gety(module_locations):
    def f(a):
        return module_locations[a][1]
    return f

def sort_by_y_then_x(locs):
    return sorted(sorted(locs.keys(),key=getx(locs)),key=gety(locs))

def sort_by_x_then_y(locs):
    return sorted(sorted(locs.keys(),key=gety(locs)),key=getx(locs))


if __name__ == "__main__":
    import sys
    sys.path.append("/home/danw/Software/kicad_dist/lib/python2.7/site-packages")
    
    BOARD_FILE = "/home/danw/Documents/analog_FIR/analog_FIR.kicad_pcb"
    SCH_FILE= "/home/danw/Documents/analog_FIR/analog_FIR.sch"
    ba = BoardRemapper(SCH_FILE,BOARD_FILE)
    
    xtheny = sort_by_x_then_y(ba._boardlocations["R"])
    ythenx = sort_by_y_then_x(ba._boardlocations["R"])
    
    remap = ba.get_remapping(sort_by_y_then_x)
    stremap = string_remapping(remap)