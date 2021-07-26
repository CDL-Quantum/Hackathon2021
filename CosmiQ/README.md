# CDL_Quantum_Hackathon_2021
Collaboration repository for CDL bootcamp Quantum Hackathon 2021.

This branch contains environment for IBM's [qiskit](https://qiskit.org/).

This project uses [mybinder.org](https://mybinder.readthedocs.io/en/latest/introduction.html) online service.

To run it, open the following [link](https://mybinder.org/v2/gh/olegxtend/CDL_Quantum_Hackathon_2021/ibmq) in your browser. It may take a couple minutes to launch.

## Note 1
When you launch mybinder, it creates a snapshot of the repo from the latest versions of the code and it doesn't automatically merge the code from GIT. If you need to refresh the code, just close your session and open a new one by launching the above link.

## Note 2
Mybinder session expires after 20 minutes of inactivity. Make sure you save your work (download your files to a local disk) if you are not using it.  

You can find a quick tutorial [here](https://the-turing-way.netlify.app/reproducible-research/renv/renv-binder.html)

## Dependencies

The environment configuration files can be found under the [/binder](./binder) folder.

The ```requirements.txt``` file is auto-generated using ```pip-compile``` which reads the ```requirements.in``` file in the same folder. You can either update it manually or regenerate by adding/modifying dependencies in the ```requirements.in``` file. The latter is preferred as it validates versions compatibility. Here are the steps:

1. Install pip-tools in your local environment:
```
python -m pip install pip-tools
```
2. Cd to a folder on your local drive where you have the ```requirements.in``` file and run the command:
```
pip-compile
```
3. Commit and push the generated ```requirements.txt``` file to the GIT repo.
4. Re-launch the project in [mybinder.org](https://mybinder.org/v2/gh/olegxtend/CDL_Quantum_Hackathon_2021/ibmq)

# CDL Readme for reference

Fill in this README.md. Example Structure:

## Project Description
(3-4 lines about what it is and how you did it)

## Setup
Example:
1. Make sure you have X installed and configured.

2. Set up your preferred virtual environment.

3. pip install -r requirements.txt

## How to Use
Example:
From command line: Use python solvers/script.py -h

## Challenge(s) You Solved

## Project Details:
  - Further walkthrough of what you did
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

## Contributors
