![](./fig/opacity_logo.png)

## Project Description 

[comment]: <> (&#40;3-4 lines about what it is and how you did it&#41;)

In our project, we demonstrated how to characterise a three-level quantum system using very limited set of quantum operations.
We calibrated a small set of rotation gates for the single-qubit (now single-qutrit) device, `ibmq_armonk`.
Through the use of simulations, we showed that it was possible to use this set of gates to characterise the quantum state of the device.
A core aspect of our method is shadow state tomography, a relatively new variant of quantum tomography that is capable of extracting device properties from a very limited set of measurements.

## Setup

If users have `make` installed, then they can run the command

`make build-requirements`

Otherwise, users should run

`pip install -r requirements.txt`

`python -m setup develop`

## How to Use

We've presented our work in a series of notebooks. 
The following notebooks represent the most important parts of our project:

1. Calibration of a pulse gates: [ibmq_armonk_calibration.ipynb](./notebooks/ibmq_armonk_calibration.ipynb).

2. Simulating single-qutrit shadow state tomography with pulse gates: [qutrit_simulation.ipynb](./notebooks/Qutrit%20Simulation.ipynb).

3. Implementing and testing pulse gates: [ibmq_armonk_experiments.ipynb](./notebooks/ibmq_armonk_experiment.ipynb).

## Challenge(s) You Solved

- Calibration of multi-'qutrit' devices

    - We initially planned to work with more qutrits. However, it quickly became clear that calibration of a solitary qubit is significantly easier. 
      We got some traction on calibrating a qutrit on `ibmq_bogota` (which has 5 qubits), as shown in [ibmq_bogota_calibration.ipynb](./notebooks/ibmq_bogota_calibration.ipynb). 
      On the other hand, `ibmq_casablanca` still stymied us, as shown in [ibmq_casablanca_calibration.ipynb](./notebooks/ibmq_casablanca_calibration.ipynb). 
    
    - We eventually got the hang of playing with the drive power and frequency to find transitions.
      We found it was much easier designing a frequency sweep for the 1 -> 2 transition by using the calibrated qubit frequency, and the device's default value of anharmonicity.
      It let us avoid doing a broad frequency sweep which often revealed several candidate peaks for the 1 -> 2 transition frequency.


## Project Details: 

- Further walkthrough of what you did

- Business applications

- [Link to Presentation]()

## Contributors 

- Tim Evans ([GitHub](https://github.com/TimEvans), [LinkedIn](https://www.linkedin.com/in/timevans01/))
  
- Tom Smith ([GitHub](https://github.com/ThomasBSmith), [LinkedIn](https://www.linkedin.com/in/thomas-smith-047288198/))
  
- Phil Evans ([GitHub](https://github.com/peva032), [LinkedIn](https://www.linkedin.com/in/philip-evans-407291122/))
  
- Claire Burnett ([LinkedIn](https://www.linkedin.com/in/claireburnett/))