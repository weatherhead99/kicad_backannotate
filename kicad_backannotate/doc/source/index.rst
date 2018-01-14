.. kicad_backannotate documentation master file, created by
   sphinx-quickstart on Sat Jan 13 23:36:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. index:: Welcome

Welcome to kicad_backannotate
=============================

Kicad_backannotate is a tool which can "back annotate" a PCB design made using the kicad_ EDA tool.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial

.. index:: Introduction

Introduction
============

When an electronic schematic is designed, the component references (e.g R1, R2 etc for resistors) are generally numbered in accordance with being convenient to find in the schematic. It is often useful, instead, to number the references so as  to be easy to find on the final manufactured pcb (i.e. R1 is the resistor at the top left of the pcb). Kicad_backannotate currently includes a simple GUI to manage this process.

Kicad_backannotate is intended to work even on complex, hierarchical schematics.

.. index:: Limitations

Limitations
===========

At present, there are two principle cases of interest not handled by kicad_backannotate:

- Multi-file flat schematics:
  If your schematic contains multiple files, but they are not arranged in a hierarchy (i.e. connections between sheets are made using global labels rather than sub-sheets and hierarchical labels), kicad_backannotate does not automatically handle remapping the schematic.

- Components on multiple layers:
  Kicad_backannotate currently has no options to separately handle re-labelling components on different layers. A board with components on back and front will correctly be re-labelled by kicad_backannotate, but at present all components will be labelled using only their x and y coordinate, with no regard to which layer the component is on. This might largely defeat the purpose of back-annotation.


.. index:: Installation

Installation
============

Kicad_backannotate only runs on python2.7 at the moment, and likely quite a way into the future - this is due to the python bindings of kicad being dependent on wx_python, which only supports python2 (until the bindings are ported to use the new wxPython Phoenix release).

The kicad_backannotate GUI uses PyQt5. You must separately install this on your system before being able to run kicad_backannotate. If you can't do this from your system package manager (e.g. you are on windows or OSX), it might be best to run kicad_backannotate from within a prepackaged python distribution, such as Anaconda_.

You must also have a working installation of the kicad python bindings. You can find information on installing kicad here_.

After having installed the prerequisites, assuming the python2 interpreter is in your path, you can then install kicad_backannotate from the command line:

.. code:: 

   python setup.py install

You can build this documentation using

.. code:: 

   python setup.py build_sphinx

You should then be able to start the GUI using

.. code::

   kicad_backannotate_gui


.. index:: Disclaimer
   
Disclaimer
==========

Kicad_backannotate is in a very early stage of development. At this stage *no guarantees can be made that it will not destroy your valuable project files!*. I am not responsible for loss of your electronic designs. Please always use this tool on a backup of your project for now.

   
Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


.. _kicad: http://www.kicad-pcb.org
.. _Anaconda: https://repo.continuum.io/
.. _here: http://docs.kicad-pcb.org/stable/en/getting_started_in_kicad.html
