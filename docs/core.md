# Core: Tape y Loader

## Tape (src/tape.py)
La clase `Tape` modela la cinta infinita de una Máquina de Turing.

- Blanco: `"_"` (símbolo por defecto para celdas vacías).
- `head`: índice entero de la posición del cabezal.
- `cells`: diccionario `pos -> símbolo`, guardando solo posiciones no-blanco.

### Operaciones
- `read()`: lee el símbolo bajo el cabezal.
- `write(sym)`: escribe un símbolo; si es `"_"` se elimina de `cells`.
- `move("L"|"R"|"S")`: mueve el cabezal.
- `snapshot(window)`: devuelve una ventana parcial de la cinta para imprimir trazas.

## Loader (src/loader.py)
El loader carga una máquina desde un archivo JSON y la convierte a una estructura eficiente.

### Transición
Una transición define:
(state, read) -> (write, move, next)

### delta
El loader construye:
`delta[(state, read)] = (write, move, next)`
para poder obtener la transición en tiempo O(1) promedio.

El resultado es un `MachineDef` con:
- blank, start_state, accept/reject states
- delta (mapa de transiciones)
