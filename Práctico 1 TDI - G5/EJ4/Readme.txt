Cálculo de Capacidad de Canal 

Este script calcula la capacidad de un canal utilizando el algoritmo de Blahut-Arimoto, trabajando con matrices de transición
que se leen desde archivos CSV y generando un archivo de resultados con la distribución óptima y la capacidad en bits.

Librerías utilizadas

NumPy: Para manipular matrices y realizar cálculos numéricos, como la normalización de distribuciones 
y el cálculo de la información mutua.

CSV: Para leer y escribir archivos CSV con las probabilidades de transición y los resultados.

OS: Se usa para manejar rutas de archivos y directorios para poder encontrar correctamente los archivos csv.

Instalación
numpy: pip install numpy
OS y CSV: La libreria os y csv se instalan al instalar python (son parte de la biblioteca estandar de python).
