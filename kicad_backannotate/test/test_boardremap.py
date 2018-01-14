import unittest
from kicad_backannotate.board_remap import BoardRemapper,  sort_by_x_then_y,  string_remapping
import os
import pcbnew
from pkg_resources import resource_filename

BOARD_FILE=resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.kicad_pcb")


class TestBoardRemapper(unittest.TestCase):
    def setUp(self):
        self._remapper = BoardRemapper(BOARD_FILE)
    def test_remap(self):
        remap = self._remapper.get_remapping(sort_by_x_then_y)
        stremap = string_remapping(remap)
        self.assertEqual(stremap["C2"], "C3")
    
    def test_change_board(self):
        remap = self._remapper.get_remapping(sort_by_x_then_y)
        oldpos = self._remapper._board.FindModuleByReference("C2").GetPosition()
        
        self._remapper.change_board_references(remap)
        
        newpos = self._remapper._board.FindModuleByReference("C3").GetPosition()
        self.assertEqual(oldpos, newpos)
        
    def test_save_board(self):
        oldpos = self._remapper._board.FindModuleByReference("C2").GetPosition()
        remap = self._remapper.get_remapping(sort_by_x_then_y)
        self._remapper.change_board_references(remap)
        
        base, ext = os.path.splitext(BOARD_FILE)
        outfile = base+"_remapped" + ext
        self._remapper.save_board(outfile)
        
        board = pcbnew.LoadBoard(outfile)
        mod = board.FindModuleByReference("C3")
        self.assertEqual(oldpos, mod.GetPosition())
        
        os.unlink(outfile)
        
        
if __name__ == "__main__":
    print(BOARD_FILE)
