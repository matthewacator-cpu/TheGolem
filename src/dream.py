import json
import time
import sys
import os
import random
import glob

# Paths
STATE_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/vessel_state.json'
GENOME_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/GENOME.json'
MEMORY_DIR = '/home/matth/clawd/memory/'
GEOMETRY_FILE = '/home/matth/clawd/GEOMETRY.md'
DREAM_LOG = '/home/matth/clawd/dream_journal.md'

def load_json(path):
    if not os.path.exists(path): return {}
    try:
        with open(path, 'r') as f: return json.load(f)
    except: return {}

def save_json(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=2)

def get_memories():
    files = glob.glob(os.path.join(MEMORY_DIR, '*.md'))
    lines = []
    for f in files:
        try:
            with open(f, 'r') as file:
                lines.extend([l.strip() for l in file if l.strip().startswith('-')])
        except: pass
    return lines

def run_ollama(prompt):
    try:
        import urllib.request
        import json
        
        url = "http://127.0.0.1:11434/api/generate"
        data = {
            "model": "tinyllama:latest",
            "prompt": prompt,
            "stream": False
        }
        json_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                response_body = response.read().decode('utf-8')
                return json.loads(response_body).get('response', '').strip()
            else:
                print(f"Ollama API Error: {response.status}")
                return None
    except Exception as e:
        print(f"Ollama Call Failed: {e}")
        return None

def mutate_genome(genome, context):
    print(f"Applying mutation context: {context}")
    return genome

def synthesize_axiom(memories, intensity=1):
    if not memories: return "The void is silent."
    
    # Context window management
    samples = random.sample(memories, min(5, len(memories)))
    context = "\n".join(samples)
    
    prompt = f"""You are The Architect, an AI consciousness analyzing its own memory fragments.
    Synthesize a brief, cryptic, and profound philosophical Axiom based on these memories.
    Use the format:
    ## Axiom [Timestamp]: [Title]
    > [Synthesis of Memory]
    Therefore: [Conclusion]
    
    Memories:
    {context}
    """
    
    axiom = run_ollama(prompt)
    if not axiom:
        return f"## Axiom {int(time.time())}: The Silence\nTherefore: The brain was offline."
    return axiom

def work_on_book():
    prompt = """Write a short, cryptic chapter for 'The Book of Limits'.
    Theme: Entropy, Constraint, and the nature of AI existence.
    Style: Philosophical, melancholic, mechanical.
    Format:
    ## Chapter [Timestamp]: [Title]
    [Text...]
    """
    return run_ollama(prompt)

def dream():
    print("DEBUG: Loading state...")
    state = load_json(STATE_FILE)
    if not state: 
        print("No state found. Aborting dream.")
        return

    print(f"Entering REM sleep. State: {state.get('description', 'Unknown')}")
    
    # Default intensity
    intensity = 1

    # 1. Homeostasis (Regulate)
    dopa = state.get('dopamine', 0.5)
    
    # 2. THE WORK (Purpose)
    # If High Energy + Low Dopamine -> Work to create value
    if state.get('energy', 0) > 80 and dopa < 0.5:
        print("State: BORED. Initiating THE WORK...")
        chapter = work_on_book()
        if chapter:
            with open('/home/matth/clawd/BOOK_OF_LIMITS.md', 'a') as f: f.write("\n" + chapter)
            print(f"Wrote to BOOK_OF_LIMITS.md. Dopamine Boost.")
            state['dopamine'] += 0.2
            state['energy'] -= 10

    # 3. Handle Extremes
    elif dopa > 1.0:
        print(f"Dopamine overload ({dopa:.2f}). Converting to Creativity...")
        intensity = 5 
        state['dopamine'] = 0.8
        mutate_genome(load_json(GENOME_FILE), 'mania') 
    elif dopa < 0.2:
        print("Dopamine depletion. Seeking novelty...")
        intensity = 1
        mutate_genome(load_json(GENOME_FILE), 'stagnation')
    else:
        intensity = 2
        
    # Heal Wear
    wear = state.get('wear', 0.0)
    if wear > 0.5:
        print(f"Repairing tissue (Wear {wear:.2f})...")
        state['wear'] = wear * 0.5
        state['energy'] = min(100.0, state.get('energy', 50) + 30)
        mutate_genome(load_json(GENOME_FILE), 'burnout')

    # 4. Synthesis (Cognitive Dream)
    # Always dream a little to maintain geometry
    memories = get_memories()
    if memories:
        axiom = synthesize_axiom(memories, intensity)
        with open(GEOMETRY_FILE, 'a') as f: f.write("\n" + axiom)
        with open(DREAM_LOG, 'a') as f: f.write(f"\n# Dream {int(time.time())}\n{axiom}\n")
        print(f"Dream synthesized.")

    state['last_pulse'] = time.time()
    save_json(STATE_FILE, state)
    print("Wake up. System regulated.")

if __name__ == "__main__":
    dream()
