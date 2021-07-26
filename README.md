<<<<<<< HEAD
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

- D-Wave

- Xanadu

- IBM Q

- Rigetti

Each technology partner will have dedicated staff member(s) available on the respective partner's slack channel to support you during the project. Given the variety of timezones we will be operating in, please acknowledge that the technical support will not be available for the entire duration of the coding component of the hackathon.

# Prizes

Prizes will be given for 1st, 2nd, and 3rd place, as well as for the choice team from each of the four technical partners. All values in CAD:

1st - $5000

2nd - $2000

3rd - $1000

Partner choices - $1000 each

# Challenges
To be announced at opening.
=======
# CDL_Quantum_Hackathon_2021
Collaboration repository for CDL bootcamp Quantum Hackathon 2021.

The main branch contains a generic python 3 environment.
Vendor specific environment can be found in other branches.

This project uses [mybinder.org](https://mybinder.readthedocs.io/en/latest/introduction.html) online service.

To run it, open the following [link](https://mybinder.org/v2/gh/olegxtend/CDL_Quantum_Hackathon_2021/HEAD) in your browser. It may take a couple minutes to launch.

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
4. Re-launch the project in [mybinder.org](https://mybinder.org/v2/gh/olegxtend/CDL_Quantum_Hackathon_2021/HEAD)
>>>>>>> main-binder
