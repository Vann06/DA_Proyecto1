# Core: Tape y Loader

## Convenciones de la Cinta

- **Enteros no negativos**: Se representan en formato unario. Un número $n$ se representa como una secuencia de $n$ símbolos `1`. Por ejemplo, el número 3 se representa como `111`. El número 0 se representa como una cadena vacía (o una celda en blanco `_`).
- **Interpretación de respuesta**: La respuesta de la máquina se encuentra en la cinta al finalizar la ejecución. Para la máquina de Fibonacci, la respuesta es el número de Fibonacci $F(n)$ representado en unario. La máquina se detiene en un estado de aceptación (`qa`) si la computación fue exitosa, y la cabeza de lectura/escritura se posiciona al inicio de la respuesta o en una posición cercana definida por la convención de la máquina.

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
