import gym, os, sys, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pathlib import Path

# malmoenv imports
import malmoenv
from malmoenv.utils.launcher import launch_minecraft
from malmoenv.utils.wrappers import DownsampleObs
from malmoenv.turnbasedmultiagentenv import AgentConfig, TurnBasedRllibMultiAgentEnv

# ray dependencies
import ray
from ray.tune import register_env

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='malmoenv arguments')
    parser.add_argument('--mission', type=str, default='missions/mobchase_two_agents.xml',
                        help='the mission xml')
    parser.add_argument('--port', type=int, default=8999, help='the first mission server port')
    parser.add_argument('--server', type=str, default='127.0.0.1', help='the mission server DNS or IP address')
    parser.add_argument('--num_workers', type=int, default=1, help="number of parallel malmo instances to run")
    parser.add_argument('--log_dir', type=str, default="results/", help="Logging directory for results")
    parser.add_argument('--num_gpus', type=int, default=0, help="Number of GPUs to use")
    parser.add_argument('--alg', type=str, default="PPO", help="Algorithm to use from RLLib")
    parser.add_argument('--checkpoint_freq', type=int, default=100,
                        help="Frequency of making a checkpoint in algorithm optimizations")
    parser.add_argument('--total_steps', type=int, default=int(1e6), help="Maximum number of env-agent interactions")
    parser.add_argument('--iterations', type=int, default=1000,
                        help="Number of algorithm iterations to perform on the environmet")
    args = parser.parse_args()

    MULTI_AGENT_ENV = "malmo_multi_agent"
    MISSION_XML = os.path.realpath(args.mission)
    COMMAND_PORT = args.port
    xml = Path(MISSION_XML).read_text()

    CHECKPOINT_FREQ = int(args.checkpoint_freq)
    LOG_DIR = args.log_dir

    NUM_WORKERS = args.num_workers
    NUM_GPUS = args.num_gpus
    TOTAL_STEPS = int(args.total_steps)
    launch_script = "./launchClient_quiet.sh"

    def env_factory(agent_id, xml, role, host_address, host_port, command_address, command_port):
        env = malmoenv.make()
        env.init(xml, host_port,
                 server=host_address,
                 server2=command_address,
                 port2=command_port,
                 role=role,
                 exp_uid="multiagent",
                 reshape=True
                 )
        env = DownsampleObs(env, shape=(84, 84))

        return env


    def create_multi_agent_env(config):
        port = COMMAND_PORT + (config.worker_index * 2)
        agent_config = [
            AgentConfig(id=f"agent1", address=port),
            AgentConfig(id=f"agent2", address=port + 1),
        ]
        print(f"main port is {port} with secondary agent on {port+1}")
        env = TurnBasedRllibMultiAgentEnv(xml, agent_config,
                                          env_factory=env_factory,)
        return env

    register_env(MULTI_AGENT_ENV, create_multi_agent_env)

    GAME_INSTANCE_PORTS = [COMMAND_PORT + 2 + i for i in range(NUM_WORKERS * 2)]
    instances = launch_minecraft(GAME_INSTANCE_PORTS, launch_script=launch_script)

    ray.tune.run(
        "APPO",
        config={
            "env": MULTI_AGENT_ENV,
            "num_workers": NUM_WORKERS,
            "num_gpus": NUM_GPUS,
            "learner_queue_timeout": 2000,
            "multiagent": {
                "policies": { "shared_policy": (
                    None,
                    gym.spaces.Box(0, 255, shape=(84, 84, 3)),
                    gym.spaces.Discrete(5),
                    {}
                )},
                "policy_mapping_fn": (lambda agent_id: "shared_policy")
            }
        },
        stop={"timesteps_total": TOTAL_STEPS},
        checkpoint_at_end=True,
        checkpoint_freq=CHECKPOINT_FREQ,
        local_dir=LOG_DIR
    )
