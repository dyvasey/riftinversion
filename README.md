# Rift Inversion in ASPECT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dyvasey/riftinversion/HEAD)

This repository contains code used for modeling 2D rift inversion in ASPECT in support of scientific publications.

## Contents

### Python Modules
There are serveral Python modules (.py) that are designed to be imported and used in other scripts or Jupyter notebooks. These include the following files:

* `ripropagate.py` - functions used for generating `.prm` input files, `composition.txt` files, and `.sh` shell scripts for ASPECT with varied parameters.
* `vtk_plot.py` - functions for plotting 2D model results from ASPECT using [Pyvista](https://github.com/pyvista/pyvista)
* `tchron/tchron.py` - functions for forward modeling AHe and ZHe thermochronology from ASPECT output. 

### Python Scripts
These are `.py` files that use the modules above in support of ASPECT rift inversion models:

* `geotherms.py`  - scripts to generate geothermal gradient values used by `ripropagate.py` to populate `.prm` files, using the [geoscripts](https://github.com/dyvasey/geoscripts]) package.

### Jupyter Notebooks
The `lab_notebooks_archived/` directory contains Jupyter notebooks logging model runs for this project. Note that to actually use these, the notebook needs to be moved to the main repository directory and the repository would need to be reverted to the commit from when the notebook cell was created.

### Base Parameter Files and Shell Scripts
`.prm` files used as a base for model runs are included, with variable parameters indicated by `XXX`. These parameters are propagated using calls to `ripropagate.py` in the Jupyter Notebooks. `.sh` scripts used for model submission on the Stampede2 cluster are also included.

A separate directory `model_files` contains the specific parameter and composition files used for the models presented in publications.


