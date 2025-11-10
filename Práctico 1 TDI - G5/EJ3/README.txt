Calculadora de Entropia y Redundancia

Descripcion
Este programa analiza archivos calculando su entropia y redundancia, 
Sirve para estimar que tan aleatorios o compresibles son los datos de un archivo.

El programa puede:

Calcular entropia independiente considerando cada byte por separado

Calcular entropia dependiente de orden 1 y 2 considerando dependencias entre bytes

Generar un reporte con los resultados e interpretacion

Archivos del ejercicio
Calc_Entropia.py Programa principal con la calculadora de entropia

Librerias utilizadas
El codigo solo usa librerias estandar de Python, por lo que no se requiere instalar nada adicional
os Para manejar archivos y rutas
math Para operaciones matematicas logaritmos en base 2
collections.Counter Para contar frecuencias de simbolos


Ejecucion
Para ejecutar el programa abrir una terminal, ubicarse en la carpeta del archivo y escribir
python Calc_Entropia.py
Luego pedira ingresar el nombre de un archivo que debe estar en la misma carpeta

Interpretacion de resultados
Entropia menor a 4 bits Archivo muy compresible texto patrones repetitivos
Entropia entre 4 y 6 bits Compresibilidad media
Entropia mayor a 6 bits Archivo dificil de comprimir datos aleatorios o encriptados

