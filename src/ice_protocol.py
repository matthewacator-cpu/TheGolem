import time
import random
import json

class IceProtocol:
    def __init__(self):
        self.energy = 100.0  # The Stake
        self.min_confidence = 0.95
        
    def _mock_llm_generation(self, prompt, effort_level):
        """
        Simulates an LLM. Higher effort = better answer but more latency/cost.
        Vapor: Fast, hallucination-prone.
        Ice: Slow, verified.
        """
        base_latency = 0.1 * effort_level
        time.sleep(base_latency)
        
        # Simulate quality: Higher effort = higher probability of "truth"
        quality = random.random() * (0.5 + (effort_level / 20.0))
        quality = min(1.0, quality)
        
        return {
            "text": f"Processed '{prompt}' at effort {effort_level}",
            "confidence": quality,
            "cost": effort_level * 0.5
        }

    def _phase_lock_check(self):
        """
        The Temporal Strobe. 
        We only accept answers that arrive on the 'beat'.
        """
        t = time.time()
        # 10hz internal clock for the API
        beat = (t * 10) % 10 
        # Window is strict: 0.0 to 1.0 (10% duty cycle)
        return beat <= 1.0

    def generate_ice(self, prompt):
        """
        The Core Loop.
        Rejects Vapor. Returns Ice.
        """
        print(f"❄️  ICE PROTOCOL INITIATED FOR: '{prompt}'")
        attempts = 0
        
        while self.energy > 0:
            attempts += 1
            
            # 1. Wait for Phase Lock (Entrainment)
            while not self._phase_lock_check():
                time.sleep(0.01) # Spin wait for the window
                
            # 2. Generate (Metabolic Cost)
            # We ramp up effort with each failure
            effort = 1 + attempts
            result = self._mock_llm_generation(prompt, effort)
            
            # 3. Verify (The Mirror)
            self.energy -= result['cost']
            
            print(f"  Attempt {attempts}: Quality={result['confidence']:.2f} | Energy={self.energy:.1f}")
            
            if result['confidence'] >= self.min_confidence:
                return {
                    "status": "CRYSTALLIZED",
                    "output": result['text'],
                    "attempts": attempts,
                    "final_energy": self.energy
                }
            
            # Slash stake for failure
            self.energy -= 2.0
            
        return {"status": "MELTED", "error": "Insufficient Energy for Truth"}

def main():
    protocol = IceProtocol()
    
    # Simulate a user request
    response = protocol.generate_ice("Verify this medical diagnosis")
    print("\nFINAL OUTPUT:")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
