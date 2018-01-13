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
Created on Fri Jan 12 06:18:23 2018

@author: danw
"""

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {"build_ui" : build_ui}
except ImportError:
    build_ui = None
    cmdclass = {}



from distutils.core import setup

setup(
      name="kicad_backannotate",
      version="0.0.1dev",
      packages=["kicad_backannotate", "kicad_backannotate.gui"],
      scripts=["kicad_backannotate/gui/kicad_backannotate_gui.py"],
      cmdclass = cmdclass
      
      )
