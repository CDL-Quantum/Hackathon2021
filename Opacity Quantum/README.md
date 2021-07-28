![](./fig/opacity_logo.png)

## Project Description 

IBM Quantum invited teams to take their beautiful qubits and use OpenPulse to purposely occupy higher-energy excited states.

We set out to achieve the following goals:
- Implement a characterisation method for qutrits that:
    - is efficient (because quantum systems are big and we just made them bigger!), and
    - has broader significance in the community (academic *and* commercial).
- Demonstrate the controls needed to perform this characterisation on a transmon qutrit.
- Challenge ourselves to explore a characterisation method that hasn't been implemented in Qiskit's Ignis library already.

In answer to these goals, we decided we would try to implement shadow state tomography, a relatively new variant of quantum tomography that is capable of extracting device properties from a very limited set of measurements.
Furthermore, we wanted to find out how to do this **on qutrits**.
We split the tasks into hardware and software components.

**Hardware**

At a minimum, we wanted to implement the necessary constituent controls for shadow tomography.
We demonstrated how to characterise a three-level quantum system using very limited set of quantum operations.
We calibrated a small set of rotation gates for the single-qubit (now single-qutrit) device, `ibmq_armonk`, which is all we would need
to perform the shadow tomography measurements.

**Software**

Through the use of simulations, we showed that it was possible to use this set of gates to characterise the quantum state of the device.
We explored the utility of shadow tomography for qutrit states and predicting properties of multi-qutrit states. 
In particular, measuring an entanglement witness for a 3-qutrit GHZ state.

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

2. Implementing and testing pulse gates: [ibmq_armonk_experiments.ipynb](./notebooks/ibmq_armonk_experiment.ipynb).

3. Simulating single- and multi-qutrit shadow state tomography with pulse gates: [qutrit_simulation.ipynb](./notebooks/qutrit_simulation.ipynb).

## Challenge(s) You Solved

- Calibration of multi-'qutrit' devices

    - We initially planned to work with more qutrits. However, it quickly became clear that calibration of a solitary qubit is significantly easier. 
      We got some traction on calibrating a qutrit on `ibmq_bogota` (which has 5 qubits), as shown in [ibmq_bogota_calibration.ipynb](./notebooks/ibmq_bogota_calibration.ipynb). 
      On the other hand, `ibmq_casablanca` still stymied us, as shown in [ibmq_casablanca_calibration.ipynb](./notebooks/ibmq_casablanca_calibration.ipynb). 
    
    - We eventually got the hang of playing with the drive power and frequency to find transitions.
      We found it was much easier designing a frequency sweep for the 1 -> 2 transition by using the calibrated qubit frequency, and the device's default value of anharmonicity.
      It let us avoid doing a broad frequency sweep which often revealed several candidate peaks for the 1 -> 2 transition frequency.

## [Link to Presentation]()

## Contributors 

- Tim Evans ([GitHub](https://github.com/TimEvans), [LinkedIn](https://www.linkedin.com/in/timevans01/))
  
- Tom Smith ([GitHub](https://github.com/ThomasBSmith), [LinkedIn](https://www.linkedin.com/in/thomas-smith-047288198/))
  
- Phil Evans ([GitHub](https://github.com/peva032), [LinkedIn](https://www.linkedin.com/in/philip-evans-407291122/))
  
- Claire Burnett ([LinkedIn](https://www.linkedin.com/in/claireburnett/))