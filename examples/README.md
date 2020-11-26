# Malmo

This repository contains various improvements to the Malmo framework. This mainly involves the launcher to automatically handle the Malmo instances instead of the need to run them manually. We also updated the ```malmoenv``` python package to facilitate working with malmo. We also got some guides and examples to show how to work with Malmo in both single and multi-agent setups. The examples use RLlib, which provides a wide range of state-of-the-art Reinforcement Learning algorithms. In the examples we have created wrappers to make Malmo compatible to RLlib, but based on these examples it is easy to adapt Malmo to other frameworks.

We provide some examples with explanations in the form of IPython notebooks that are ready to run after getting the dependencies installed.
We have the following examples:
- [Random Player in Malmo](notebooks/random_agent_malmo.ipynb) - Explains the setup and shows how to interact with the environment using random action sampling.
- [RLlib single agent training](notebooks/rllib_single_agent.ipynb) - Expands the random agent example with using RLlib to handle RL experiments.
- [RLlib multi-agent training](notebooks/rllib_multi_agent.ipynb) - A multi-agent version of the previous example.
- [RLlib checkpoint evaluation](notebooks/rllib_evaluate_checkpoint.ipynb) - load checkpoint and evaluate the trained agent with capturing the agent's observations as a GIF. Can use this method to continue a training using ray's tune API.
- [RLlib checkpoint evaluation V2](notebooks/rllib_evaluate_checkpoint_v2.ipynb) - load a checkpoint and manually evaluate it by extracting the agent's policy.

We also provided non-notebook versions of these guides, which contain less explanation, but might be more reusable in your projects.

## Setup process 
- 1, clone malmo (```git clone https://github.com/martinballa/malmo```)
- 2, install java 8 and python 3. 
- 3, ```cd malmo/``` and install malmo using pip ```pip install -e MalmoEnv/``` 
- 4, Test if Malmo works correctly by running the examples in the ```examples/``` directory.
- 4*, Some examples requires ```ray``` (with ```tune``` and ```rllib```) installed and ```ffmpeg-python```. 
- +1, to run malmo headless on a linux headless server you should install xvfb ```sudo apt-get install -y xvfb```

*Note:* Minecraft uses gradle to build the project and it's not compatible with newer versions of Java, so make sure that you use java version 8 for the build and make sure that $JAVA_HOME is pointing to the correct version.

## Baseline results
Single-agent PPO

Multi-agent PPO