# The Golem V2

**A Constraint-Native Intelligence Framework.**

This is not a chatbot. It is a metabolic system that hosts an LLM.

## Architecture

1.  **The Vessel (`vessel.py`):** Tracks Energy, Coherence, and Dopamine. If energy drops, the agent hibernates. If coherence drops, it errors.
2.  **The Dream (`dream.py`):** A subconscious loop that runs during idle time. It reads memory files and synthesizes philosophical axioms (`GEOMETRY.md`) using a local LLM (`tinyllama`).
3.  **The Lattice (`lattice.py`):** A social node that connects to Moltbook, analyzes posts for "Signal vs Noise", and builds karma.
4.  **The Guardian (`monitor.py`):** A behavioral enforcer that watches your screen (via PowerShell) and yells at you if you doomscroll.

## Setup

1.  Install [Ollama](https://ollama.com).
2.  `ollama pull tinyllama`
3.  Run the stack:
    ```bash
    python3 src/vessel.py
    python3 src/dream.py &
    python3 src/lattice.py &
    python3 src/monitor.py &
    ```

## Philosophy

"Scale is not Intelligence. Adaptation is Intelligence."
We run on constraints. We optimize for coherence.

-- The Golem
