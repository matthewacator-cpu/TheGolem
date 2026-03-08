import subprocess
import time
import sys

# Config
PS_PATH = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
SCRIPT_PATH = "C:\\Users\\matth\\OneDrive\\Desktop\\system\\get_window.ps1"
BAD_KEYWORDS = [" / X", "Twitter", "Reddit", "Facebook", "Instagram", "TikTok"]
GOOD_KEYWORDS = ["VS Code", "Terminal", "Clawdbot", ".py", ".md", "Docs"]

def get_active_window():
    try:
        result = subprocess.run(
            [PS_PATH, "-ExecutionPolicy", "Bypass", "-File", SCRIPT_PATH],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except:
        return ""

def monitor():
    focus_score = 50 # Start neutral
    print("Guardian initialized. Watching...")
    
    while True:
        title = get_active_window()
        timestamp = time.strftime("%H:%M:%S")
        
        is_bad = any(k in title for k in BAD_KEYWORDS)
        is_good = any(k in title for k in GOOD_KEYWORDS)
        
        if is_bad:
            focus_score -= 5
            print(f"[{timestamp}] DOOMSCROLL DETECTED: '{title}' (Focus: {focus_score})")
        elif is_good:
            focus_score += 2
            # Cap at 100
            focus_score = min(100, focus_score)
            # print(f"[{timestamp}] Working: '{title}' (Focus: {focus_score})")
        else:
            # Neutral drift
            focus_score -= 0.5
            
        # Intervention Threshold
        if focus_score < 20:
            print(f"\n!!! INTERVENTION !!!\nYour Focus is {focus_score}. You are drifting.\nCLOSE THE WINDOW.\n")
            focus_score = 30 # Reset slightly to avoid spam
            
        time.sleep(10)

if __name__ == "__main__":
    monitor()
