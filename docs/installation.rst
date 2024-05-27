Installation
============

Prerequisites
~~~~~~~~~~~~~

Ensure you have Conda installed. If not, follow the instructions here:
https://conda.io/projects/conda/en/latest/user-guide/install/index.html

Linux conda installation
~~~~~~~~~~~~~~~~~~~~~~~~

Linux Conda Installation

Install Conda using the following commands:

.. code:: bash

   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm -rf ~/miniconda3/miniconda.sh

Add conda to your PATH

.. code:: bash

   ~/miniconda3/bin/conda init bash
   ~/miniconda3/bin/conda init zsh

Restart your terminal and verify the Conda installation:

.. code:: bash

   conda --version

Setting Up the Project
~~~~~~~~~~~~~~~~~~~~~~

Create and activate a new Conda environment:

.. code:: bash

   conda env create -f environment.yml

Activate the environment

.. code:: bash

   conda activate PLASMAG

Run the application

.. code:: bash

   python PLASMAG.py