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
        modtypes = set([])
        modules = self._board.GetModules()
        for mod in modules:
            centre = locfun(mod)
            modtype, modnumber = _parse_reference(mod.GetReference())
            if modtype is not None:
                modtypes.add(modtype)
                if modtype not in self._boardlocations:
                    self._boardlocations[modtype] = {}
                self._boardlocations[modtype][modnumber] = centre[0],centre[1]

    def get_remapping(self,sortfun):
        mapping = {}
        for modtype,modules in self._boardlocations.items():            
            geomsort = sortfun(modules)
            numsort = sorted(geomsort)
            mapping[modtype] = {_ : __ for _, __ in zip(geomsort,numsort)}
        
        return mapping
            
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