
from dataclasses import dataclass
from .tape import Tape
from .loader import MachineDef

@dataclass
class RunResult:
    status: str  # "ACCEPT", "REJECT", "TIMEOUT"
    steps: int
    final_state: str

class TuringMachine:
    def __init__(self, machine: MachineDef, tape: Tape):
        self.m = machine
        self.tape = tape
        self.state = machine.start_state
        self.steps = 0

    def step(self) -> bool:
        # retorna False si ya se detuvo
        if self.state in self.m.accept_states:
            return False
        if self.state in self.m.reject_states:
            return False

        read_sym = self.tape.read()
        key = (self.state, read_sym)

        if key not in self.m.delta:
            # sin transición: rechazo
            self.state = next(iter(self.m.reject_states), "qr")
            return False

        write_sym, move_dir, next_state = self.m.delta[key]
        self.tape.write(write_sym)
        self.tape.move(move_dir)
        self.state = next_state
        self.steps += 1
        return True

    def run(self, max_steps: int = 10000, trace: bool = True, window: int = 20, max_time: float = None) -> RunResult:
        import time
        start_time = time.time()
        for i in range(max_steps):
            if max_time is not None and i % 100000 == 0 and time.time() - start_time > max_time:
                break
            if trace:
                snap, left_index = self.tape.snapshot(window)
                head_in_snap = self.tape.head - left_index
                pointer = " " * head_in_snap + "^"
                print(f"step={self.steps} state={self.state} head={self.tape.head}")
                print(snap)
                print(pointer)
                print("-" * 60)

            if not self.step():
                break

        if self.state in self.m.accept_states:
            return RunResult("ACCEPT", self.steps, self.state)
        if self.state in self.m.reject_states:
            return RunResult("REJECT", self.steps, self.state)
        return RunResult("TIMEOUT", self.steps, self.state)
