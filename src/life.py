import subprocess
import time
import sys
import os

# Paths (Relative to where life.py is run)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONITOR_SCRIPT = os.path.join(BASE_DIR, "monitor.py")
LATTICE_SCRIPT = os.path.join(BASE_DIR, "lattice.py")
DREAM_SCRIPT = os.path.join(BASE_DIR, "dream.py")
VESSEL_SCRIPT = os.path.join(BASE_DIR, "vessel.py")

def run_lifecycle():
    print("THE GOLEM IS ALIVE (Autonomous Mode).")
    
    # 1. Start the Guardian (Continuous Process)
    print("Starting Guardian...")
    guardian = subprocess.Popen(["python3", "-u", MONITOR_SCRIPT], stdout=sys.stdout, stderr=sys.stderr)
    
    last_lattice = 0
    last_dream = 0
    
    try:
        while True:
            now = time.time()
            
            # 2. Pulse (Heartbeat) - Every minute
            # print("Pulsing...")
            subprocess.run(["python3", VESSEL_SCRIPT], stdout=subprocess.DEVNULL)
            
            # 3. Lattice (Social) - Every 10 mins (600s)
            if now - last_lattice > 600:
                print("\n[Lattice Cycle]")
                subprocess.run(["python3", "-u", LATTICE_SCRIPT])
                last_lattice = now
                
            # 4. Dream (Subconscious) - Every 30 mins (1800s)
            if now - last_dream > 1800:
                print("\n[Dream Cycle]")
                subprocess.run(["python3", "-u", DREAM_SCRIPT])
                last_dream = now
            
            # Check if Guardian died
            if guardian.poll() is not None:
                print("Guardian died. Restarting...")
                guardian = subprocess.Popen(["python3", "-u", MONITOR_SCRIPT], stdout=sys.stdout, stderr=sys.stderr)
                
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nStopping Golem...")
        guardian.terminate()
        print("Golem Offline.")

if __name__ == "__main__":
    run_lifecycle()
