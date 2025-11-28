"""
Sistema de Control de Error Reed-Solomon con Entrelazado
GF(16) generado por f(x) = X^4 + X + 1
Parámetros: N=15, K=9 (bytes de 4 bits), t=3 (corrige hasta 3 errores)
"""

import os
import sys

# ============================================================================
# ARITMÉTICA DE CAMPO GALOIS GF(16)
# ============================================================================

class GF16:
    """Implementación de GF(16) con polinomio primitivo f(x) = X^4 + X + 1"""
    
    def __init__(self):
        self.tabla_multiplicacion = [[0] * 16 for _ in range(16)]
        self.tabla_division = [[0] * 16 for _ in range(16)]
        self.tabla_exponencial = [0] * 32
        self.tabla_logaritmica = [0] * 16
        self._construir_tablas()
    
    def _construir_tablas(self):
        self.tabla_exponencial[0] = 1
        for i in range(1, 15):
            anterior = self.tabla_exponencial[i-1]
            siguiente_valor = (anterior << 1) & 0x0F
            if anterior & 0x08:
                siguiente_valor ^= 0x03
            self.tabla_exponencial[i] = siguiente_valor
        
        self.tabla_exponencial[15] = 1
        for i in range(16, 32):
            self.tabla_exponencial[i] = self.tabla_exponencial[i % 15]
        
        self.tabla_logaritmica[0] = -1
        for i in range(15):
            self.tabla_logaritmica[self.tabla_exponencial[i]] = i
        
        for a in range(16):
            for b in range(16):
                if a == 0 or b == 0:
                    self.tabla_multiplicacion[a][b] = 0
                else:
                    suma_log = (self.tabla_logaritmica[a] + self.tabla_logaritmica[b]) % 15
                    self.tabla_multiplicacion[a][b] = self.tabla_exponencial[suma_log]
        
        for a in range(16):
            for b in range(1, 16):
                diferencia_log = (self.tabla_logaritmica[a] - self.tabla_logaritmica[b] + 15) % 15
                self.tabla_division[a][b] = self.tabla_exponencial[diferencia_log] if a != 0 else 0
    
    def sumar(self, a, b): return a ^ b
    def multiplicar(self, a, b): return self.tabla_multiplicacion[a][b]
    def dividir(self, a, b):
        if b == 0: raise ValueError("División por cero")
        return self.tabla_division[a][b]

gf16 = GF16()


# ============================================================================
# CODIFICACIÓN REED-SOLOMON
# ============================================================================

class ReedSolomon:
    def __init__(self, n=15, k=9):
        self.n = n
        self.k = k
        self.t = (n - k) // 2
        self.polinomio_generador = self._construir_polinomio_generador()
    
    def _construir_polinomio_generador(self):
        g = [1]
        for i in range(1, 2 * self.t + 1):
            alpha_i = gf16.tabla_exponencial[i % 15]
            nuevo_g = [0] * (len(g) + 1)
            for j in range(len(g)):
                nuevo_g[j + 1] = g[j]
            for j in range(len(g)):
                nuevo_g[j] = gf16.sumar(nuevo_g[j], gf16.multiplicar(g[j], alpha_i))
            g = nuevo_g
        return g
    
    def codificar(self, mensaje):
        if len(mensaje) != self.k:
            raise ValueError(f"El mensaje debe tener exactamente {self.k} símbolos")
        
        mensaje_entero = [int(m) if isinstance(m, (int, str)) else ord(m) & 0x0F for m in mensaje]
        polinomio_mensaje = [0] * self.n
        for i in range(self.k):
            polinomio_mensaje[i + (self.n - self.k)] = mensaje_entero[i]
        
        resto = self._modulo_polinomio(polinomio_mensaje, self.polinomio_generador)
        
        palabra_codigo = [0] * self.n
        for i in range(self.k):
            palabra_codigo[i + (self.n - self.k)] = mensaje_entero[i]
        for i in range(self.n - self.k):
            palabra_codigo[i] = resto[i]
        
        return palabra_codigo
    
    def _modulo_polinomio(self, dividendo, divisor):
        resto = list(dividendo)
        grado_divisor = len(divisor) - 1
        while grado_divisor >= 0 and divisor[grado_divisor] == 0:
            grado_divisor -= 1
        if grado_divisor < 0: raise ValueError("Divisor no puede ser cero")
        
        while True:
            grado_resto = len(resto) - 1
            while grado_resto >= 0 and resto[grado_resto] == 0:
                grado_resto -= 1
            if grado_resto < grado_divisor: break
            
            factor = gf16.dividir(resto[grado_resto], divisor[grado_divisor])
            desplazamiento = grado_resto - grado_divisor
            for i in range(grado_divisor + 1):
                if divisor[i] != 0:
                    posicion = desplazamiento + i
                    if posicion < len(resto):
                        resto[posicion] = gf16.sumar(resto[posicion], gf16.multiplicar(factor, divisor[i]))
        
        resultado = [0] * (self.n - self.k)
        for i in range(min(len(resto), len(resultado))):
            resultado[i] = resto[i]
        return resultado


# ============================================================================
# ENTRELAZADO (INTERLEAVING)
# ============================================================================

def entrelazar_codigos(palabras_codigo):
    """
    Realiza un entrelazado de bloques (Block Interleaving).
    Toma una lista de palabras código (filas) y las lee por columnas.
    
    Entrada: Matriz de [M filas x N columnas] (M palabras de N símbolos)
    Salida:  Lista plana de M*N símbolos ordenados por columna.
    """
    if not palabras_codigo:
        return []
    
    num_palabras = len(palabras_codigo)
    longitud_palabra = len(palabras_codigo[0]) # N = 15
    
    datos_entrelazados = []
    
    # Recorremos por columna (0..14) y luego por fila (0..M)
    # Esto dispersa los símbolos de una misma palabra código a lo largo del archivo
    for j in range(longitud_palabra):
        for i in range(num_palabras):
            datos_entrelazados.append(palabras_codigo[i][j])
            
    return datos_entrelazados


# ============================================================================
# PROCESAMIENTO DE ARCHIVOS
# ============================================================================

def dividir_byte_en_nibbles(valor_byte):
    nibble_alto = (valor_byte >> 4) & 0x0F
    nibble_bajo = valor_byte & 0x0F
    return nibble_alto, nibble_bajo

def combinar_nibbles_a_byte(nibble_alto, nibble_bajo):
    return ((nibble_alto & 0x0F) << 4) | (nibble_bajo & 0x0F)

def procesar_archivo_a_bloques_rs(datos):
    nibbles = []
    for valor_byte in datos:
        alto, bajo = dividir_byte_en_nibbles(valor_byte)
        nibbles.append(alto)
        nibbles.append(bajo)
    
    bloques_rs = []
    i = 0
    while i < len(nibbles):
        if i + 9 <= len(nibbles):
            bloque = nibbles[i:i+9]
            bloques_rs.append(bloque)
            i += 9
        else:
            bloque = nibbles[i:] + [0] * (9 - (len(nibbles) - i))
            bloques_rs.append(bloque)
            break
    return bloques_rs

def guardar_simbolos_en_archivo(lista_simbolos_planos, ruta_salida):
    """
    Guarda una lista plana de símbolos (0-15) en un archivo binario.
    Cada símbolo se convierte a su representación ASCII ('0'-'9', 'A'-'F').
    """
    datos_salida = []
    for simbolo in lista_simbolos_planos:
        if simbolo < 10:
            datos_salida.append(ord('0') + simbolo)
        else:
            datos_salida.append(ord('A') + simbolo - 10)
            
    with open(ruta_salida, 'wb') as f:
        f.write(bytes(datos_salida))
    return len(datos_salida)

def codificar_archivo_y_obtener_codigos(archivo_entrada):
    """
    Lee y codifica el archivo, retornando la matriz de palabras código.
    """
    print(f"\n=== LEYENDO ARCHIVO: {archivo_entrada} ===")
    with open(archivo_entrada, 'rb') as f:
        datos = f.read()
    
    print(f"Tamaño original: {len(datos)} bytes")
    bloques_rs = procesar_archivo_a_bloques_rs(datos)
    print(f"Bloques a procesar: {len(bloques_rs)}")
    
    rs = ReedSolomon(n=15, k=9)
    palabras_codigo = []
    
    print("Codificando bloques...")
    for i, bloque in enumerate(bloques_rs):
        palabra = rs.codificar(bloque)
        palabras_codigo.append(palabra)
        
    return palabras_codigo, len(datos)

# ============================================================================
# UTILIDADES DE RUTA
# ============================================================================

def obtener_carpeta_script():
    ruta_script = os.path.abspath(__file__)
    return os.path.dirname(ruta_script)

def listar_archivos_txt():
    carpeta = obtener_carpeta_script()
    archivos = []
    try:
        for archivo in os.listdir(carpeta):
            ruta = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta) and archivo.lower().endswith('.txt'):
                if archivo not in ['A2.txt', 'A3.txt', 'A1_decodificado.txt']:
                    archivos.append(archivo)
    except Exception: pass
    return sorted(archivos)

def seleccionar_archivo():
    carpeta = obtener_carpeta_script()
    archivos = listar_archivos_txt()
    
    if not archivos:
        print("\n⚠ No se encontraron archivos de entrada.")
        print("  Creando A1.txt de prueba...")
        ruta = os.path.join(carpeta, "A1.txt")
        with open(ruta, 'w') as f: f.write("TEORIADELAINFORMACION")
        return ruta
    
    print("\n--- SELECCIONAR ARCHIVO DE ENTRADA ---")
    for i, arch in enumerate(archivos, 1):
        print(f" [{i}] {arch}")
    print(" [0] A1.txt (Default)")
    
    sel = input("\nOpción: ").strip()
    if sel == "" or sel == "0":
        ruta = os.path.join(carpeta, "A1.txt")
        if not os.path.exists(ruta):
            with open(ruta, 'w') as f: f.write("TEORIADELAINFORMACION")
        return ruta
        
    try:
        idx = int(sel) - 1
        if 0 <= idx < len(archivos):
            return os.path.join(carpeta, archivos[idx])
    except: pass
    return None

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SISTEMA DE CODIFICACIÓN RS(15,9) + ENTRELAZADO")
    print("=" * 70)
    
    archivo_entrada = seleccionar_archivo()
    if not archivo_entrada: sys.exit()
    
    carpeta = obtener_carpeta_script()
    archivo_A2 = os.path.join(carpeta, "A2.txt")
    archivo_A3 = os.path.join(carpeta, "A3.txt")
    
    try:
        # 1. CODIFICACIÓN
        palabras_codigo, len_orig = codificar_archivo_y_obtener_codigos(archivo_entrada)
        
        # Guardar A2 (Secuencial: Palabra1, Palabra2, ...)
        lista_plana_A2 = [simbolo for palabra in palabras_codigo for simbolo in palabra]
        size_A2 = guardar_simbolos_en_archivo(lista_plana_A2, archivo_A2)
        
        print(f"\n[A2] Archivo codificado (secuencial) generado: {os.path.basename(archivo_A2)}")
        print(f"     Tamaño: {size_A2} bytes | Redundancia: {size_A2/len_orig:.2f}x")

        # 2. ENTRELAZADO
        print(f"\n[A3] Generando entrelazado de códigos...")
        lista_plana_A3 = entrelazar_codigos(palabras_codigo)
        
        # Guardar A3 (Entrelazado: Columna 0 de todas, Columna 1 de todas...)
        size_A3 = guardar_simbolos_en_archivo(lista_plana_A3, archivo_A3)
        
        print(f"[A3] Archivo entrelazado generado: {os.path.basename(archivo_A3)}")
        print(f"     Tamaño: {size_A3} bytes ")
        
        # Verificación visual rápida (primeros bytes)
        print("\n--- Comparación Visual (Primeros 30 chars) ---")
        with open(archivo_A2, 'r') as f: print(f"A2 (Secuencial): {f.read(30)}...")
        with open(archivo_A3, 'r') as f: print(f"A3 (Entrelazado):{f.read(30)}...")
        
        print("\nProceso finalizado exitosamente.")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()