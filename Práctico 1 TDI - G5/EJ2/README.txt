# Análisis de Archivos BMP

Este script permite validar y leer archivos en formato BMP.  
El programa verifica que el archivo tenga el formato correcto y muestra la información de su cabecera, incluyendo tamaño, dimensiones, compresión, profundidad de color y otros parámetros técnicos.

---

Librerías utilizadas

os: Se utiliza para gestionar rutas de archivos y directorios de manera independiente del sistema operativo. Permite obtener la ruta del directorio actual, construir rutas completas, y verificar si un archivo existe.  

struct: Se utiliza para interpretar bytes como valores binarios. Permite decodificar correctamente los datos de la cabecera BMP (como enteros, tamaños y propiedades de la imagen).

---

Instalación

Ambas librerías (`os` y `struct`) forman parte de la biblioteca estándar de Python.  
Se instalan automáticamente al instalar Python, por lo que no es necesario agregar nada extra.
 

 
