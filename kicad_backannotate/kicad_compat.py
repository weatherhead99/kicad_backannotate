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

import pcbnew
from types import MethodType

class KicadCompatMeta(type):
    def __new__(cls, name, bases, dct):
        print("patching classes for kicad compatibility")

        instance = super(KicadCompatMeta,cls).__new__(cls,name,bases,dct)
        if "pcbnew" in instance._kicad_compat_fixes:
            print("applying pcbnew related compat patches")
            instance._get_libitem = KicadCompatMeta.compat_libitem_func(instance)
         
        return instance

    @staticmethod
    def compat_libitem_func(instance):
        try:
            test_obj = pcbnew.FPID()
        except AttributeError:
            test_obj = pcbnew.LIB_ID()
            
        if not hasattr(test_obj,"GetLibItemName"):
            return MethodType(lambda self,x : x.GetFootprintName(),instance)
        else:
            return MethodType(lambda self,x : x.GetLibItemName(),instance)
