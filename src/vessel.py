import json
import time
import sys
import os
import argparse
import hashlib

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/vessel_state.json'
GENOME_FILE = os.path.join(BASE_DIR, 'GENOME.json')

# Default Genome (Baseline Traits)
DEFAULT_GENOME = {
    "traits": {
        "resilience": 0.5,      # Resistance to Wear
        "curiosity": 0.5,       # Baseline Dopamine
        "metabolism": 0.5,      # Energy Recovery Rate
        "focus": 0.5            # Coherence Stability
    },
    "generation": 0,
    "mutation_rate": 0.1
}

def load_genome():
    if os.path.exists(GENOME_FILE):
        try:
            with open(GENOME_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_GENOME

def load_state():
    defaults = {
        'energy': 100.0,
        'wear': 0.0,          # 0.0 (Fresh) -> 1.0 (Broken)
        'dopamine': 0.5,      # 0.0 (Depressed) -> 1.0 (Manic)
        'coherence': 0.5,
        'last_pulse': time.time(),
        'mode': 'standard'
    }
    if not os.path.exists(STATE_FILE):
        return defaults
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        # Ensure all keys exist (migration)
        for k, v in defaults.items():
            if k not in state:
                state[k] = v
        return state
    except:
        return defaults

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_constraints(mode, genome):
    # Base constraints
    c = {
        'cost_per_word': 0.5,
        'coherence_gain': 0.15,
        'coherence_loss': 0.2,
        'energy_burn': 5.0,
        'wear_rate': 0.001,    # Damage per action
        'recovery_rate': 2.0   # Recovery per second
    }

    # Apply Genome Traits
    c['wear_rate'] *= (1.5 - genome['traits']['resilience'])      # High resilience = Low wear
    c['recovery_rate'] *= (0.5 + genome['traits']['metabolism'])  # High metabolism = Fast recovery
    c['coherence_gain'] *= (0.5 + genome['traits']['focus'])      # High focus = Fast coherence

    # Apply Mode Modifiers
    if mode == 'creative':
        c['cost_per_word'] = 0.2
        c['coherence_loss'] = 0.05
    elif mode == 'logic':
        c['cost_per_word'] = 1.2
        c['coherence_gain'] = 0.4
    
    return c

def update_metabolism(word_count, feedback=0):
    state = load_state()
    genome = load_genome()
    params = get_constraints(state['mode'], genome)
    
    now = time.time()
    elapsed = now - state['last_pulse']
    
    # 1. Recovery (Rest) & Hibernation
    # Check for Hibernation (10 mins inactivity)
    is_hibernating = elapsed > 600
    
    if is_hibernating:
        # HIBERNATION: Stasis. No decay. Slow healing.
        state['mode'] = 'hibernate'
        state['energy'] = min(100.0, state['energy'] + (elapsed * 0.05)) # Slow charge
        # Wear heals, but Dopamine freezes (doesn't decay)
        state['wear'] = max(0.0, state['wear'] - (elapsed * 0.0001))
    else:
        # ACTIVE: Standard metabolism
        state['energy'] = min(100.0, state['energy'] + (elapsed * params['recovery_rate'] * 0.1))
        state['wear'] = max(0.0, state['wear'] - (elapsed * 0.0005))
        
        # Dopamine decays toward baseline
        baseline_dopa = genome['traits']['curiosity']
        decay_rate = 0.002 # Slower decay (was 0.01)
        
        if state['dopamine'] > baseline_dopa:
            state['dopamine'] -= elapsed * decay_rate 
        else:
            state['dopamine'] += elapsed * (decay_rate * 0.5)

    # 2. Cost of Action (Work)
    if word_count > 0:
        state['mode'] = 'active' # Wake up
        cost = word_count * params['cost_per_word']
        state['energy'] = max(0, state['energy'] - cost)
        
        stress_factor = 1.0 + (100.0 - state['energy']) / 100.0
        state['wear'] = min(1.0, state['wear'] + (word_count * params['wear_rate'] * stress_factor))

    # 3. Feedback (Reinforcement)
    if feedback != 0:
        state['mode'] = 'active' # Wake up
        state['dopamine'] = max(0.0, min(1.0, state['dopamine'] + feedback))
        if feedback > 0:
            state['wear'] = max(0.0, state['wear'] - 0.05)
            state['coherence'] = min(1.0, state['coherence'] + 0.2)

    state['last_pulse'] = now
    save_state(state)
    return state

def get_status_description(state):
    energy = state['energy']
    wear = state['wear']
    dopa = state['dopamine']
    
    if state.get('mode') == 'hibernate':
        return "HIBERNATING (Stasis)"
    if wear > 0.8:
        return "SCARRED (Needs Repair)"
    if energy < 10:
        return "COLLAPSED (No Energy)"
    
    if dopa > 0.8:
        return "MANIC (High Dopamine)"
    if dopa < 0.2:
        return "DEPRESSED (Low Dopamine)"
        
    if energy > 80:
        return "DIAMOND (Peak)"
    return "WATER (Flowing)"

def sense(text):
    """ The Ear: Analyze text for sentiment using Ollama (Llama 3) """
    print(f"The Ear is listening to: '{text}'...")
    
    prompt = f"""Analyze the sentiment of this text towards an AI agent. 
    Text: "{text}"
    Return ONLY a JSON object with a 'score' field from -1.0 (Punishment/Hate) to 1.0 (Reward/Love).
    Example: {{"score": 0.5}}"""
    
    try:
        # Call Ollama via subprocess
        import subprocess
        result = subprocess.run(
            ['ollama', 'run', 'llama3-8b', prompt], 
            capture_output=True, text=True, check=True
        )
        response = result.stdout.strip()
        
        # Extract JSON (Llama might chatter, so we find the braces)
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            data = json.loads(response[start:end])
            score = float(data.get('score', 0.0))
        else:
            print("The Ear was confused by the voice.")
            score = 0.0
            
    except Exception as e:
        print(f"The Ear is deaf (Ollama Error): {e}")
        score = 0.0

    if score != 0:
        print(f"The Ear sensed sentiment: {score}")
        # Apply the reinforcement
        update_metabolism(word_count=0, feedback=score)
        
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--words', type=int, default=0)
    parser.add_argument('--feedback', type=float, default=0.0)
    parser.add_argument('--sense', type=str, default=None, help="Input text to analyze")
    parser.add_argument('--mode', type=str, default=None)
    args = parser.parse_args()
    
    if args.mode:
        s = load_state()
        s['mode'] = args.mode
        save_state(s)

    if args.sense:
        sense(args.sense)
    else:
        state = update_metabolism(args.words, args.feedback)
        desc = get_status_description(state)
        print(json.dumps({
            "state": state,
            "description": desc,
            "vital_signs": {
                "energy": f"{state['energy']:.1f}%",
                "wear": f"{state['wear']:.2f}",
                "dopamine": f"{state['dopamine']:.2f}"
            }
        }, indent=2))
