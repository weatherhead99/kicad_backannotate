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

from sch import Schematic, Sheet
import os
from collections import Counter


def splitrefkv(st):
    return st.split('Ref="')[1].strip('"')

def joinrefkv(ref):
    return 'Ref="%s"'%ref

class SchematicUpdater(object):
    
    def __init__(self,sch_file):
        self._sch_file = sch_file
        self._schematic = Schematic(self._sch_file)
        if self._schematic is None:
            raise RuntimeError("couldn't open schematic file")        
        self._sheet_counts = self.get_sheet_counts()
        self._edited_schematics = {}
        self.found_in_schematic = {}
        
    @property
    def edited_schematics(self):
        return self._edited_schematics
            
    def remap_symbols(self,mapping,schematic=None,duplicate=False):        
        if schematic is None:
            schematic = self._schematic
            
        if duplicate and schematic.filename in self._edited_schematics:
            return {}
        
        remapped = {}
        for comp in schematic.components:
            designator = comp.fields[0]["ref"].strip('"')
            if designator in mapping:
                print("remapping: %s -> %s" % (designator,mapping[designator]))
                if designator not in remapped.keys():
                    remapped[designator] = mapping[designator]
                    comp.fields[0]["ref"] = '"%s' % mapping[designator]
                if designator not in self.found_in_schematic:
                    self.found_in_schematic[designator] = schematic.filename
            if len(comp.references) > 0:
                for ref in comp.references:
                    refdesig = splitrefkv(ref["ref"])
                    if refdesig in mapping:
                        if duplicate and refdesig not in remapped.keys():
                            print("remapping %s on duplicate sheet" % refdesig)
                            if refdesig not in remapped.keys():
                                remapped[refdesig] = mapping[designator]
                                ref["ref"] = joinrefkv(mapping[refdesig])
                        else:
                            print("rmapping reference %s" % refdesig)
                            ref["ref"] = joinrefkv(mapping[refdesig])
        self._edited_schematics[schematic.filename] = schematic
        return remapped
            
    def get_sheet_counts(self,sch=None):
        if sch is None:
            sch = self._schematic
        if not isinstance(sch,Schematic):
            raise TypeError("require a Schematic object")
        
        ctr = Counter()
        for sheet in sch.sheets:
            filepath = self.get_sheet_filepath(sheet)
            ctr[filepath] += 1
            subsch = self.load_schematic_for_sheet(sheet)
            ctr.update(self.get_sheet_counts(sch=subsch))
            
        return ctr
        
            
    
    def get_sheet_filepath(self,sheet):
        dirname = os.path.dirname(os.path.abspath(self._sch_file))
        if isinstance(sheet,Sheet):
            fname = os.path.join(dirname,sheet.fields[1]["value"].strip('"'))
        elif isinstance(sheet,str):
            fname = os.path.join(dirname,sheet.strip('"'))
        else:
            raise TypeError("sheet type not understood")
        return fname
    
    def load_schematic_for_sheet(self,sheet):
        fname = self.get_sheet_filepath(sheet)
        print("loading %s" % fname)
        return Schematic(fname)
    
    def recursive_remap(self,mapping,schematic=None,toplevel=True):
        if toplevel:
            self._done_sheets = []
        
        if schematic is None:
            schematic = self._schematic
        elif not isinstance(schematic,Schematic):
            raise TypeError("require Schematic object")
            
        done = self.remap_symbols(mapping,schematic)
        for sheet in schematic.sheets:
            sheetpath = self.get_sheet_filepath(sheet)
            if sheetpath in self._done_sheets:
                continue
            
            duplicate = self._sheet_counts[sheetpath] > 1
            
            schem = self.load_schematic_for_sheet(sheet)
            done.update(self.remap_symbols(mapping,schem,duplicate))
            remaining = get_remaining(mapping,done)
            print("remaining: %d" % len(remaining))
            done.update(self.recursive_remap(remaining,schem))
            self._done_sheets.append(sheetpath)
        
        if toplevel:
            self._done_sheets = []
        
        return done

def get_remaining(remap, done):
    return {k:v for k,v in remap.items() if k not in done.keys()}
