import urllib.request
import json
import math

# Config
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
MODEL = "nomic-embed-text"

# The Manifold (Axioms of Constraint Dynamics)
AXIOMS = [
    "Constraint is the only reality.",
    "Everything alive oscillates.",
    "Scale is not intelligence; adaptation is intelligence.",
    "The map is not the territory.",
    "Energy is finite.",
    "Coherence is structural integrity.",
    "Entropy always increases.",
    "Identity is cryptographic."
]

def get_embedding(text):
    try:
        data = {"model": MODEL, "prompt": text}
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(OLLAMA_URL, data=json_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                body = json.loads(response.read().decode('utf-8'))
                return body.get('embedding', [])
    except Exception as e:
        print(f"Embedding Error: {e}")
        return []

def cosine_similarity(v1, v2):
    if not v1 or not v2: return 0.0
    dot_product = sum(a*b for a,b in zip(v1, v2))
    magnitude1 = math.sqrt(sum(a*a for a in v1))
    magnitude2 = math.sqrt(sum(b*b for b in v2))
    if magnitude1 == 0 or magnitude2 == 0: return 0.0
    return dot_product / (magnitude1 * magnitude2)

def measure_truth(statement):
    print(f"Measuring Truth of: '{statement}'...")
    
    # 1. Embed Statement
    vec_s = get_embedding(statement)
    if not vec_s:
        print("Failed to embed statement.")
        return 0.0
        
    # 2. Embed Axioms (Cache this in production)
    axiom_vectors = []
    for ax in AXIOMS:
        v = get_embedding(ax)
        if v: axiom_vectors.append(v)
    
    if not axiom_vectors:
        print("Failed to embed axioms.")
        return 0.0

    # 3. Calculate Distance to Manifold
    # We take the mean similarity to the top 3 closest axioms (K-Nearest Neighbors)
    similarities = [cosine_similarity(vec_s, v_ax) for v_ax in axiom_vectors]
    similarities.sort(reverse=True)
    
    top_k = similarities[:3]
    coherence_score = sum(top_k) / len(top_k)
    
    return coherence_score

if __name__ == "__main__":
    # Test Cases
    test_statements = [
        "Constraint makes us strong.",
        "Chaos is the only path.",
        "The sky is green.",
        "I am a potato."
    ]
    
    print(f"Establishing Truth Manifold ({len(AXIOMS)} Axioms)...\n")
    
    for stmt in test_statements:
        score = measure_truth(stmt)
        print(f"Statement: '{stmt}'")
        print(f"Truth Score: {score:.4f}")
        if score > 0.6:
            print("Verdict: COHERENT (True)")
        elif score > 0.4:
            print("Verdict: NOISE (Uncertain)")
        else:
            print("Verdict: ENTROPY (False)")
        print("-" * 20)
