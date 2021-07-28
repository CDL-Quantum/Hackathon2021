Fill in this README.md. Example Structure:

## Project Description 

In the following project we apply various Quantum algorithms to weather related image data. Our business proposal is also aligned with developing a quantum weathert application. We have also partially implemented a quantum SVM in Pennylane, but it still needs some work.

## Setup
Example:
1. Make sure you have X installed and configured.

2. Set up your preferred virtual environment.

3. pip install -r requirements.txt

## How to Use
Example:
From command line: Use python solvers/script.py -h

For judges feel free

## Challenge(s) You Solved

Overall Hackathon

Pennylane 

## Project Details: 
  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications: the problem we address is lack of computational capabilities. We research Quantum Machine Learning techniques in the framework of Quantum Image Processing and its potential applications to industries/markets such as weather forecasting, emotion recognition and prediction, nanotechnology etc. Our extensive business proposal can be found here.
## Requirments

After you have activate your environment, before you install anything, make sure
to update your pip with: pip install --upgrade pip

## Installation/plugins with jupyter

`nbstripout` is a great option for clearing the output of the jupyter notebooks.
It can be installed using `pip install nbstripout`. For more info see below in
[before you commit section](#beforecommit)

`nbdime` is a great tool for looking at the git diff for jupyter notebooks.

For jupyterlab there is a market place extension which you need to enable first
and that will let you search and install extensions from within jupyter lab. You
can enable the marketplace extension with the following code:

`jupyter labextension install @jupyter-widgets/jupyterlab-manager`

For jupyter notebook, there is a similar extension but that just gets you all
the extension in one go and lets you enable or disable them from the jupyter
home page toolbar. You can install the extension for the jupyter notebook using:
`pip install jupyter_contrib_nbextensions`

`jupyter contrib nbextension install --user`

## <a name="beforecommit"></a> Before you commit or do a pull request:

Since jupyter is not just a text file and uses JSON format, everytime
code/markdown is changed in jupyter notebook, lot of information about the
layout changes as well. This is especially the case for python code which
outputs pictures/graphs. The pictures are stored as text which show up in the
diff. This complicates the git diff. And hence, the best way to version control
jupyter notebooks is by clearing the output before doing a commit. We have been
using nbstripout for clearing output from notebooks automatically. You can
install nbtripout using `pip install nbstripout`. Please make sure to run
`nbstripout notebook.ipynb` to clear the output in a file. To clear the output
in all the notebooks in a given folder, you can run it on a folder, e.g. the
command `nbstripout Qube/*` clears the output from all the notebooks in `Qube`
folder.

