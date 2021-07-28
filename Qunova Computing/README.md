Fill in this README.md. Example Structure:

## Project Description 
(3-4 lines about what it is and how you did it)

## Setup
0. For all file path written in this project, the root directory is `/Qunova Computing/`.

1. Make sure you have [QVM](https://pyquil-docs.rigetti.com/en/v3.0.0/start.html#downloading-the-qvm-and-compiler) installed and configured.

   (Linux) If you counter a trouble that the system can't find `libffi.so.6` when calling `qvm --version` , refer to [here](https://stackoverflow.com/questions/61875869/ubuntu-20-04-upgrade-python-missing-libffi-so-6)
   
2. To use Rigetti QPU, you need to install [QCS-CLI](https://docs.rigetti.com/qcs/guides/using-the-qcs-cli#installation) as well.
3. Set up your preferred virtual environment.

4. `pip install -r requirements.txt`

## How to Use
### 1. Rigetti Challenge
1. Run Jupyter Notebook Server
2. Open two terminals and run `qvm -S` and `quilc -S` for each terminal.
3. **(Data Preprocessing)** Run the [notebook file](./covid19_data/covid19.ipynb) for the preprocessing.
4. **(Training)** Run the [python script file](./training_pyquil.py) for the training by `python ./traiing_pyquil.py`.

   - You can monitor the training process running `tensorboard --logdir=./runs/zzzpfm_c12v3_zzzpfm_c12v3_pyquil`.
5. **(Testing)** Run the [notebook file](test.ipynb) to test the trained model.
6. **(QPU Testing)** Run the [notebook file](./zzzpfm_c12_pyquil_test_only_qpu.ipynb) to test the trained model on Aspen-9.

## Challenge(s) You Solved
### 1. Rigetti Challenge

## Project Details: 
### 1. Rigetti Challenge
1. 

  - Further walkthrough of what you did 
  - Links to any Jupyter notebooks/scripts
  - Business applications
  - Link to Presentation

## Contributors 
