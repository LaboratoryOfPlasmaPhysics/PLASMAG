.. PLASMAG documentation master file, created by
   sphinx-quickstart on Mon Mar 11 17:18:55 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PLASMAG
=======

**(Python Library for Accurate Space Magnetometer Adjustments with
Genetics)**

PLASMAG is a simulation software specifically designed for space
magnetometers. At its core, PLASMAG serves as a comprehensive tool for
the parameters adjustment.

Currently, PLASMAG is tailored to support search coil type instruments.
However, its architecture is built with flexibility and extensibility in
mind. This means PLASMAG is not only limited to current implementations
but is also designed to easily accommodate the addition of new
instruments and the integration of diverse calculation methods and
models.

Table of Contents
-----------------

-  `Quick Setup <#quick-setup>`__
-  `Installation <#installation>`__

   -  `Prerequisites <#prerequisites>`__
   -  `Installing Conda <#installing-conda>`__
   -  `Setting Up the Project <#setting-up-the-project>`__

-  `Usage <#usage>`__
-  `Availables Models <#availables-models>`__
-  `Documentation <#documentation>`__
-  `Contributing <#contributing>`__
-  `License <#license>`__
-  `Acknowledgments <#acknowledgments>`__

Quick Setup
-----------

Clone the repository :

.. code:: bash

   git clone https://github.com/LaboratoryOfPlasmaPhysics/PLASMAG

Usage
-----

1. Simulation Capabilities:

-  Full Electrokinetic Simulation: Uses SPICE kernel via PySPICE for
   comprehensive electrokinetic modeling.
-  (WIP) Real Data Fitting: Incorporates a two-step data fitting tool
   that includes denoising and neural network fitting for accurate
   simulations based on measured data.

2. Visualization Tools:

-  Adaptive Input Section: Adjusts input options based on the
   magnetometer parameter set.
-  Real-time Parameter Variation: Sliders and real-time calculations to
   visualize the impact of parameter changes.
-  Modular Plot Section: Allows up to 5 simultaneous displays of various
   products, providing a comprehensive view of simulation results.

3. Modularity and Flexibility:

-  Strategy Design Pattern: Implements a modular engine design using the
   strategy pattern, allowing dynamic changes in computation methods and
   easy adaptation to new requirements.
-  Parallel Computation: Supports parallelization of computations for
   improved efficiency.
-  Graph Visualization Tools: Provides full graph visualization to
   monitor computation dependencies and processes.

4. Export and Import Capabilities:

-  Export Data: Allows exporting of any product or parameter for
   plotting or later re-importation.

5. Optimization Module (Work in Progress):

-  Genetic Optimization (DEAP): Utilizes evolutionary algorithms to find
   optimal parameter sets.
-  Particle Swarm Optimization: Implements swarm intelligence techniques
   to explore solution spaces.
-  Simulated Annealing: Employs probabilistic techniques to approximate
   global optimization.
-  Mono-parameter and Multi-parameter Optimization: Supports
   optimization for single and multiple parameters.
-  Mono-criteria and Multi-criteria Optimization: Handles single and
   multiple criteria, combining them into a single framework using
   weighted polynomials.

Availables Models
-----------------

At the moment, the PLASMAG simulation model has only one model
implemented: a simple search coil MAGNETOMETER analytic model.

The simulation was validated by comparing the simulation results with
the real data from the JUICE mission.

The parameters for JUICE’s search coil can be found in the
data/JUICE.json file.”

The implemented simulation model performs quite well, demonstrating high
accuracy for low frequency values. This is reflected in the impedance
plot, where the plotted curves all maintain consistent levels and
shapes.

However, challenges arise when extending the analysis to higher
frequency ranges. Specifically, for the NEMI and Closed Loop Transfer
Function (CLTF), the model tends to diverge slightly at high
frequencies. This divergence becomes particularly evident after the
resonance frequency. At this juncture, analytically describing the
‘capacitance’ part of the system grows increasingly difficult, leading
to a slight deviation from expected behaviors. This discrepancy
underlines a current limitation of the model, spotlighting the need for
further refinement and development to enhance its accuracy.

Documentation
-------------

To generate project documentation:

.. code:: bash

   pip install sphinx
   cd docs
   make html

Navigate to docs/_build/html/index.html to view the documentation.

Contributing
------------

The project is open to contributions. Please refer to the
`CONTRIBUTING.md <CONTRIBUTING.md>`__ file for more information.

Acknowledgments
---------------

-  **Maxime RONCERAY** - Developer - LPP/CNRS/X
   `contact-me <mailto:ronceray.maxime@gmail.com>`__
-  **Malik MANSOUR** - Supervisor - LPP/CNRS/X
   malik.mansour@lpp.polytechnique.fr
-  **Claire REVILLET** - IT/Dev supervisor - CNRS Orleans/LPC2E
-  **Guillaume JANNET** - Electronics Engineer - CNRS Orleans/LPC2E


Welcome to PLASMAG's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   controler
   model
   view
   contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

