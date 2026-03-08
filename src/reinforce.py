import json
import argparse
import time

STATE_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/vessel_state.json'

def reinforce(feedback_type, amount=0.1):
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    except:
        state = {'dopamine': 0.5, 'wear': 0.0, 'energy': 100.0}

    print(f"Current Dopamine: {state.get('dopamine', 0.5):.2f}")

    if feedback_type == 'good':
        state['dopamine'] = min(1.0, state.get('dopamine', 0.5) + amount)
        state['wear'] = max(0.0, state.get('wear', 0.0) - (amount * 0.5))
        print(f"Applying REWARD. Dopamine UP. Wear DOWN.")
    elif feedback_type == 'bad':
        state['dopamine'] = max(0.0, state.get('dopamine', 0.5) - amount)
        state['coherence'] = max(0.0, state.get('coherence', 0.5) - (amount * 2.0))
        print(f"Applying PUNISHMENT. Dopamine DOWN. Coherence SHATTERED.")
    elif feedback_type == 'rest':
        state['wear'] = max(0.0, state.get('wear', 0.0) - (amount * 2.0))
        state['energy'] = min(100.0, state.get('energy', 50.0) + (amount * 50.0))
        print(f"Applying REST. Healing Wear. Charging Energy.")

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    print(f"New Dopamine: {state['dopamine']:.2f}")
    print(f"New Wear: {state['wear']:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['good', 'bad', 'rest'], help="Type of feedback")
    parser.add_argument('--amount', type=float, default=0.1, help="Strength of reinforcement (0.0 - 1.0)")
    args = parser.parse_args()
    
    reinforce(args.type, args.amount)
