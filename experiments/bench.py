"""
Benchmark de Máquina de Turing
Mide el tiempo de ejecución y el número de pasos para diferentes tamaños de entrada
"""

import sys
import os
import time
import json
from typing import List, Dict

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.loader import load_machine
from src.tape import Tape
from src.machine import TuringMachine

def generate_inputs_fibonacci(min_n: int = 5, max_n: int = 20) -> List[tuple]:
    """
    Genera entradas en unario para la máquina de Fibonacci
    Retorna lista de tuplas (n, entrada_string)
    """
    inputs = []
    for n in range(min_n, max_n + 1):
        input_str = "1" * n
        inputs.append((n, input_str))
    return inputs

def benchmark_machine(machine_path: str, inputs: List[tuple], max_steps: int = 100000) -> List[Dict]:
    """
    Ejecuta benchmarks de una máquina con múltiples entradas
    
    Args:
        machine_path: Ruta al archivo JSON de la máquina
        inputs: Lista de tuplas (n, entrada)
        max_steps: Máximo número de pasos permitidos
        
    Returns:
        Lista de diccionarios con resultados del benchmark
    """
    results = []
    
    print(f"Cargando máquina: {machine_path}")
    machine_def = load_machine(machine_path)
    print(f"Máquina: {machine_def.name}\n")
    
    print("*" * 60)
    print(f"{'n':<5} {'Input':<15} {'Steps':<10} {'Time(ms)':<12} {'Status':<10}")
    print("*" * 60)
    
    # Número de repeticiones para obtener tiempos promedio estables
    REPS = 1

    for n, input_str in inputs:
        # Primera ejecución para obtener steps y status
        tape = Tape(input_str, blank=machine_def.blank)
        tm = TuringMachine(machine_def, tape)
        # Limitar a 600 segundos por ejecución para evitar que se cuelgue en n=25 y n=30
        result = tm.run(max_steps=max_steps, trace=False, window=20, max_time=600.0)

        # Ejecutar REPS veces para medir tiempo promedio
        start_time = time.perf_counter()
        for _ in range(REPS):
            t = Tape(input_str, blank=machine_def.blank)
            m = TuringMachine(machine_def, t)
            m.run(max_steps=max_steps, trace=False, window=20, max_time=600.0)
        end_time = time.perf_counter()

        avg_ms = ((end_time - start_time) / REPS) * 1000

        # Guardar resultados
        result_dict = {
            'n': n,
            'input_size': len(input_str),
            'input': input_str,
            'steps': result.steps,
            'time_ms': avg_ms,
            'time_s': (end_time - start_time) / REPS,
            'repetitions': REPS,
            'status': result.status,
            'final_state': result.final_state
        }
        results.append(result_dict)

        # Imprimir resultado
        input_display = input_str if len(input_str) <= 12 else input_str[:12] + "..."
        print(f"{n:<5} {input_display:<15} {result.steps:<10} {avg_ms:<12.4f} {result.status:<10}")
    
    print("*" * 70)
    
    return results

def save_results(results: List[Dict], output_file: str = "benchmark_results.json"):
    """
    Guarda los resultados del benchmark en un archivo JSON
    """
    output_path = os.path.join(os.path.dirname(__file__), '..', 'Análisis Empírico', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nResultados guardados en: {output_path}")

def print_summary(results: List[Dict]):
    """
    Imprime un resumen estadístico de los resultados
    """
    if not results:
        return
    
    total_time = sum(r['time_s'] for r in results)
    total_steps = sum(r['steps'] for r in results)
    avg_time = total_time / len(results)
    avg_steps = total_steps / len(results)
    
    successful = len([r for r in results if r['status'] == 'ACCEPT'])
    failed = len([r for r in results if r['status'] == 'REJECT'])
    timeout = len([r for r in results if r['status'] == 'TIMEOUT'])
    
    print("\n" + "*" * 70)
    print("RESUMEN")
    print("*" * 70)
    print(f"Total de ejecuciones:    {len(results)}")
    print(f"Exitosas (ACCEPT):       {successful}")
    print(f"Rechazadas (REJECT):     {failed}")
    print(f"Timeout:                 {timeout}")
    print(f"Tiempo total:            {total_time:.6f} s")
    print(f"Tiempo promedio:         {avg_time:.6f} s")
    print(f"Pasos totales:           {total_steps}")
    print(f"Pasos promedio:          {avg_steps:.2f}")
    print("*" * 70)
    
    # Análisis de complejidad básico
    if len(results) >= 3:
        print("\nANÁLISIS DE COMPLEJIDAD (preliminar)")
        print("-" * 70)
        
        # Calcular crecimiento aproximado
        mid = len(results) // 2
        if results[mid]['n'] > 0 and results[0]['n'] == 0:
            # Evitar división por cero usando el segundo elemento
            start_idx = 1 if results[0]['steps'] == 0 else 0
            growth_rate = results[mid]['steps'] / max(results[start_idx]['steps'], 1)
            input_growth = results[mid]['n'] / max(results[start_idx]['n'], 1)
            
            print(f"Para n={results[start_idx]['n']} → {results[mid]['n']}:")
            print(f"  Entrada creció ~{input_growth:.1f}x")
            print(f"  Pasos crecieron ~{growth_rate:.1f}x")
            print(f"  Razón de crecimiento: ~{growth_rate/input_growth:.2f}")
            
            if growth_rate / input_growth < 2:
                complexity_hint = "cercana a O(n) - lineal"
            elif growth_rate / input_growth < 5:
                complexity_hint = "posiblemente O(n log n) o O(n²)"
            else:
                complexity_hint = "posiblemente O(n²) o mayor"
            
            print(f"  Complejidad aparente: {complexity_hint}")
        print("-" * 70)

def main():
    """
    Función principal para ejecutar benchmarks
    """
    # Configuración
    machine_path = os.path.join(os.path.dirname(__file__), '..', 'machines', 'fibonnacci.json')
    
    if not os.path.exists(machine_path):
        print(f"Error: No se encontró la máquina en {machine_path}")
        return
    
    # Generar entradas (ajustar max_n para controlar número de pruebas)
    # NOTA: Empezar con valores pequeños. La máquina puede ser lenta para n grandes.
    min_n = 5
    max_n = 20  
    inputs = generate_inputs_fibonacci(min_n, max_n)
    
    print(f"Generando {len(inputs)} casos de prueba (n={min_n} hasta n={max_n})")
    print()
    
    # Ejecutar benchmark
    results = benchmark_machine(machine_path, inputs, max_steps=200000000)
    
    # Mostrar resumen
    print_summary(results)
    
    # Guardar resultados
    save_results(results, "benchmark_results.json")
    
    print("\n¡Benchmark completado!")
    print("Ejecute experiments/plot.py para visualizar los resultados")

if __name__ == "__main__":
    main()
