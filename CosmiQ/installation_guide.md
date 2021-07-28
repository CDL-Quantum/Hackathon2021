## Setup
In order to facilitate online collaboration, the CosmiQ team used [mybinder.org](https://mybinder.readthedocs.io/en/latest/introduction.html) free online service. See [binder/README](binder/README.md) file for more details.

For local installations, please follow the instructions below.

1. Make sure you have python 3.8+, pip and JupyterLab installed and configured.
2. Set up your preferred virtual environment, e.g.:
```
python3 -m venv cdl
source cdl/bin/activate
```
3. Configure two conda environments to install vendor specific dependencies, e.g.:
```
conda create -n CDLQ_IBMQ python=3
conda create -n CDLQ_XANADU python=3
```
4. Activate corresponding environment and load vendor specific dependencies before starting `jupyter notebook` in each of the subfolders:


   - *__IBMQ__*

   To run the Jupyter notebooks in the [ibmq](ibmq) folder, activate CDLQ_IBMQ environment and the corresponding jupyter kernel, then install dependencies:
   ```
   conda activate CDLQ_IBMQ
   ipython kernel install --name CDLQ_IBMQ --user
   pip install -r ibmq/requirements.txt
   ```

   - *__XANADU__*

   To run the Jupyter notebooks in the [xanadu](xanadu) folder, activate CDLQ_XANADU environment and the corresponding jupyter kernel, then install dependencies:
   ```
   conda activate CDLQ_XANADU
   ipython kernel install --name CDLQ_XANADU --user
   pip install -r xanadu/requirements.txt
   
   ```
