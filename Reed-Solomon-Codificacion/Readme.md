==============================================================================
DOCUMENTACIÓN DEL CODIFICADOR REED-SOLOMON Y ENTRELAZADO (GRUPO 5)
==============================================================================

1. DESCRIPCIÓN DEL SISTEMA
------------------------------------------------------------------------------
Este software implementa la etapa de transmisión de un sistema de comunicaciones
robusto, diseñado para cumplir con las consignas del Trabajo Práctico de 
Teoría de la Información.

El programa realiza dos funciones principales de protección de datos:
1. Codificación de Canal (Reed-Solomon): Para corregir errores aleatorios.
2. Entrelazado (Interleaving): Para corregir errores en ráfaga.

PARÁMETROS DEL SISTEMA:
- Campo Finito: GF(16) generado por el polinomio f(x) = X^4 + X + 1.
- Código RS: (15, 9).
  - N = 15 (Símbolos totales por palabra).
  - K = 9  (Símbolos de información por palabra).
  - t = 3  (Capacidad de corrección: hasta 3 símbolos erróneos por palabra).
- Símbolos: Nibbles de 4 bits (0-15).

------------------------------------------------------------------------------
2. FUNCIONAMIENTO PASO A PASO
------------------------------------------------------------------------------
El script ejecuta automáticamente el siguiente flujo de trabajo:

PASO A: Lectura y Preparación
- Lee el archivo de entrada (por defecto "A1.txt").
- Divide cada byte (8 bits) en dos nibbles (4 bits) para trabajar en GF(16).

PASO B: Codificación Reed-Solomon (Generación de A2)
- Agrupa los nibbles en bloques de 9 (información).
- Calcula 6 símbolos de paridad mediante el polinomio generador.
- Genera una secuencia lineal de palabras código.
- Salida: "A2.txt" (Archivo codificado secuencialmente).

PASO C: Entrelazado de Bloques (Generación de A3)
- Toma las palabras código generadas en el paso anterior.
- Aplica un entrelazado matricial (escribe por filas, lee por columnas).
- Objetivo: Dispersar los errores. Si una ráfaga de ruido corrompe varios
  bytes seguidos en el canal, al desentrelazar en el receptor, esos errores
  se distribuirán entre muchas palabras código diferentes, permitiendo que
  el decodificador RS los corrija individualmente.
- Salida: "A3.txt" (Archivo final listo para transmisión).

------------------------------------------------------------------------------
3. LIBRERÍAS Y REQUISITOS
------------------------------------------------------------------------------
Este software ha sido desarrollado utilizando ÚNICAMENTE la Biblioteca Estándar
de Python para garantizar la máxima compatibilidad y facilidad de uso.

- NO requiere instalación de librerías externas (no hace falta pip install).
- Librerías importadas:
  1. os: Manejo de rutas y sistema de archivos.
  2. sys: Control de ejecución y argumentos.
  3. traceback: Diagnóstico de errores detallado.

Requisito único: Tener instalado Python 3.x.

------------------------------------------------------------------------------
4. INSTRUCCIONES DE USO
------------------------------------------------------------------------------
1. Ubicación:
   Asegúrese de que el script .py y el archivo de texto a codificar (ej: "A1.txt")
   estén en la misma carpeta.

2. Ejecución:
   Abra una terminal/consola en esa carpeta y ejecute:

   python Reed-Solomon-Codificacion.py

3. Interacción:
   - El programa buscará automáticamente archivos .txt en la carpeta.
   - Seleccione el archivo deseado del menú (o presione Enter para "A1.txt").

4. Resultados:
   El programa creará (o sobrescribirá) dos archivos en la misma carpeta:
   - A2.txt: El archivo con la codificación RS pura.
   - A3.txt: El archivo final con la codificación RS + Entrelazado.

==============================================================================
