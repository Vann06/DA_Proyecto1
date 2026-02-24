
"""
SIMULACION DE CINTA INFINITA
representación de la cinta para mantener la entrada, simbolos intermedios y 
la salida.

Utilizamos un diccionario ya que puede crecer en cualquier dirección y
en cualquier posición no guardada se interpreta como un blank 
"""

from __future__ import annotations

class Tape:
    # la cinta es un diccionario que mapean posiciones a caracteres 
    def __init__(self, input_str: str, blank: str = "_"):
        self.blank = blank
        self.head = 0
        self.cells: dict[int, str] = {}
        for i , ch in enumerate(input_str):
            if ch != blank:
                self.cells[i] = ch

    # devolver el simbolo donde está el cabezal, si no existe en cells devuelve blank
    def read(self) -> str:
        return self.cells.get(self.head, self.blank)
    
    # escribir sym en la pos actual, sino de guarda en cells[head]
    def write(self, sym:str) -> None:
        if sym == self.blank:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = sym

    # direccion e interpretacion S es para quedarse 
    def move(self, direction:str) -> None:
        if direction == "L":
            self.head -= 1
        elif direction == "R":
            self.head += 1
        elif direction == "S":
            # S = Stay, no mover el cabezal
            # antes teniamos self.head == "S"
            pass
        else:
            raise ValueError(f"Movimiento invalido:{direction}")
        
    # vista parcial de la cinta para imprimir en el trace
    def snapshot(self, window: int = 20) -> str:
        left = self.head - window
        right = self.head + window
        s = []
        for i in range(left, right +1):
            s.append(self.cells.get(i, self.blank))
        return "".join(s), left