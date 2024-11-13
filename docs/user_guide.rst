User Guide
==========
This manual is intended to help you get started with PLASMAG. Most of
the features are described exhaustively.

Installation
------------

We recommend to use a Python virtual environment to run PLASMAG. In the following explanation, we
will use Conda [#condaWebsite]_ to prepare the environment. If you don't have it already, please
refer to this page to install it:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html

Getting PLASMAG
^^^^^^^^^^^^^^^

PLASMAG's repository is reachable at: https://github.com/LaboratoryOfPlasmaPhysics/PLASMAG

To use it you can either download a tagged version or clone the most recent state of the master
branch.

Installing prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^

1. Open a terminal (or an Anaconda PowerShell prompt under Windows)
2. Go to the main folder of PLASMAG
3. Execute the following command to create a virtual environment with all needed prerequisites:

.. code:: bash

   conda env create -f user_environment.yml

4. Activate the environment

.. code:: bash

   conda activate PLASMAG

5. [Windows only] If you're running Windows, you need to copy manually a library where Python will
   search for it. For that the first step is to identify the path of your virtual environment:

   .. code:: bash

      where python

   Let's name <path_of_your_environment> the answer, to which you remove "python.exe".
   Then copy the file "ngspice.dll" from <path_of_your_environment>/bin/ to
   <path_of_your_environment>/lib/Site_packages/PySpice/Spice/NgSpice/Spice64_dll/dll-vs/
   (the two last folders has to by created before)

6. Run the application

.. code:: bash

   python PLASMAG.py

Whenever you open a new terminal (or an Anaconda PowerShell prompt), you will need to do the
activation (*conda activate PLASMAG*) step before running the application.



.. rubric:: Footnotes

.. [#condaWebsite] https://conda.io/projects/conda/en/latest/user-guide/index.html

Global presentation of the User Interface
-----------------------------------------

The UI is divided into three main sections: the menubar, the parameter
panel, and the canvas.

.. figure:: images/img.png

Menubar
^^^^^^^

The menubar is located at the top of the window and contains the
following menus:

.. figure:: images/img_2.png

- **File:** this menu gives access to import and export features
  (see the *Feature* section below for more details)
- **Options:** this menu gives access to the parametrisation of the number of plots in
  the Canva area
- **Help:** this menu gives access to the documentation and to some representation of the way the
  different physical quantities are related (nodes dependencies)


Tabs
^^^^

.. figure:: images/img_4.png

It’s used to switch between different functionalities of the program.

Parameters Section
~~~~~~~~~~~~~~~~~~

.. figure:: images/img_5.png

The parameters section is located on the left side of the window and
contains the parameters of the simulation. All of the parameters are
grouped by category.

How to change a parameter
"""""""""""""""""""""""""

Option 1:

- Click on the line edit field of the parameter you want to change
- Enter the new value
- Press Enter
- If the value is valid, the calculation will be triggered. If the value is invalid, the field
  will turn red and the calculation will not be triggered.

Option 2:

- Click on the line edit field of the parameter you want to change
- Use the sliders to change the value, the value will be updated in real time and the calculation
  will be triggered

.. figure:: images/img_6.png

At every moment, you can reset the value of a parameter by clicking on
the reset button. Or force trigger the calculation by clicking on the
calculate button. You can use the frequency range double slider to select
the frequency range you want to simulate.

Strategy selection
~~~~~~~~~~~~~~~~~~

.. figure:: images/img_7.png

One of the most importants features of PLASMAG is to be modular and to
allow the user to choose the strategy he wants to use to simulate a
particular value (like the resistance, the capacitance, etc…). You can
easily implement your own strategy by following the instructions in the
:ref:`contributing new code` section. If you did everything well,
your strategy will appear in the strategy selection combobox. You can
now select it and it will be used in the simulation.

When you select a strategy if an error occurs, the error message will be
displayed in a popup. It often means that the parameters are not valid
for the selected strategy, or your implementation is not valid and
implicate cyclic dependencies between differents calculations nodes.

Canvas
^^^^^^

The canvas is located on the right side of the window and contains the
plots of the simulation. You can adjust the number of plots displayed by
clicking on the options button and changing the plot count (from 1 to 5,
default 3)

.. figure:: images/img_9.png

Using the combo box you can chose to display whatever you want in the
plot. The list contains every node that can be calculated in the
program. The graph will be updated in real time when you change the
parameters. The data is linear but plotted in a logarithmic scale, for x
and y axis.

If you want to fit existing data by tuning parameters, you can load a
curve in background by clicking on the load curve button. You can then
select a csv file that contains the curve you want to display. The file
must be composed of 2 columns (frequencies and values) separated by commas,
and the frequency must be in Hz.

Memory
~~~~~~

-  As PLASMAG is a tuning tool, it’s important to be able to compare the
   results of different simulations. To do so, you can save the results
   of a simulation by clicking on one of the save button (1,2,3). The
   results/parameters will be saved in memory and you can load them back
   by clicking on the load button.
-  When data are stored in memory, the save button will turn green.
-  You can “reset” parameters to the saved state by clicking again on a
   green save button.
-  Memory is not saved when you close the program (please use the
   *Export Parameters* feature for a more permanent saving).
-  You can clear the memory by clicking on the clear memory button.


Features
--------

Analytical model
^^^^^^^^^^^^^^^^

Resistance (R) Node
~~~~~~~~~~~~~~~~~~~
The resistance node proposes 2 analytical strategies:

.. autoclass:: src.model.strategies.strategy_lib.resistance.AnalyticalResistanceStrategy

.. autoclass:: src.model.strategies.strategy_lib.resistance.MultiLayerResistanceStrategy

Magnetometric demagnetizing factor (:math:`N_z`) Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The magnetometric demagnetizing factor node proposes 2 analytical strategies:

.. autoclass:: src.model.strategies.strategy_lib.Nz.AnalyticalNzStrategy

.. autoclass:: src.model.strategies.strategy_lib.Nz.AnalyticalNzDiaboloStrategy

Effective permeability (:math:`\mu_{app}`) Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The effective permeability node proposes 2 analytical strategies:

.. autoclass:: src.model.strategies.strategy_lib.mu_app.AnalyticalMu_appStrategy

.. autoclass:: src.model.strategies.strategy_lib.mu_app.AnalyticalMu_appDiaboloStrategy

Lambda coefficient factor (:math:`\lambda`) Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The lambda coefficient factor node proposes 2 analytical strategies:

.. autoclass:: src.model.strategies.strategy_lib.lambda_strategy.LukoschusAnalyticalLambdaStrategy

.. autoclass:: src.model.strategies.strategy_lib.lambda_strategy.ClercAnalyticalLambdaStrategy

Inductance (L) Node
~~~~~~~~~~~~~~~~~~~
The inductance is computed as follow:

.. autoclass:: src.model.strategies.strategy_lib.inductance.AnalyticalInductanceStrategy

Capacitance (C) Node
~~~~~~~~~~~~~~~~~~~~
The capacitance is computed as follow:

.. autoclass:: src.model.strategies.strategy_lib.capacitance.AnalyticalCapacitanceStrategy

Impedance (Z) Node
~~~~~~~~~~~~~~~~~~
The impedance is computed as follow:

.. autoclass:: src.model.strategies.strategy_lib.impedance.AnalyticalImpedanceStrategy

ASIC's transfer function (:math:`H`, :math:`H_1` and :math:`H_2`) Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ASIC transfer function is the product of both stage's transfer function.
Here are the strategies for each stage and for the whole ASIC.

.. autoclass:: src.model.strategies.strategy_lib.TF_ASIC.TF_ASIC_Stage_1_Strategy_linear

.. autoclass:: src.model.strategies.strategy_lib.TF_ASIC.TF_ASIC_Stage_2_Strategy_linear

.. autoclass:: src.model.strategies.strategy_lib.TF_ASIC.TF_ASIC_Strategy_linear

Open Loop Transfer Function (OLTF)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This strategy returns 2 transfer functions: the first one "OLTF" is not impacted by the ASIC's 2nd
stage, the second "OLTF_filtered" is filtered by the ASIC's 2nd stage.
Both are plotted together on the "OLTF" plot.

.. autoclass:: src.model.strategies.strategy_lib.OLTF.OLTF_Strategy

Closed Loop Transfer Function (CLTF)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This strategy returns 2 transfer functions: the first one "CLTF" is not impacted by the ASIC's 2nd
stage, the second "CLTF_filtered" is filtered by the ASIC's 2nd stage.
Both are plotted together on the "CLTF" plot.

.. autoclass:: src.model.strategies.strategy_lib.CLTF.CLTF_Strategy

Noises Spectral Densities
~~~~~~~~~~~~~~~~~~~~~~~~~

The spectral densities here are all computed in :math:`\frac{V}{\sqrt{Hz}}` and called *Noise
Spectral Densities*. They are plotted together in the "Display_all_PSD" plot (still as Noise
Spectral Densities)

They can be rendered in :math:`\frac{V^2}{Hz}` (real Power Spectral Density) by using
"Display_all_PSD_strategy" in the *Strategy Selection* tab.

Except for the Flicker noise spectral density, all the spectral density strategies return 2
quantities: the first one "NSD_XX" is not impacted by the ASIC's 2nd
stage, the second "NSD_XX_filtered" is filtered by the ASIC's 2nd stage.
Both are plotted together on the "NSD_XX" plot.

The "NSD_filtered_Total" is the quadratic sum of the filtered NSD_XX.

All the filtered spectral densities are plotted together on the "Display_all_PSD_filtered" while
all the non-filtered are plotted together on the "Display_all_PSD"


.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_R_cr

.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_R_Coil

.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_Flicker

.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_e_en

.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_e_in

.. autoclass:: src.model.strategies.strategy_lib.Noise.NSD_Total

SPICE
^^^^^

Parameters export and import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Through the *File* menu in the menubar, you can export or import parameters and data.

.. figure:: images/img_1.png

The JSON format has been chosen to allow both user and computer to read and write the parameters files
easily.
The available features are:

   - **Export Parameters:** exports the whole set of current parameters of to a JSON file.

   - **Import Parameters:** imports the parameters from a JSON file (same structure as exported
     files). If some parameters are missing from your file, they will be taken in *default.json*

   - **Import Flicker Params:** imports the flicker parameters from a JSON file formatted like this::

         {
             "Para_A": 615.0,
             "Para_B": 34.0,
             "Alpha": 7.0,
             "e_en": 3.0,
             "e_in": 106.0
         }

     Be careful that your values are inside the limits defined by the last file loaded through
     *Import Parameters* or those defined in *default.json*.

   - **Export Results:** exports the results of the simulation to a CSV file. Each physical quantity
     values are stored in a column, whether it depends on the frequency or not.

   - **Export CLTF NEMI:** export CLTF and NEMI curves as a plot file.


Dependency tree visualisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Through the *Help* menu of the menubar, you access different representation of the model nodes
(please see the section "Notion of Model" for more explanation) that may help you understand the
dependencies. Two main ways to represent the nodes are available:

   - the **Export Dependency Tree** feature generates a JSON file containing the node
     dependency tree

   - the **Display XX Graph** features generates dynamic graphical representation in HTML format.
     Open the generated file to visualise the node tree. There are 3 types of graph:

      - the *dependency* tree help to see the computation dependencies;
      - the *community* tree groups the nodes that work together;
      - the *degree* tree help identifying the nodes far from the leaf nodes.


Notion of "Model"
-----------------

At its beginning PLASMAG was built to be a numerical representation of a Search-Coil Magnetometer
(SCM) based on a fixed amount of equations. This was one numerical "model" of an SCM.

Then we tried to have a representation of another type de SCM, with a different core shape and a
different way to wind the copper wire around it. For this we added new nodes and new strategies to
already existing nodes, and potentially removed some strategies. This was a second numerical "model"
of an SCM.

A "model" in PLASMAG is a consistent set of nodes (holding physical values) --working on
equations, abacus, optimisation, IA, or whatever-- that represents a physical sensor.

Whether you want to simulate an SCM, another type of magnetometer or something else, you'll find
everything you need to build your own "model" for your sensor in the contribution guide.
