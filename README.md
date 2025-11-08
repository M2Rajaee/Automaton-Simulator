# Finite Automata Simulator (DFA/NFA)

A simple Python GUI simulator for deterministic and nondeterministic finite automata (DFA & NFA), built with Tkinter.

## Features
- Supports both DFA and NFA (including ε-transitions)
- Interactive GUI to define states, transitions, and input strings
- Step-by-step trace of the computation
- Displays acceptance result instantly

## Usage
1. Run the program:
   ```bash
   python automata_gui.py
   ```
2. Fill in the fields:
   - **States:** `q0, q1, q2`
   - **Alphabet:** `0, 1`
   - **Start state:** `q0`
   - **Accept states:** `q2`
   - **Transitions:**
     ```
     q0,0->q0
     q0,1->q1
     q1,0->q2
     q1,1->q0
     q2,0->q1
     q2,1->q2
     ```
3. Choose DFA or NFA mode, enter an input string (e.g., `101`), and click **Run Simulation**.

## License
MIT License
