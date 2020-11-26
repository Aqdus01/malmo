import os, pickle

def get_config(checkpoint_file):
    # go a directory up to retrieve params.pkl
    checkpoint = os.path.join(os.path.dirname(os.path.dirname(checkpoint_file)), "params.pkl")
    with open(checkpoint, 'rb') as file:
        config = pickle.load(file)
    return config

def update_checkpoint_for_rollout(checkpoint_path):
    # RLlib sometimes complains about not seeing the trainer_state in the checkpoint so we manually add it
    with open(checkpoint_path, "rb") as f:
        extra_data = pickle.load(f)
    if not "trainer_state" in extra_data:
        extra_data["trainer_state"] = {}
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(extra_data, f)