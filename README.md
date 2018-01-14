#  kicad_backannotator

A back annotation tool for [kicad](http://kicad-pcb.org)

Documentation and tutorial available [here](http://kicad-backannotate.readthedocs.io/en/latest/)

## Disclaimer

This is not in a finished state yet. ** DO NOT USE IT, ESPECIALLY NOT ON PRODUCTION BOARDS. I AM NOT RESPONSIBLE FOR BREAKING YOUR FILES **

## Installation
You require a working installation of PyQt5 and the kicad python bindings for kicad\_backannotate to run. Kicad\_backannotator only works on python 2 (this is a limitation of the kicad python bindings at the moment)

For now, you must install kicad_backannotate from a checked out source.

` git clone git@github.com:weatherhead99/kicad_backannotate.git `

You can install with
`python setup.py install`

or (preferred)

`pip install .`

You can build the documentation (such that it is) using

`python setup.py build_sphinx` 

and find the html documentation in the doc/build/html directory.
