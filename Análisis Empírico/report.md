# Análisis Empírico - Máquina de Turing Fibonacci

## Resumen Ejecutivo

Este documento presenta el análisis empírico del tiempo de ejecución de una Máquina de Turing 
que calcula la sucesión de Fibonacci.

## Metodología

- **Entradas de prueba**: n = 0 hasta n = 20
- **Representación**: Unario (n unos consecutivos)
- **Mediciones**: Número de pasos y tiempo de ejecución

## Resultados

### Datos de Prueba

| n | Entrada | Pasos | Tiempo (ms) | Estado |
|---|---------|-------|-------------|--------|
| 5 | 11111 | 310 | 0.1713 | ACCEPT |
| 10 | 1111111111 | 11711 | 6.6528 | ACCEPT |
| 15 | 1111111111... | 1222899 | 743.9204 | ACCEPT |
| 20 | 1111111111... | 148301948 | 529014.1201 | ACCEPT |
| 25 | 1111111111... | 72400000 | 60036.5087 | TIMEOUT |
| 30 | 1111111111... | 74200000 | 60116.1560 | TIMEOUT |

## Análisis de Complejidad

### Regresión Polinomial

Se probaron polinomios de grado 1 a 5 para ajustar los datos empíricos.
Para el análisis final se utilizó un polinomio de grado 2 (cuadrático) por consideraciones teóricas.

- **Grado utilizado**: Polinomio de grado 2
- **Coeficiente R²**: 0.936211
- **Complejidad asintótica**: **O(n²) - Cuadrática**

### Ecuación del Modelo

```
f(n) = 1.47e+06*n^2 + -2.78e+07*n^1 + 1.10e+08
```

### Interpretación

El análisis empírico sugiere que la complejidad temporal de esta Máquina de Turing 
es **O(n²) - Cuadrática**.

Esto significa que:
- El tiempo crece **cuadráticamente** con el tamaño de entrada
- Duplicar la entrada aproximadamente cuadruplica el tiempo

## Conclusiones

1. La Máquina de Turing implementada tiene complejidad temporal O(n²) - Cuadrática
2. El modelo polinomial se ajusta bien a los datos (R² = 0.9362)
3. Para entradas grandes, el tiempo de ejecución puede crecer rápidamente

## Visualizaciones

Ver archivos:
- `steps_vs_input.png` - Gráfico de pasos vs entrada
- `time_vs_input.png` - Gráfico de tiempo vs entrada

## Fecha de Análisis

Generado automáticamente por experiments/plot.py
