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
| 5 | 11111 | 310 | 0.2111 | ACCEPT |
| 6 | 111111 | 561 | 0.3851 | ACCEPT |
| 7 | 1111111 | 1083 | 0.8026 | ACCEPT |
| 8 | 11111111 | 2244 | 1.5188 | ACCEPT |
| 9 | 111111111 | 4987 | 4.2288 | ACCEPT |
| 10 | 1111111111 | 11711 | 11.1556 | ACCEPT |
| 11 | 1111111111... | 28618 | 27.1292 | ACCEPT |
| 12 | 1111111111... | 71785 | 49.6171 | ACCEPT |
| 13 | 1111111111... | 183075 | 173.0427 | ACCEPT |
| 14 | 1111111111... | 471688 | 586.7750 | ACCEPT |
| 15 | 1111111111... | 1222899 | 1508.8852 | ACCEPT |
| 16 | 1111111111... | 3182543 | 5323.1058 | ACCEPT |
| 17 | 1111111111... | 8301614 | 8011.9216 | ACCEPT |
| 18 | 1111111111... | 21685217 | 22244.8034 | ACCEPT |
| 19 | 1111111111... | 56694411 | 141836.0260 | ACCEPT |
| 20 | 1111111111... | 148301948 | 277738.3394 | ACCEPT |

## Análisis de Complejidad

### Regresión Polinomial

Se probaron polinomios de grado 1 a 5 para ajustar los datos empíricos.
El grado seleccionado fue el que ofreció el mejor ajuste (R² más alto).

- **Grado utilizado**: Polinomio de grado 5
- **Coeficiente R²**: 0.993979
- **Complejidad asintótica**: **O(n⁵) - Quíntica**

### Nota sobre Fibonacci

Los números de Fibonacci crecen exponencialmente (~φ^n donde φ≈1.618).
En representación unaria, la MT debe copiar valores que crecen exponencialmente,
resultando en un comportamiento que puede aproximarse con polinomios de alto grado.

### Ecuación del Modelo

```
f(n) = 5.05e+03*n^5 + -2.80e+05*n^4 + 5.99e+06*n^3 + -6.12e+07*n^2 + 2.98e+08*n^1 + -5.51e+08
```

### Interpretación

El análisis empírico sugiere que la complejidad temporal de esta Máquina de Turing 
es **O(n⁵) - Quíntica**.

Esto significa que:
- El tiempo crece **quínticamente** (grado 5) con el tamaño de entrada
- Duplicar la entrada multiplica el tiempo por ~32
- Este alto grado sugiere un comportamiento cercano al exponencial

## Conclusiones

1. La Máquina de Turing implementada tiene complejidad temporal O(n⁵) - Quíntica
2. El modelo polinomial se ajusta bien a los datos (R² = 0.9940)
3. Para entradas grandes, el tiempo de ejecución puede crecer rápidamente

## Visualizaciones

Ver archivos:
- `steps_vs_input.png` - Gráfico de pasos vs entrada
- `time_vs_input.png` - Gráfico de tiempo vs entrada

## Fecha de Análisis

Generado automáticamente por experiments/plot.py
