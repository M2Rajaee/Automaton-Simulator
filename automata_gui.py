import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import defaultdict

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states, is_deterministic=True):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.is_deterministic = is_deterministic

    def _epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get(state, {}).get('ε', []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def _move(self, states, symbol):
        next_states = set()
        for state in states:
            next_states |= self.transitions.get(state, {}).get(symbol, set())
        return next_states

    def accepts(self, input_string, trace=False):
        output = []
        if self.is_deterministic:
            current_state = self.start_state
            output.append(f"Start at: {current_state}")
            for symbol in input_string:
                next_states = self.transitions.get(current_state, {}).get(symbol)
                if not next_states:
                    output.append(f"No transition from {current_state} on '{symbol}'. Reject.")
                    return False, "\n".join(output)
                current_state = list(next_states)[0]
                output.append(f"On '{symbol}' -> {current_state}")
            accepted = current_state in self.accept_states
            output.append(f"End at: {current_state}. Accepted: {accepted}")
            return accepted, "\n".join(output)
        else:
            current_states = self._epsilon_closure({self.start_state})
            output.append(f"Start at ε-closure({self.start_state}) = {current_states}")
            for symbol in input_string:
                next_states = self._epsilon_closure(self._move(current_states, symbol))
                output.append(f"On '{symbol}' -> {next_states}")
                current_states = next_states
            accepted = any(s in self.accept_states for s in current_states)
            output.append(f"End states: {current_states}. Accepted: {accepted}")
            return accepted, "\n".join(output)


class AutomatonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Finite Automaton Simulator")
        master.geometry("650x600")

        tk.Label(master, text="States (comma-separated):").pack()
        self.states_entry = tk.Entry(master, width=60)
        self.states_entry.pack()

        tk.Label(master, text="Alphabet (comma-separated):").pack()
        self.alphabet_entry = tk.Entry(master, width=60)
        self.alphabet_entry.pack()

        tk.Label(master, text="Start state:").pack()
        self.start_entry = tk.Entry(master, width=60)
        self.start_entry.pack()

        tk.Label(master, text="Accept states (comma-separated):").pack()
        self.accept_entry = tk.Entry(master, width=60)
        self.accept_entry.pack()

        tk.Label(master, text="Transitions (format: state,symbol->next1,next2):").pack()
        self.transition_text = scrolledtext.ScrolledText(master, width=60, height=10)
        self.transition_text.pack()

        self.mode = tk.StringVar(value="DFA")
        tk.Radiobutton(master, text="DFA", variable=self.mode, value="DFA").pack()
        tk.Radiobutton(master, text="NFA", variable=self.mode, value="NFA").pack()

        tk.Label(master, text="Input string:").pack()
        self.input_entry = tk.Entry(master, width=60)
        self.input_entry.pack()

        tk.Button(master, text="Run Simulation", command=self.run_simulation).pack(pady=10)

        tk.Label(master, text="Trace Output:").pack()
        self.output_box = scrolledtext.ScrolledText(master, width=70, height=15)
        self.output_box.pack()

    def parse_transitions(self, text):
        transitions = defaultdict(lambda: defaultdict(set))
        for line in text.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if "->" not in line:
                raise ValueError(f"Invalid transition format: {line}")
            left, right = line.split("->")
            state, symbol = left.split(",")
            next_states = set(s.strip() for s in right.split(","))
            transitions[state.strip()][symbol.strip()] |= next_states
        return transitions

    def run_simulation(self):
        try:
            states = [s.strip() for s in self.states_entry.get().split(",")]
            alphabet = [a.strip() for a in self.alphabet_entry.get().split(",")]
            start_state = self.start_entry.get().strip()
            accept_states = [a.strip() for a in self.accept_entry.get().split(",")]
            transitions = self.parse_transitions(self.transition_text.get("1.0", tk.END))
            is_deterministic = self.mode.get() == "DFA"
            automaton = FiniteAutomaton(states, alphabet, transitions, start_state, accept_states, is_deterministic)

            input_str = self.input_entry.get().strip()
            accepted, trace = automaton.accepts(input_str, trace=True)

            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, trace)
            self.output_box.insert(tk.END, f"\n\nResult: {'ACCEPTED ✅' if accepted else 'REJECTED ❌'}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonGUI(root)
    root.mainloop()
