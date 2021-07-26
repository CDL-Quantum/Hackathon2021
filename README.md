![CDL Quantum Hackathon 2021](CDL_logo.jpg)
# CDL Quantum Hackathon 2021

# Description

The quantum hackathon will be a competition in which teams of the CDL Quantum program participants intensively develop a quantum software project or application over the course of 48 hours. Participants will utilize one of the quantum platforms provided by CDL’s Technical Partners to produce a set of code that implements a quantum algorithm for a chosen application.

The problem a team decides to tackle will be up to the team. To facilitate problem identification, technical partners will present relevant problems (challenges) which we hope will provide inspiration and insight when the teams are deciding what to work on.  

# Purpose

The hackathon has four objectives:

  1. Synthesis and consolidation of knowledge. Participants will have a chance to put what they have learned into practice and contextualize them within a coding environment.

  2. Team dynamics testing. The hackathon will be a first opportunity for co-founders to work directly with their peers and verify whether or not they work well within a given team.

  3. Test business ideas. We hope that many co-founders will take the hackathon as a chance to test out their business ideas and get some early validation.

  4. Opportunities for corporate partners and early pilots. The hackathon represents an excellent engagement opportunity for our corporate partners interested in getting in on the ground floor of quantum computing.

# Format

Prior to the start of the hackathon, participants will have formed teams of 2-4 people, and will have been provided with a list of example projects which they may choose from if they wish.

The hackathon will begin with a presentation introducing the event, and setting rules and expectations. At 10am on Wednesday, July 22th the teams will begin working on their code and be free to do so until 10am on Thursday, July 23th. At this time we will implement a code freeze, meaning that teams will need to upload their code to a repository under MIT License, and we will not accept projects after the deadline.

After lunch and a break, the teams will give short presentations on their projects, which will be judged by a panel (composition to be decided). 

# Team Deliverables and Judging

The teams should strive to create the most complete and streamlined version of their project as is possible within the time allocated. Their performance will be judged on the following primary criteria:

1) Technical difficulty

2) Creativity and originality

3) Usefulness and business potential

4) Presentation quality

# Location: 

The event will take place online. You will be responsible for coordinating meetings and video conferences for your team during the coding component. We recommend that you stay in regular contact throughout the hackathon to support group dynamics in a virtual setting. Presentations will be made using a cohort-wide zoom call.

# Partners 

Participants may use any of the quantum platforms provided by the following technical partners:

- IBM Q

- Xanadu

- D-Wave

- Rigetti

Each technology partner will have dedicated staff member(s) available on the respective partner's slack channel to support you during the project. Given the variety of timezones we will be operating in, please acknowledge that the technical support will not be available for the entire duration of the coding component of the hackathon.

# Prizes

Prizes will be given for 1st, 2nd, and 3rd place, as well as for the choice team from each of the four technical partners. All values in CAD:

1st - $5000

2nd - $2000

3rd - $1000

Partner choices - $1000 each

# Challenges
The following problems were provided by our technical partners. Teams can choose to work on one of the problems or an appropriate generalization thereof.

## IBM Q’s Challenge:

Qiskit Pulse allows you to program real quantum computers at the pulse level. Namely, it provides a language for specifying the microwave control tones (i.e. control of the continuous time dynamics of input signals) that program the quantum state.
In most quantum algorithms/applications, computations are carried out over a 2^n-dimensional Hilbert space spanned by {|0>,|1⟩}^n, where n is the number of qubits. In IBM's quantum hardware, however, there also exists higher energy states which are typically avoided. (e.g. the single qubit "DRAG" pulse helps reduce unintentionally occupation in the |2> state).

In this challenge we want you to use Qiskit Pulse to explore the higher energy states, and put together a unique project which shows how that higher energy state directly benefits or makes your idea possible.
The best application of this idea will be the winner. Preference will be given to projects that:
- Use Qiskit and/or IBM Quantum's devices
- Explain issues faced, problem your team overcame, and future implications of your project
- Show how your project could benefit the quantum computing community
- Delve into why this is important for future research or applications

**Background reading:**
IBM released pulse gates to all users on IBM Quantum systems to attach custom gates defined via their pulse representation, called "calibrations" in Qiskit, to QASM circuits. This allows for a streamlined way to incorporate pulse-level control with the simplicity of QASM circuit construction. A [tutorial](https://qiskit.org/documentation/tutorials/circuits_advanced/05_pulse_gates.html) is available to help you implement this feature into your code.

## Xanadu’s Challenge:

Choose your favourite scientific paper proposing a quantum algorithm that can be run on small-scale devices. Implement it on a simulator using PennyLane or Strawberry Fields. Bonus: implement it also on quantum hardware.

## D-Wave’s Challenge:
Practical applications require domain knowledge and solutions that work at a real-world scale. Hybrid development brings the power of quantum to the scale of classical. Users are challenged to select a practical problem and to solve it at scale with Leap's hybrid solvers (BQM and DQM hybrid solvers). 

As a hint, problems with graph structure like the maximum independent set, structural imbalance, and maximum cut can be translated to a binary quadratic model without additional variables and problems like graph coloring and clustering can be efficiently mapped to the discrete quadratic model. 

Check out https://cloud.dwavesys.com/leap/examples/ for ideas, but use your creativity! The best projects would be the ones that solve the most practical problems.

**Note:** Refer to the Bootcamp training for ideas on how to use the most recent Ocean features.

## Rigetti Challenge:

One of the most exciting applications of quantum computers is Quantum Machine Learning (QML).
Broadly speaking, this refers to the intersection of quantum computing and (classical) machine
learning, and is a growing area of interest among both academic researchers and industry
practitioners. One of the ways in which these two fields come together is by using quantum resources
to process classical data. This has incredibly far-reaching implications in that it may be impactful
for every industry which already leverages some form of data science to drive business decisions
or to increase business value.

For many such QML algorithms, encoding classical data into quantum states is an important step.
An example of this is the amplitude encoding subroutine, which has been implemented for you in
pyQuil. You could use this to implement some QML algorithm, e.g. the one in
https://arxiv.org/abs/1703.10793, or something entirely new and interesting of your own
choosing. The code and jupyter notebook has been provided for amplitude encoding, but feel
free to ask Rigetti Staff for other tips or best practices.

