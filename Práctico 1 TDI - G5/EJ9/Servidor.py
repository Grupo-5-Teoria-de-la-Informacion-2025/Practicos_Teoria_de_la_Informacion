import socket
import json

def descomprimir(comprimido, codigos):
    inv_codigos = {v: k for k, v in codigos.items()}
    actual = ""
    resultado = []
    for bit in comprimido:
        actual += bit
        if actual in inv_codigos:
            resultado.append(inv_codigos[actual])
            actual = ""
    return "".join(resultado)

if __name__ == "__main__":
    ip = "0.0.0.0"
    puerto = 5555
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, puerto))
    servidor.listen(1)
    print(f"[*] Esperando conexiones en {ip}:{puerto}")

    cliente, direccion = servidor.accept()
    print(f"[*] Conexión establecida con {direccion[0]}:{direccion[1]}")

    for _ in range(3):  # Recibir tres métodos
        # Algoritmo
        algoritmo_len = int(cliente.recv(16).decode().strip())
        algoritmo = cliente.recv(algoritmo_len).decode()
        print(f"\n[*] Algoritmo recibido: {algoritmo}")

        # Tabla
        tabla_len = int(cliente.recv(16).decode().strip())
        tabla_json = cliente.recv(tabla_len).decode()
        codigos = json.loads(tabla_json)

        # Comprimido
        comprimido_len = int(cliente.recv(16).decode().strip())
        comprimido = cliente.recv(comprimido_len).decode()

        print(f"[*] Descomprimiendo con {algoritmo}...")
        descomprimido = descomprimir(comprimido, codigos)

        nombre_archivo = f"descomprimido_{algoritmo}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(descomprimido)

        print(f"[*] Resultado guardado en {nombre_archivo}")
        print(f"Texto descomprimido: {descomprimido}")

    cliente.close()
    servidor.close()
