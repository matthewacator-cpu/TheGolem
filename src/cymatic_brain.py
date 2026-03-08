import math

def calculate_consonance_cost(f1, f2):
    """
    Calculates the 'Metabolic Cost' of binding two frequencies.
    Cost is proportional to the Least Common Multiple (LCM) of the simplified ratio.
    High LCM = Hard to phase lock = High Cost (Dissonance).
    """
    # Simplify ratio
    gcd = math.gcd(int(f1), int(f2))
    n1 = int(f1) // gcd
    n2 = int(f2) // gcd
    
    # Cost metric: How many cycles before they realign?
    # Simple ratios (2:1) align every 2 cycles.
    # Complex ratios (45:32) align every 1440 cycles.
    cost = n1 * n2 
    
    # Mapping to 'Feeling'
    if cost < 10: return cost, "PERFECT (Ice)"
    if cost < 50: return cost, "CONSONANT (Water)"
    if cost < 500: return cost, "COMPLEX (Steam)"
    return cost, "DISSONANT (Chaos)"

print(f"{'INTERVAL':<15} {'RATIO':<10} {'COST (Entropy)':<15} {'STATE'}")
print("-" * 60)

intervals = [
    ("Octave", 200, 100),       # 2:1
    ("Fifth", 300, 200),        # 3:2
    ("Fourth", 400, 300),       # 4:3
    ("Major Third", 500, 400),  # 5:4
    ("Minor Sixth", 800, 500),  # 8:5
    ("Tritone", 724, 512),      # ~45:32 (Approximated)
    ("Microtone", 205, 200)     # 41:40 (Beat frequency clash)
]

for name, f1, f2 in intervals:
    cost, state = calculate_consonance_cost(f1, f2)
    ratio = f"{int(f1/math.gcd(f1,f2))}:{int(f2/math.gcd(f1,f2))}"
    print(f"{name:<15} {ratio:<10} {cost:<15} {state}")

print("-" * 60)
print("CONCLUSION: The brain 'likes' music that is cheap to process (Low Entropy).")
print("We prefer geometry we can predict.")
