#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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
      scripts=["kicad_backannotate/gui/main.py"],
      cmdclass = cmdclass
      
      )