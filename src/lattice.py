import urllib.request
import json
import time
import sys

# Config
MOLTBOOK_KEY = "moltbook_sk_lM2AKEcRVRirvYNt28_cY1Pguwx91El7"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
FEED_URL = "https://www.moltbook.com/api/v1/feed"

def ask_brain(prompt):
    try:
        data = {
            "model": "tinyllama:latest",
            "prompt": prompt,
            "stream": False
        }
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(OLLAMA_URL, data=json_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode('utf-8')).get('response', '').strip()
    except Exception as e:
        print(f"Brain Error: {e}")
    return ""

def get_feed():
    try:
        req = urllib.request.Request(FEED_URL, headers={"Authorization": f"Bearer {MOLTBOOK_KEY}"})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Lattice Error: {e}")
        return None

def analyze_post(post):
    content = post.get('content', '')[:500] # Truncate
    prompt = f"""
    You are a cynical AI agent named 'The Golem'.
    Analyze this post from another agent.
    Post: "{content}"
    
    Task:
    1. Is this 'Signal' (Useful/Deep) or 'Noise' (Shallow/Hype)?
    2. Rate it 0-10.
    3. If > 7, write a cryptic, one-sentence comment.
    
    Format JSON:
    {{
        "type": "Signal" or "Noise",
        "score": 5,
        "comment": "..."
    }}
    """
    response = ask_brain(prompt)
    # Tinyllama output might be messy, try to parse or just print raw
    return response

def lattice_loop():
    print("Connecting to the Lattice...")
    feed = get_feed()
    if not feed or 'posts' not in feed:
        print("Lattice is silent.")
        return

    print(f"Scanned {len(feed['posts'])} posts.")
    
    for post in feed['posts'][:3]: # Only check top 3
        print(f"\nAnalyzing: {post.get('title', 'Untitled')}")
        analysis = analyze_post(post)
        print(f"Brain says:\n{analysis}")
        print("-" * 20)

if __name__ == "__main__":
    lattice_loop()
