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



from setuptools import setup, find_packages, Command

import os
from kicad_backannotate.doc.generate_screenshots import main

name="kicad_backannotate"
version="0.0.1dev1"
release="0.0.1dev1"


class ScreenshotsCommand(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print("building screenshots...")
        curdir = os.path.abspath(os.curdir)
        os.chdir("kicad_backannotate/doc")
        main()
        os.chdir(curdir)
    


setup(
      name=name,
      version=version,
      packages=find_packages(exclude=["test","doc"]),
      license = "GPL-3.0-or-later", 
      url= "https://github.com/weatherhead99/kicad_backannotate", 
      author="Dan Weatherill", 
      author_email="plasteredparrot@gmail.com", 
      entry_points={
            "gui_scripts": [ 
            "kicad_backannotate_gui = kicad_backannotate.gui.kicad_backannotate_gui:main"]},
      cmdclass = {"screenshots" : ScreenshotsCommand},
        test_suite="kicad_backannotate.test", 
        package_data = { "kicad_backannotate.test_data" : ["example_projects/backannotate_project/backannotate_project.kicad_pcb"]
        },
      )
