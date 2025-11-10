Comunicación Cliente-Servidor con Compresión de Archivos

Este proyecto implementa un sistema de comunicación entre procesos usando sockets TCP en Python.
Un cliente lee un archivo de texto, lo comprime utilizando tres algoritmos distintos (Huffman, Shannon y Fano)
y envía las versiones comprimidas al servidor.
El servidor recibe los datos, los descomprime usando las tablas enviadas y guarda el resultado en archivos de texto separados.

De esta forma se muestra cómo se pueden usar distintos métodos de compresión sin pérdida en un entorno de comunicación
cliente-servidor.

Librerías utilizadas

socket: Usada tanto en el cliente como en el servidor.
Permite la comunicación mediante sockets TCP para enviar y recibir datos entre dos procesos en la red.

json: Usada para enviar y recibir la tabla de códigos de compresión (Huffman, Shannon–Fano o Fano).
Convierte los diccionarios de Python en cadenas de texto (JSON) para poder transmitirlos fácilmente por la red.

heapq: Usada en la implementación del algoritmo de Huffman.
Permite manejar una cola de prioridad (min-heap) para construir el árbol de Huffman de forma eficiente.

collections.Counter: Usada en los algoritmos de compresión.
Facilita el cálculo de las frecuencias de los símbolos en el texto original.

collections.namedtuple: Usada en la implementación de Huffman.
Define una estructura simple (Nodo) para representar los nodos del árbol binario de Huffman.

OS: Se utiliza para gestionar rutas de archivos y directorios de manera independiente del sistema operativo. 
Permite obtener la ruta del directorio actual y construir las rutas completas de los archivos donde se guardan y leen los registros.

Instalación

Todas las librerías usadas (socket, json, heapq, collections, os) forman parte de la biblioteca estándar de Python.
