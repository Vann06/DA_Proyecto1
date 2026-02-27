# Universidad del Valle de Guatemala
## Departamento de Computación
### Análisis y Diseño de Algoritmos

# Proyecto No. 1 Simulador de Máquina de Turing

Este proyecto implementa un simulador completo de una Máquina de Turing en Python. Incluye la capacidad de cargar máquinas desde archivos JSON, ejecutar simulaciones paso a paso con una cinta infinita, visualizar el diagrama de estados de la máquina y realizar análisis empíricos (benchmarks) de su rendimiento.

Como caso de estudio principal, el proyecto incluye una Máquina de Turing diseñada para calcular la secuencia de Fibonacci.

## Integrantes

* **Angie Nadissa Vela Lopez, 23764**
* **Vianka Vanessa Castro Ordoñez, 23201**

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

```text
DA_Proyecto1/
├── src/                    # Código fuente principal del simulador
│   ├── cli.py              # Interfaz de línea de comandos (CLI)
│   ├── machine.py          # Lógica central de la Máquina de Turing
│   ├── tape.py             # Implementación de la cinta infinita
│   ├── loader.py           # Carga y validación de máquinas desde JSON
│   └── visualize_tm.py     # Generador de diagramas de estados (Graphviz/DOT)
├── machines/               # Definiciones de Máquinas de Turing en formato JSON
│   ├── fibonacci.json      # Máquina para calcular la secuencia de Fibonacci
│   └── example.json        # Máquina de ejemplo
├── experiments/            # Scripts para pruebas de rendimiento
│   ├── bench.py            # Ejecución de benchmarks (tiempo y pasos)
│   └── plot.py             # Generación de gráficas de los resultados
├── Análisis Empírico/      # Resultados de los experimentos y reportes
│   ├── benchmark_results.json
│   ├── fibonacci_tm.dot
│   └── report.md
├── docs/                   # Documentación adicional del proyecto
│   ├── core.md
│   └── doc.md
├── requirements.txt        # Dependencias de Python
└── README.md               # Este archivo
```

## Requisitos e Instalación

Asegúrate de tener instalado **Python 3.8+**. Para instalar las dependencias necesarias, ejecuta:

```bash
pip install -r requirements.txt
```

*Nota: Para la generación de imágenes a partir de los archivos `.dot` en la visualización, es necesario tener instalado [Graphviz](https://graphviz.org/download/) en tu sistema y agregado al PATH.*

##  Uso del Simulador

Puedes ejecutar el simulador desde la línea de comandos utilizando el script `src/cli.py`. 

**Sintaxis básica:**
```bash
python -m src.cli --machine <ruta_al_json> --input <cadena_entrada> [--trace] [--max-steps <num>]
```

**Ejemplo de ejecución:**
```bash
python -m src.cli --machine machines/fibonacci.json --input "11111" --trace
```

* `--machine`: Ruta al archivo JSON que define la Máquina de Turing.
* `--input`: Cadena de entrada inicial en la cinta.
* `--trace`: (Opcional) Imprime la configuración de la cinta y el estado en cada paso.
* `--max-steps`: (Opcional) Límite máximo de pasos para evitar bucles infinitos (por defecto: 10000).
* `--window`: (Opcional) Tamaño de la ventana de la cinta a mostrar en el trace (por defecto: 20).

##  Visualización de la Máquina

El proyecto incluye una herramienta para generar diagramas de transición de estados a partir de los archivos JSON.

```bash
python src/visualize_tm.py
```
*(Asegúrate de revisar los argumentos dentro del script o modificar la ruta del JSON de entrada según sea necesario).* Esto generará un archivo `.dot` y un `.png` con el grafo de la máquina.

## Análisis Empírico y Benchmarks

Para evaluar el rendimiento de la Máquina de Turing (por ejemplo, midiendo la complejidad temporal en función de la longitud de la entrada), puedes utilizar los scripts en la carpeta `experiments/`.

1. **Ejecutar Benchmarks:**
   ```bash
   python experiments/bench.py
   ```
   Esto ejecutará la máquina con diferentes tamaños de entrada y guardará los resultados.

2. **Generar Gráficas:**
   ```bash
   python experiments/plot.py
   ```
   Generará gráficas utilizando `matplotlib` para visualizar la relación entre el tamaño de la entrada, el número de pasos y el tiempo de ejecución.

## Formato de Definición de Máquinas (JSON)

Las máquinas se definen en archivos JSON con la siguiente estructura básica:

```json
{
  "name": "Nombre de la Máquina",
  "states": ["q0", "q1", "q_accept", "q_reject"],
  "input_alphabet": ["0", "1"],
  "tape_alphabet": ["0", "1", "_"],
  "start_state": "q0",
  "blank": "_",
  "accept_states": ["q_accept"],
  "reject_states": ["q_reject"],
  "transitions": [
    {
      "state": "q0",
      "read": "1",
      "next": "q1",
      "write": "0",
      "move": "R"
    }
  ]
}
```
