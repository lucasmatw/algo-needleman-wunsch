# GRASP

## Idea general de la implementación

### Soluciones iniciales
Para generar las soluciones iniciales se calcula el score de 
muchas parejas de sequencias.
En base a esos Score, se seleccionan parejas distribuidas a lo largo de ese Score, con la intención de no sesgar el Score final basándose solo en los mejores.

### Búsqueda local
Se van probando swaps entre secuencias, desde el comienzo y desde el final de la lista.

### Plot
Se grafican los resultados (mejorados) de la búsqueda local

## Ejecución

Ejecutar archivo "main.py"
