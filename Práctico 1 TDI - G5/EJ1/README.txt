# Análisis de Archivos WAV

Este script permite validar y leer archivos en formato **WAV**.  
El programa verifica que el archivo tenga el formato correcto y muestra la información de su cabecera, incluyendo datos como frecuencia de muestreo, número de canales, duración estimada y demás parámetros técnicos.

---

Librerías utilizadas

os: Se utiliza para gestionar rutas de archivos y directorios de manera independiente del sistema operativo. Permite obtener la ruta del directorio actual, construir rutas completas, y verificar si un archivo existe.  

struct: Se utiliza para interpretar bytes como valores binarios. Permite decodificar correctamente los datos de la cabecera WAV (como enteros, tamaños y frecuencias).

---

Instalación

Ambas librerías (`os` y `struct`) forman parte de la biblioteca estándar de Python.  
Se instalan automáticamente al instalar Python, por lo que no es necesario agregar nada extra.
