import socket
import heapq
import json
from collections import Counter, namedtuple
import os

# ======== HUFFMAN =========
class Nodo(namedtuple("Nodo", ["simbolo", "izq", "der"])):
    def __lt__(self, otro):
        return False

def construir_arbol(frecuencias):
    heap = [[peso, Nodo(simbolo, None, None)] for simbolo, peso in frecuencias.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        peso1, nodo1 = heapq.heappop(heap)
        peso2, nodo2 = heapq.heappop(heap)
        nuevo = Nodo(None, nodo1, nodo2)
        heapq.heappush(heap, [peso1 + peso2, nuevo])
    return heap[0][1]

def generar_codigos_huffman(nodo, prefijo="", codigo={}):
    if nodo.simbolo is not None:
        codigo[nodo.simbolo] = prefijo
    else:
        generar_codigos_huffman(nodo.izq, prefijo + "0", codigo)
        generar_codigos_huffman(nodo.der, prefijo + "1", codigo)
    return codigo

def comprimir_huffman(texto):
    frecuencias = Counter(texto)
    arbol = construir_arbol(frecuencias)
    codigos = generar_codigos_huffman(arbol)
    comprimido = "".join(codigos[c] for c in texto)
    return comprimido, codigos

# ======== SHANNON =========
def generar_codigos_shannon(frecuencias):
    simbolos = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    codigos = {s: "" for s, _ in simbolos}

    def dividir(simbolos):
        if len(simbolos) <= 1:
            return
        total = sum(p for _, p in simbolos)
        acumulado = 0
        punto = 0
        for i, (_, p) in enumerate(simbolos):
            acumulado += p
            if acumulado >= total / 2:
                punto = i
                break
        izquierda, derecha = simbolos[:punto + 1], simbolos[punto + 1:]
        for s, _ in izquierda:
            codigos[s] += "0"
        for s, _ in derecha:
            codigos[s] += "1"
        dividir(izquierda)
        dividir(derecha)

    dividir(simbolos)
    return codigos

def comprimir_shannon(texto):
    frecuencias = Counter(texto)
    codigos = generar_codigos_shannon(frecuencias)
    comprimido = "".join(codigos[c] for c in texto)
    return comprimido, codigos

# ======== FANO =========
def generar_codigos_fano(simbolos, codigos, prefijo=""):
    # simbolos = lista [(s, p), ...] ordenados por probabilidad descendente
    if len(simbolos) == 1:
        s, _ = simbolos[0]
        codigos[s] = prefijo if prefijo else "0"
        return

    total = sum(p for _, p in simbolos)
    acumulado = 0
    punto = 0
    for i, (_, p) in enumerate(simbolos):
        acumulado += p
        if acumulado >= total / 2:
            punto = i
            break

    izquierda, derecha = simbolos[:punto + 1], simbolos[punto + 1:]
    generar_codigos_fano(izquierda, codigos, prefijo + "0")
    generar_codigos_fano(derecha, codigos, prefijo + "1")

def comprimir_fano(texto):
    frecuencias = Counter(texto)
    simbolos = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    codigos = {}
    generar_codigos_fano(simbolos, codigos)
    comprimido = "".join(codigos[c] for c in texto)
    return comprimido, codigos

# ======== CLIENTE PRINCIPAL =========
if __name__ == "__main__":
    servidor = "127.0.0.1" #Ingresar dirección IP del servidor para hacer la conexión correctamente
    puerto = 5555
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((servidor, puerto))

    # Leer archivo de texto original
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_path = os.path.join(base_dir, "archivo.txt")
    with open(archivo_path, "r", encoding="utf-8") as f:
        texto = f.read().strip()

    # Aplicar los tres métodos
    metodos = {
        "huffman": comprimir_huffman(texto),
        "shannon": comprimir_shannon(texto),
        "fano": comprimir_fano(texto)
    }

    bits_original = len(texto) * 8
    print(f"Texto original: {texto}")
    print(f"Tamaño original (ASCII plano): {bits_original} bits")

    # Enviar cada versión
    for nombre, (comprimido, codigos) in metodos.items():
        bits_comprimido = len(comprimido)
        print(f"[{nombre.upper()}] Comprimido: {bits_comprimido} bits (ratio {bits_original / bits_comprimido:.2f}x)")

        # Enviar algoritmo
        cliente.send(f"{len(nombre):<16}".encode())
        cliente.send(nombre.encode())

        # Enviar tabla
        tabla_json = json.dumps(codigos)
        cliente.send(f"{len(tabla_json):<16}".encode())
        cliente.send(tabla_json.encode())

        # Enviar comprimido
        cliente.send(f"{len(comprimido):<16}".encode())
        cliente.send(comprimido.encode())

    print("[*] Todas las versiones enviadas.")
    cliente.close()

