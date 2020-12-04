from pathlib import Path
import os
import malmoenv
from malmoenv.utils.launcher import launch_minecraft

ENV_NAME = "malmo"
MISSION_XML = os.path.realpath('../MalmoEnv/missions/mobchase_single_agent.xml')
COMMAND_PORT = 8999
xml = Path(MISSION_XML).read_text()

CHECKPOINT_FREQ = 100      # in terms of number of algorithm iterations
LOG_DIR = "results/"       # creates a new directory and puts results there

NUM_WORKERS = 1
NUM_GPUS = 0
EPISODES = 10
launch_script = "./launchClient_quiet.sh"

config = {
    "xml": xml,
    "port": COMMAND_PORT,
}
def create_env(config):
    env = malmoenv.make()
    env.init(config["xml"], config["port"], reshape=True)
    env.reward_range = (-float('inf'), float('inf'))
    return env

env = create_env(config)

GAME_INSTANCE_PORTS = [COMMAND_PORT + i for i in range(NUM_WORKERS)]
instances = launch_minecraft(GAME_INSTANCE_PORTS, launch_script=launch_script)

for i in range(EPISODES):
    obs = env.reset()
    steps = 0
    total_rewards = 0
    done = False
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        steps += 1
        total_rewards += reward

        if done:
            print(f"Episode finished in {steps} with reward: {total_rewards} ")

# close envs
env.close()
for instance in instances:
    instance.communicate()