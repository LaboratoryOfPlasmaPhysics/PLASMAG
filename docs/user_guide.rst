User Manual
===========

This manual is intended to help you get started with PLASMAG. Most of
the features are described exhaustively.

How to use the program
======================

The UI
------

The UI is divided into three main sections: the toolbar, the parameter
panel, and the canvas.

.. figure:: docs/images/img.png
   :alt: img.png

   img.png

Toolbar
-------

The toolbar is located at the top of the window and contains the
following buttons:

-  **File:** contains the buttons to open and save files.

   -  .. figure:: docs/images/img_1.png
         :alt: img_1.png

         img_1.png

   -  **Export Parameters:** exports the parameters of to a JSON file,
      can be edited by hand and imported back

   -  **Import Parameters:** imports the parameters from a JSON file,
      must be in the correct format

   -  **Import Flicker Params :** imports the flicker parameters from a
      JSON file, must be in the correct format

   -  **Export Results:** exports the results of the simulation to a csv
      file than can be opened in Excel or any other spreadsheet software

-  **Options:** contains the buttons to change the settings of the
   program.

   -  .. figure:: docs/images/img_2.png
         :alt: img_2.png

         img_2.png

   -  **Change Plot count:** changes the number of plots that are
      displayed in the right panel

Tabs
----

.. figure:: docs/images/img_4.png
   :alt: img_4.png

   img_4.png

It’s used to switch between differents functionalities of the program.

Parameters Section
------------------

.. figure:: docs/images/img_5.png
   :alt: img_5.png

   img_5.png

The parameters section is located on the left side of the window and
contains the parameters of the simulation. All of the parameters are
grouped by category.

How to change a parameter
~~~~~~~~~~~~~~~~~~~~~~~~~

Option 1 : - Click on the line edit field of the parameter you want to
change - Enter the new value - Press Enter - If the value is valid, the
calculation will be triggered. If the value is invalid, the field will
turn red and the calculation will not be triggered.

Option 2: - Click on the line edit field of the parameter you want to
change - Use the sliders to change the value, the value will be updated
in real time and the calculation will be triggered

At every moment, you can reset the value of a parameter by clicking on
the reset button. Or force trigger the calculation by clicking on the
calculate button. |img_6.png| You can use the frequency range double
slider to select the frequency range you want to simulate.

Strategy selection
~~~~~~~~~~~~~~~~~~

.. figure:: docs/images/img_7.png
   :alt: img_7.png

   img_7.png

One of the most importants features of PLASMAG is to be modular and to
allow the user to choose the strategy he wants to use to simulate a
particular value (like the resistance, the capacitance, etc…). You can
easily implement your own strategy by following the instructions in the
`Contributing Guide <contributing.md>`__. If you did everything well,
your strategy will appear in the strategy selection combobox. You can
now select it and it will be used in the simulation.

When you select a strategy if an error occurs, the error message will be
displayed in a popup. It often means that the parameters are not valid
for the selected strategy, or your implementation is not valid and
implicate cyclic dependencies between differents calculations nodes.

Canvas
------

The canvas is located on the right side of the window and contains the
plots of the simulation. You can adjust the number of plots displayed by
clicking on the options button and changing the plot count (from 1 to 5,
default 3)

.. figure:: docs/images/img_9.png
   :alt: img_9.png

   img_9.png

Using the combo box you can chose to display whatever you want in the
plot. The list contains every node that can be calculated in the
program. The graph will be updated in real time when you change the
parameters. The data is linear but plotted in a logarithmic scale, for x
and y axis.

If you want to fit existing data by tunign parameters, you can load a
curve in background by clicking on the load curve button. You can then
select a csv file that contains the curve you want to display. The file
must be in the correct format (frequency, value) and the frequency must
be in Hz.

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
-  Memory is not saved when you close the program.
-  You can clear the memory by clicking on the clear memory button.

.. |img_6.png| image:: docs/images/img_6.png
