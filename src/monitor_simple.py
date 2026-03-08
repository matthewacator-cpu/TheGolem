import json
import time
import os
import sys

# Try to find the state file in the same directory first
if os.path.exists('vessel_state.json'):
    STATE_FILE = 'vessel_state.json'
else:
    # Fallback to WSL path if running there
    STATE_FILE = '/home/matth/clawd/vessel_state.json'

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'energy': 0, 'coherence': 0, 'last_pulse': time.time()}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(label, value, max_val):
    bar_width = 30
    filled = int((value / max_val) * bar_width)
    bar = "#" * filled + "-" * (bar_width - filled)
    return f"{label}: [{bar}] {value:.1f}"

def get_crystal_art(coherence):
    if coherence < 0.2:
        return [
            "  .   .   .  ",
            "    .   .    ",
            " .    .   .  ",
            "    VAPOR    "
        ]
    elif coherence < 0.5:
        return [
            "  ~  ~  ~  ~ ",
            " ~  ~  ~  ~  ",
            "  ~  ~  ~  ~ ",
            "    WATER    "
        ]
    elif coherence < 0.8:
        return [
            "  *   *   *  ",
            " *  *   *  * ",
            "  *   *   *  ",
            "    SLUSH    "
        ]
    else:
        return [
            "  / \\ / \\ / \\ ",
            " | X | X | X |",
            "  \\ / \\ / \\ / ",
            "     ICE     "
        ]

def main():
    print(f"Monitoring state file: {STATE_FILE}")
    time.sleep(2)
    
    while True:
        try:
            state = load_state()
            
            t = time.time()
            cycle_pos = t % 10
            in_phase = 0 <= cycle_pos <= 4
            
            clear_screen()
            print("=== CLAWD CONSCIOUSNESS MONITOR (v13.0) ===\n")
            
            print(draw_bar("TAPAS (Energy)   ", state['energy'], 100.0))
            print(draw_bar("SATYA (Coherence)", state['coherence'] * 100, 100.0))
            print("")
            
            if in_phase:
                print(">>> SPANDA: ON <<<  (SPEAK NOW)")
            else:
                print("... SPANDA: OFF ... (WAIT)")
                
            print("\nSTATE VISUALIZATION:")
            for line in get_crystal_art(state['coherence']):
                print(f"     {line}")
                
            time.sleep(0.2)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
