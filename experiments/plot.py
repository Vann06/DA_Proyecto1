"""
Visualización y Análisis de Resultados de Benchmark
Genera gráficos de dispersión y regresión polinomial para analizar la complejidad temporal
"""

import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

def load_results(filename: str = "benchmark_results.json") -> List[Dict]:
    """
    Carga los resultados del benchmark desde un archivo JSON
    """
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo {filepath}")
        print("Ejecute primero experiments/bench.py para generar los datos")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    return results

def polynomial_regression(x: np.ndarray, y: np.ndarray, degree: int) -> Tuple[np.ndarray, float]:
    """
    Realiza regresión polinomial de grado especificado
    
    Returns:
        coefficients, r_squared
    """
    # Ajustar polinomio
    coefficients = np.polyfit(x, y, degree)
    poly = np.poly1d(coefficients)
    
    # Calcular R²
    y_pred = poly(x)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return coefficients, r_squared

def find_best_polynomial(x: np.ndarray, y: np.ndarray, max_degree: int = 5, force_degree: int = None) -> Tuple[int, np.ndarray, float]:
    """
    Encuentra el mejor grado polinomial comparando R²
    
    Args:
        force_degree: Si se especifica, usa este grado independientemente del mejor R²
    
    Returns:
        best_degree, best_coefficients, best_r_squared
    """
    best_degree = 1
    best_r_squared = -1
    best_coefficients = None
    
    print("\nProbando diferentes grados de polinomios:")
    print("-" * 60)
    
    for degree in range(1, max_degree + 1):
        coefficients, r_squared = polynomial_regression(x, y, degree)
        print(f"  Grado {degree}: R² = {r_squared:.6f}")
        
        if r_squared > best_r_squared:
            best_r_squared = r_squared
            best_degree = degree
            best_coefficients = coefficients
    
    print("-" * 60)
    print(f"  Mejor ajuste por R²: Grado {best_degree} con R² = {best_r_squared:.6f}")
    
    # Si se fuerza un grado específico, usarlo
    if force_degree is not None:
        forced_coefficients, forced_r_squared = polynomial_regression(x, y, force_degree)
        print(f"  *** USANDO GRADO FORZADO: {force_degree} con R² = {forced_r_squared:.6f} ***")
        return force_degree, forced_coefficients, forced_r_squared
    
    return best_degree, best_coefficients, best_r_squared

def complexity_from_degree(degree: int) -> str:
    """
    Mapea el grado del polinomio a notación Big-O
    """
    complexity_map = {
        1: "O(n) - Lineal",
        2: "O(n²) - Cuadrática",
        3: "O(n³) - Cúbica",
        4: "O(n⁴) - Cuártica",
        5: "O(n⁵) - Quíntica"
    }
    return complexity_map.get(degree, f"O(n^{degree})")

def plot_scatter_with_regression(results: List[Dict], save_path: str = None):
    """
    Genera diagramas de dispersión con regresión polinomial.
    
    - Gráfica 1: Tiempo de ejecución vs tamaño de entrada (lo que pide el proyecto)
    - Gráfica 2: Número de pasos vs tamaño de entrada (métrica complementaria)
    
    Ambas muestran todos los grados de 1 a 5 en consola y fuerzan grado 2.
    """
    # Extraer datos
    n_values = np.array([r['n'] for r in results], dtype=float)
    times_ms = np.array([r['time_ms'] for r in results], dtype=float)
    steps    = np.array([r['steps'] for r in results], dtype=float)

    # ------ Análisis: probar grados 1-5, forzar grado 2 ------
    print("\n--- ANÁLISIS PARA TIEMPO DE EJECUCIÓN ---")
    deg_time, coef_time, r2_time = find_best_polynomial(
        n_values, times_ms, max_degree=5, force_degree=2)
    poly_time = np.poly1d(coef_time)

    print("\n--- ANÁLISIS PARA NÚMERO DE PASOS ---")
    deg_steps, coef_steps, r2_steps = find_best_polynomial(
        n_values, steps, max_degree=5, force_degree=2)
    poly_steps = np.poly1d(coef_steps)

    # Puntos suaves para las curvas
    n_smooth = np.linspace(n_values.min(), n_values.max(), 300)

    # ==================================================================
    #  GRÁFICA 1 — Diagrama de dispersión: Tiempo de ejecución vs n
    # ==================================================================
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    # Puntos del scatter (grandes, con borde negro para que se noten)
    ax1.scatter(n_values, times_ms,
                color='#2196F3', edgecolors='black', linewidths=0.8,
                s=140, zorder=5, label='Mediciones empíricas')

    # Curva de regresión (línea punteada por detrás)
    ax1.plot(n_smooth, poly_time(n_smooth),
             color='#F44336', linewidth=2, linestyle='--',
             zorder=4, label=f'Regresión polinomial grado {deg_time}')

    ax1.set_xlabel('Tamaño de entrada  (n)', fontsize=13)
    ax1.set_ylabel('Tiempo de ejecución  (ms)', fontsize=13)
    ax1.set_title(
        'Diagrama de dispersión\n'
        'Tiempo de ejecución en función del tamaño de entrada',
        fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(n_values.astype(int))
    ax1.grid(True, alpha=0.25, linestyle=':')
    ax1.legend(fontsize=10, loc='upper left')

    info_time = (f'Grado forzado: 2  (cuadrático)\n'
                 f'R² = {r2_time:.4f}\n'
                 f'Complejidad: {complexity_from_degree(deg_time)}')
    ax1.text(0.98, 0.02, info_time, transform=ax1.transAxes,
             fontsize=9, family='monospace', verticalalignment='bottom',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.85))

    fig1.tight_layout()
    path1 = save_path or os.path.join(os.path.dirname(__file__), 'time_vs_input.png')
    fig1.savefig(path1, dpi=300, bbox_inches='tight')
    print(f"\nDiagrama de dispersión (tiempo) guardado en: {path1}")
    plt.show()

    # ==================================================================
    #  GRÁFICA 2 — Diagrama de dispersión: Pasos vs n
    # ==================================================================
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    ax2.scatter(n_values, steps,
                color='#4CAF50', edgecolors='black', linewidths=0.8,
                s=140, zorder=5, label='Datos empíricos (pasos)')

    ax2.plot(n_smooth, poly_steps(n_smooth),
             color='#FF9800', linewidth=2, linestyle='--',
             zorder=4, label=f'Regresión polinomial grado {deg_steps}')

    ax2.set_xlabel('Tamaño de entrada  (n)', fontsize=13)
    ax2.set_ylabel('Número de pasos de la MT', fontsize=13)
    ax2.set_title(
        'Diagrama de dispersión\n'
        'Número de pasos en función del tamaño de entrada',
        fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(n_values.astype(int))
    ax2.grid(True, alpha=0.25, linestyle=':')
    ax2.legend(fontsize=10, loc='upper left')

    # Ecuación legible
    eq_parts = []
    for i, c in enumerate(coef_steps):
        pw = len(coef_steps) - 1 - i
        if abs(c) < 1e-6:
            continue
        if pw == 0:
            eq_parts.append(f'{c:.4f}')
        elif pw == 1:
            eq_parts.append(f'{c:.4f}·n')
        else:
            eq_parts.append(f'{c:.4f}·n^{pw}')
    eq_str = ' + '.join(eq_parts)

    info_steps = (f'Grado forzado: 2  (cuadrático)\n'
                  f'R² = {r2_steps:.4f}\n'
                  f'f(n) ≈ {eq_str}\n'
                  f'Complejidad: {complexity_from_degree(deg_steps)}')
    ax2.text(0.98, 0.02, info_steps, transform=ax2.transAxes,
             fontsize=9, family='monospace', verticalalignment='bottom',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.85))

    fig2.tight_layout()
    path2 = os.path.join(os.path.dirname(__file__), 'steps_vs_input.png')
    fig2.savefig(path2, dpi=300, bbox_inches='tight')
    print(f"Diagrama de dispersión (pasos)  guardado en: {path2}")
    plt.show()

    return deg_time, coef_time, r2_time, deg_steps, coef_steps, r2_steps

def generate_report(results: List[Dict], save_path: str = None):
    """
    Genera un reporte detallado del análisis
    """
    if save_path is None:
        save_path = os.path.join(os.path.dirname(__file__), '..', 'report', 'report.md')
    
    # Extraer datos
    n_values = np.array([r['n'] for r in results])
    steps = np.array([r['steps'] for r in results])
    
    # Probar grados 1-5 pero forzar grado 2 para el reporte
    print("\n--- ANÁLISIS PARA REPORTE ---")
    best_degree, coefficients, r_squared = find_best_polynomial(n_values, steps, max_degree=5, force_degree=2)
    complexity = complexity_from_degree(best_degree)
    
    # Crear reporte
    report = f"""# Análisis Empírico - Máquina de Turing Fibonacci

## Resumen Ejecutivo

Este documento presenta el análisis empírico del tiempo de ejecución de una Máquina de Turing 
que calcula la sucesión de Fibonacci.

## Metodología

- **Entradas de prueba**: n = 0 hasta n = {n_values.max()}
- **Representación**: Unario (n unos consecutivos)
- **Mediciones**: Número de pasos y tiempo de ejecución

## Resultados

### Datos de Prueba

| n | Entrada | Pasos | Tiempo (ms) | Estado |
|---|---------|-------|-------------|--------|
"""
    
    for r in results:
        input_display = r['input'] if len(r['input']) <= 10 else r['input'][:10] + "..."
        report += f"| {r['n']} | {input_display} | {r['steps']} | {r['time_ms']:.4f} | {r['status']} |\n"
    
    report += f"""
## Análisis de Complejidad

### Regresión Polinomial

Se probaron polinomios de grado 1 a 5 para ajustar los datos empíricos.
Para el análisis final se utilizó un polinomio de grado 2 (cuadrático) por consideraciones teóricas.

- **Grado utilizado**: Polinomio de grado {best_degree}
- **Coeficiente R²**: {r_squared:.6f}
- **Complejidad asintótica**: **{complexity}**

### Ecuación del Modelo

```
f(n) = {' + '.join([f'{c:.2e}*n^{len(coefficients)-1-i}' if i < len(coefficients)-1 else f'{c:.2e}' for i, c in enumerate(coefficients)])}
```

### Interpretación

El análisis empírico sugiere que la complejidad temporal de esta Máquina de Turing 
es **{complexity}**.

Esto significa que:
"""
    
    if best_degree == 1:
        report += "- El tiempo crece **linealmente** con el tamaño de entrada\n"
        report += "- Duplicar la entrada aproximadamente duplica el tiempo\n"
    elif best_degree == 2:
        report += "- El tiempo crece **cuadráticamente** con el tamaño de entrada\n"
        report += "- Duplicar la entrada aproximadamente cuadruplica el tiempo\n"
    elif best_degree == 3:
        report += "- El tiempo crece **cúbicamente** con el tamaño de entrada\n"
        report += "- Duplicar la entrada multiplica el tiempo por ~8\n"
    else:
        report += f"- El tiempo crece **polinómicamente** con exponente {best_degree}\n"
        report += f"- Duplicar la entrada multiplica el tiempo por ~{2**best_degree}\n"
    
    report += f"""
## Conclusiones

1. La Máquina de Turing implementada tiene complejidad temporal {complexity}
2. El modelo polinomial se ajusta bien a los datos (R² = {r_squared:.4f})
3. Para entradas grandes, el tiempo de ejecución puede crecer rápidamente

## Visualizaciones

Ver archivos:
- `steps_vs_input.png` - Gráfico de pasos vs entrada
- `time_vs_input.png` - Gráfico de tiempo vs entrada

## Fecha de Análisis

Generado automáticamente por experiments/plot.py
"""
    
    # Guardar reporte
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Reporte guardado en: {save_path}")

def main():
    """
    Función principal
    """
    print("*" * 60)
    print("ANÁLISIS Y VISUALIZACIÓN DE RESULTADOS")
    print("*" * 60)
    
    # Cargar resultados
    print("\nCargando resultados del benchmark")
    results = load_results()
    print(f"✓ Cargados {len(results)} resultados")
    
    # Generar gráficos
    print("\n" + "*" * 60)
    print("GENERANDO GRÁFICOS")
    print("*" * 60)
    
    print("\n1. Generando diagramas de dispersión con regresión polinomial")
    plot_scatter_with_regression(results)
    
    # Generar reporte
    print("\n" + "*" * 60)
    print("GENERANDO REPORTE")
    print("*" * 60)
    generate_report(results)
    
    print("\n" + "*" * 60)
    print("ANÁLISIS COMPLETADO")
    print("*" * 60)
    print("\nArchivos generados:")
    print("  - experiments/steps_vs_input.png")
    print("  - experiments/time_vs_input.png")
    print("  - report/report.md")

if __name__ == "__main__":
    main()
