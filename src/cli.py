import argparse
from .loader import load_machine
from .tape import Tape
from .machine import TuringMachine

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--machine", required=True, help="Ruta al archivo JSON de la máquina")
    p.add_argument("--input", required=True, help="Cadena de entrada (según convención)")
    p.add_argument("--trace", action="store_true", help="Imprimir configuraciones")
    p.add_argument("--max-steps", type=int, default=10000)
    p.add_argument("--window", type=int, default=20)
    args = p.parse_args()

    m = load_machine(args.machine)
    tape = Tape(args.input, blank=m.blank)
    tm = TuringMachine(m, tape)

    print(f"Machine: {m.name}")
    result = tm.run(max_steps=args.max_steps, trace=args.trace, window=args.window)
    print(f"RESULT: {result.status} | steps={result.steps} | final_state={result.final_state}")

if __name__ == "__main__":
    main()
