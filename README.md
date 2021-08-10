# Rift Inversion in ASPECT Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Includes current source files (.prm, .py,.sh) used in the ASPECT rift inversion project, as well as lab notebooks (.ipynb) detailing modeling history. Models are currently being run on Stampede2 with ASPECT 9.4.0-pre and dealii 9.3.0. Some functions are imported from the [geoscripts](https://github.com/dyvasey/geoscripts) repository.

The core of the project is the ri_base.prm file, which contains the current standard parameters for ASPECT model runs but also contains blanks for parameters being varied. Parameters are filled in using the ripropagate.generate function, which is run in Jupyter notebooks logging modeling progress. This function also generates a shell script for running the model on Stampede2. Parameters for the temperature structure of the model are generated using the geotherms script, which builds on functions in the [geoscripts](https://github.com/dyvasey/geoscripts) repository. The ripropagate.comp_ascii function produces a composition.txt file used by the prm file to define compositional fields and initial plastic strain values.



