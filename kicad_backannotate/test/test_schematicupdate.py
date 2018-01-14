from kicad_backannotate.schematic_updater import SchematicUpdater
from kicad_backannotate.sch import Schematic

import unittest
from pkg_resources import resource_filename
import os

SCH_FILE = resource_filename("kicad_backannotate.test","test_data/backannotate_project/backannotate_project.sch")


class TestSchematicUpdate(unittest.TestCase):
    def setUp(self):
        self._updater = SchematicUpdater(SCH_FILE)
    
    def testFindSymbols(self):
        comp1 = self._updater.find_symbol("C2")
        comp2 = self._updater.find_symbol("C3")
        self.assertNotEqual(comp1, None)
        self.assertNotEqual(comp2, None)
        
    
    def testSingleRemap(self):
        remap = {'C2' :  'C12',  'C3' : 'C13' }
        
        oldsym= self._updater.find_symbol('C2')
        
        oldx = int(oldsym.fields[0]['posx'])
        oldy = int(oldsym.fields[0]['posy'])
        done = self._updater.remap_symbols(remap)
        
        #check the update is reported correctly
        self.assertIn('C2', done)
        self.assertIn('C3', done)
        self.assertEqual(len(done), 2)
        
        #check the new symbol is now in the schematic
        sym = self._updater.find_symbol('C12')
        self.assertNotEqual(sym,  None)
        
        #check the new symbol has the position of the old one
        newx = int(sym.fields[0]['posx'])
        newy = int(sym.fields[0]['posy'])
        
        self.assertEqual(oldx, newx)
        self.assertEqual(oldy, newy)
        
    
    def testSaveData(self):
        remap = {"C2" : "C10"}
        self._updater.remap_symbols(remap)
        
        self._updater.save_changes("_remapped")
        
        basename, ext=  os.path.splitext(SCH_FILE)
        outfname = basename + "_remapped" + ext
        
        #check file was created
        self.assertEqual(os.path.isfile(outfname),  True)
        
        #check "C10" component in the written file
        newschem = Schematic(outfname)
        
        refs = [_.fields[0]["ref"].strip('"') for _ in newschem.components]
        self.assertIn("C10", refs)
        
        #get rid of temporary file
        os.unlink(outfname)
        
        
if __name__ == "__main__":
    unittest.main()
        
        
