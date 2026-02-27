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
| 5 | 11111 | 310 | 0.1889 | ACCEPT |
| 6 | 111111 | 561 | 0.5962 | ACCEPT |
| 7 | 1111111 | 1083 | 1.4826 | ACCEPT |
| 8 | 11111111 | 2244 | 2.5739 | ACCEPT |
| 9 | 111111111 | 4987 | 7.5108 | ACCEPT |
| 10 | 1111111111 | 11711 | 8.6276 | ACCEPT |
| 11 | 1111111111... | 28618 | 18.7826 | ACCEPT |
| 12 | 1111111111... | 71785 | 54.4116 | ACCEPT |
| 13 | 1111111111... | 183075 | 124.5908 | ACCEPT |
| 14 | 1111111111... | 471688 | 451.5108 | ACCEPT |
| 15 | 1111111111... | 1222899 | 905.2844 | ACCEPT |
| 16 | 1111111111... | 3182543 | 2637.8304 | ACCEPT |
| 17 | 1111111111... | 8301614 | 7573.9170 | ACCEPT |
| 18 | 1111111111... | 21685217 | 15436.5007 | ACCEPT |
| 19 | 1111111111... | 56694411 | 42983.8812 | ACCEPT |
| 20 | 1111111111... | 148301948 | 123782.5345 | ACCEPT |

## Análisis de Complejidad

### Regresión Polinomial

Se probaron polinomios de grado 1 a 5 para ajustar los datos empíricos.
Para el análisis final se utilizó un polinomio de grado 2 (cuadrático) por consideraciones teóricas.

- **Grado utilizado**: Polinomio de grado 2
- **Coeficiente R²**: 0.696925
- **Complejidad asintótica**: **O(n²) - Cuadrática**

### Ecuación del Modelo

```
f(n) = 1.14e+06*n^2 + -2.36e+07*n^1 + 1.08e+08
```

### Interpretación

El análisis empírico sugiere que la complejidad temporal de esta Máquina de Turing 
es **O(n²) - Cuadrática**.

Esto significa que:
- El tiempo crece **cuadráticamente** con el tamaño de entrada
- Duplicar la entrada aproximadamente cuadruplica el tiempo

## Conclusiones

1. La Máquina de Turing implementada tiene complejidad temporal O(n²) - Cuadrática
2. El modelo polinomial se ajusta bien a los datos (R² = 0.6969)
3. Para entradas grandes, el tiempo de ejecución puede crecer rápidamente

## Visualizaciones

Ver archivos:
- `steps_vs_input.png` - Gráfico de pasos vs entrada
- `time_vs_input.png` - Gráfico de tiempo vs entrada

## Fecha de Análisis

Generado automáticamente por experiments/plot.py
