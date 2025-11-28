"""
Sistema de Control de Error Reed-Solomon
GF(16) generado por f(x) = X^4 + X + 1
Parámetros: N=15, K=9 (bytes de 4 bits), t=3 (corrige hasta 3 errores)
"""

import os
import random
import struct
import sys


# ============================================================================
# ARITMÉTICA DE CAMPO GALOIS GF(16)
# ============================================================================

class GF16:
    """
    Implementación de GF(16) con polinomio primitivo f(x) = X^4 + X + 1
    """
    
    # Polinomio primitivo: x^4 + x + 1 = 0, entonces x^4 = x + 1
    # Representación: 0b10011 = 19 (pero trabajamos con 4 bits, así que 0b10011 mod 16 = 3)
    # En realidad, para GF(16), el polinomio es x^4 + x + 1 = 0
    # Esto significa que α^4 = α + 1, donde α es el elemento primitivo
    
    def __init__(self):
        # Tabla de multiplicación precalculada para GF(16)
        # Usando polinomio primitivo x^4 + x + 1 (binario: 10011)
        self.tabla_multiplicacion = [[0] * 16 for _ in range(16)]
        self.tabla_division = [[0] * 16 for _ in range(16)]
        self.tabla_exponencial = [0] * 32  # Tabla exponencial (α^i)
        self.tabla_logaritmica = [0] * 16  # Tabla logarítmica (log_α(i))
        
        self._construir_tablas()
    
    def _construir_tablas(self):
        """Construye las tablas de multiplicación y exponenciales para GF(16)"""
        # Polinomio primitivo: x^4 + x + 1 = 0
        # Esto significa: x^4 = x + 1
        # En representación binaria de 4 bits: cuando x^4 aparece, lo reemplazamos con x + 1
        # El polinomio reducido es: 0x03 (00011) = x + 1
        
        # Inicializar tabla_exponencial: tabla_exponencial[i] = α^i
        self.tabla_exponencial[0] = 1  # α^0 = 1
        for i in range(1, 15):
            # Multiplicar por α (shift left y aplicar polinomio primitivo si necesario)
            anterior = self.tabla_exponencial[i-1]
            siguiente_valor = (anterior << 1) & 0x0F
            if anterior & 0x08:  # Si el bit más significativo (x^3) es 1, necesitamos reducir
                # Aplicar x^4 = x + 1, que es XOR con 0x03 (00011)
                siguiente_valor ^= 0x03
            self.tabla_exponencial[i] = siguiente_valor
        
        # Completar el ciclo (α^15 = 1)
        self.tabla_exponencial[15] = 1
        for i in range(16, 32):
            self.tabla_exponencial[i] = self.tabla_exponencial[i % 15]
        
        # Construir tabla_logaritmica: tabla_logaritmica[tabla_exponencial[i]] = i
        self.tabla_logaritmica[0] = -1  # log(0) no está definido
        for i in range(15):
            self.tabla_logaritmica[self.tabla_exponencial[i]] = i
        
        # Construir tabla de multiplicación
        for a in range(16):
            for b in range(16):
                if a == 0 or b == 0:
                    self.tabla_multiplicacion[a][b] = 0
                else:
                    # a * b = α^(log(a) + log(b))
                    suma_log = (self.tabla_logaritmica[a] + self.tabla_logaritmica[b]) % 15
                    self.tabla_multiplicacion[a][b] = self.tabla_exponencial[suma_log]
        
        # Construir tabla de división
        for a in range(16):
            for b in range(1, 16):  # No dividir por 0
                # a / b = α^(log(a) - log(b))
                diferencia_log = (self.tabla_logaritmica[a] - self.tabla_logaritmica[b] + 15) % 15
                self.tabla_division[a][b] = self.tabla_exponencial[diferencia_log] if a != 0 else 0
    
    def sumar(self, a, b):
        """Suma en GF(16) (XOR)"""
        return a ^ b
    
    def multiplicar(self, a, b):
        """Multiplicación en GF(16)"""
        return self.tabla_multiplicacion[a][b]
    
    def dividir(self, a, b):
        """División en GF(16)"""
        if b == 0:
            raise ValueError("División por cero")
        return self.tabla_division[a][b]
    
    def potencia(self, a, n):
        """Potenciación en GF(16): a^n"""
        if a == 0:
            return 0
        if n == 0:
            return 1
        log_a = self.tabla_logaritmica[a]
        resultado_log = (log_a * n) % 15
        return self.tabla_exponencial[resultado_log]


# Instancia global de GF(16)
gf16 = GF16()


# ============================================================================
# CODIFICACIÓN REED-SOLOMON
# ============================================================================

class ReedSolomon:
    """
    Codificador/Decodificador Reed-Solomon
    Parámetros: N=15, K=9, t=3 (corrige hasta 3 errores)
    """
    
    def __init__(self, n=15, k=9):
        self.n = n  # Longitud del código
        self.k = k  # Longitud del mensaje
        self.t = (n - k) // 2  # Capacidad de corrección (t=3)
        self.polinomio_generador = self._construir_polinomio_generador()
    
    def _construir_polinomio_generador(self):
        """
        Construye el polinomio generador g(x) = ∏(x - α^i) para i = 1, 2, ..., 2t
        Para t=3: g(x) = (x-α)(x-α^2)...(x-α^6)
        """
        # g(x) = (x - α)(x - α^2)...(x - α^6)
        # Empezamos con g(x) = 1
        g = [1]  # Representa 1 (coeficiente de x^0)
        
        # Multiplicar por (x - α^i) para i = 1, 2, ..., 6
        for i in range(1, 2 * self.t + 1):
            # (x - α^i) = x - α^i
            # En GF(16), -α^i = α^(15-i) ya que α^15 = 1
            alpha_i = gf16.tabla_exponencial[i % 15]
            # Multiplicar g(x) por (x - α^i)
            # g(x) * (x - α^i) = g(x) * x - g(x) * α^i
            nuevo_g = [0] * (len(g) + 1)
            # Primero: g(x) * x (shift hacia la izquierda)
            for j in range(len(g)):
                nuevo_g[j + 1] = g[j]
            # Segundo: restar α^i * g(x)
            for j in range(len(g)):
                nuevo_g[j] = gf16.sumar(nuevo_g[j], gf16.multiplicar(g[j], alpha_i))
            g = nuevo_g
        
        return g
    
    def codificar(self, mensaje):
        """
        Codifica un mensaje de K símbolos en un código de N símbolos
        Codificación sistemática: [mensaje | síndromes]
        """
        if len(mensaje) != self.k:
            raise ValueError(f"El mensaje debe tener exactamente {self.k} símbolos")
        
        # Convertir mensaje a lista de enteros (si no lo es)
        mensaje_entero = [int(m) if isinstance(m, (int, str)) else ord(m) & 0x0F for m in mensaje]
        
        # Crear polinomio mensaje: m(x) = m[0] + m[1]*x + ... + m[k-1]*x^(k-1)
        # Pero necesitamos m(x) * x^(n-k) para la codificación sistemática
        polinomio_mensaje = [0] * self.n
        for i in range(self.k):
            polinomio_mensaje[i + (self.n - self.k)] = mensaje_entero[i]
        
        # Calcular resto de la división: r(x) = m(x) * x^(n-k) mod g(x)
        resto = self._modulo_polinomio(polinomio_mensaje, self.polinomio_generador)
        
        # Código sistemático: [mensaje | resto]
        palabra_codigo = [0] * self.n
        for i in range(self.k):
            palabra_codigo[i + (self.n - self.k)] = mensaje_entero[i]
        for i in range(self.n - self.k):
            palabra_codigo[i] = resto[i]
        
        return palabra_codigo
    
    def _modulo_polinomio(self, dividendo, divisor):
        """Calcula el resto de la división polinomial en GF(16)"""
        # Implementación de división polinomial
        resto = list(dividendo)
        grado_divisor = len(divisor) - 1
        
        # Encontrar el grado real del divisor (ignorar ceros al inicio)
        while grado_divisor >= 0 and divisor[grado_divisor] == 0:
            grado_divisor -= 1
        
        if grado_divisor < 0:
            raise ValueError("Divisor no puede ser cero")
        
        # División larga
        while True:
            # Encontrar el grado del resto
            grado_resto = len(resto) - 1
            while grado_resto >= 0 and resto[grado_resto] == 0:
                grado_resto -= 1
            
            # Si el grado del resto es menor que el del divisor, terminamos
            if grado_resto < grado_divisor:
                break
            
            # Calcular factor de multiplicación
            factor = gf16.dividir(resto[grado_resto], divisor[grado_divisor])
            
            # Restar (factor * divisor) del dividendo
            desplazamiento = grado_resto - grado_divisor
            for i in range(grado_divisor + 1):
                if divisor[i] != 0:
                    posicion = desplazamiento + i
                    if posicion < len(resto):
                        resto[posicion] = gf16.sumar(resto[posicion], gf16.multiplicar(factor, divisor[i]))
        
        # El resto tiene grado menor que el divisor
        # Asegurarnos de que tenga la longitud correcta
        resultado = [0] * (self.n - self.k)
        for i in range(min(len(resto), len(resultado))):
            resultado[i] = resto[i]
        
        return resultado
    
    
   

# ============================================================================
# PROCESAMIENTO DE ARCHIVOS
# ============================================================================

def dividir_byte_en_nibbles(valor_byte):
    """Divide un byte (8 bits) en dos nibbles (4 bits cada uno)"""
    nibble_alto = (valor_byte >> 4) & 0x0F
    nibble_bajo = valor_byte & 0x0F
    return nibble_alto, nibble_bajo


def combinar_nibbles_a_byte(nibble_alto, nibble_bajo):
    """Combina dos nibbles (4 bits) en un byte (8 bits)"""
    return ((nibble_alto & 0x0F) << 4) | (nibble_bajo & 0x0F)


def procesar_archivo_a_bloques_rs(datos):
    """
    Procesa los datos del archivo según la estrategia especificada:
    - Cada byte ASCII se divide en dos nibbles (4 bits)
    - Cada 5 bytes ASCII (10 nibbles) se agrupan en:
      * Primer bloque RS: primeros 9 nibbles (4.5 bytes)
      * Segundo bloque RS: último nibble del 5to byte + siguientes 4 bytes (9 nibbles)
    - Por cada 9 bytes ASCII originales, se generan 2 palabras válidas RS
    """
    nibbles = []
    for valor_byte in datos:
        alto, bajo = dividir_byte_en_nibbles(valor_byte)
        nibbles.append(alto)
        nibbles.append(bajo)
    
    bloques_rs = []
    i = 0
    while i < len(nibbles):
        # Tomar grupos de 9 nibbles para cada palabra RS
        if i + 9 <= len(nibbles):
            bloque = nibbles[i:i+9]
            bloques_rs.append(bloque)
            i += 9
        else:
            # Rellenar con ceros si no hay suficientes nibbles
            bloque = nibbles[i:] + [0] * (9 - (len(nibbles) - i))
            bloques_rs.append(bloque)
            break
    
    return bloques_rs


def procesar_bloques_rs_a_archivo(bloques_rs):
    """
    Convierte bloques RS decodificados de vuelta a bytes ASCII
    """
    nibbles = []
    for bloque in bloques_rs:
        # Cada bloque tiene 9 nibbles (solo tomamos los primeros 9, ignorando padding)
        nibbles.extend(bloque[:9])
    
    # Combinar nibbles en bytes
    datos_bytes = []
    for i in range(0, len(nibbles) - 1, 2):
        valor_byte = combinar_nibbles_a_byte(nibbles[i], nibbles[i+1])
        datos_bytes.append(valor_byte)
    
    # Si hay un nibble suelto al final, lo descartamos (era padding)
    return bytes(datos_bytes)


def codificar_archivo(archivo_entrada, archivo_salida):
    """
    Codifica un archivo ASCII usando Reed-Solomon
    """
    print(f"\n=== CODIFICANDO ARCHIVO: {archivo_entrada} ===")
    
    # Leer archivo
    with open(archivo_entrada, 'rb') as f:
        datos = f.read()
    
    print(f"Tamaño original: {len(datos)} bytes")
    
    # Procesar a bloques RS
    bloques_rs = procesar_archivo_a_bloques_rs(datos)
    print(f"Número de bloques RS (palabras válidas): {len(bloques_rs)}")
    
    # Codificar cada bloque
    rs = ReedSolomon(n=15, k=9)
    palabras_codigo = []
    for i, bloque in enumerate(bloques_rs):
        palabra_codigo = rs.codificar(bloque)
        palabras_codigo.append(palabra_codigo)
        if i < 3:  # Mostrar primeros 3 para ejemplo
            print(f"  Bloque {i+1}: {bloque[:5]}... -> palabra código de {len(palabra_codigo)} símbolos")
    
    # Convertir palabras código a bytes para guardar
    # Cada símbolo de 4 bits se guarda como un byte (ASCII)
    datos_salida = []
    for palabra in palabras_codigo:
        for simbolo in palabra:
            # Guardar como carácter ASCII (0-15 -> '0'-'9', 'A'-'F')
            if simbolo < 10:
                datos_salida.append(ord('0') + simbolo)
            else:
                datos_salida.append(ord('A') + simbolo - 10)
    
    # Guardar archivo codificado
    with open(archivo_salida, 'wb') as f:
        f.write(bytes(datos_salida))
    
    print(f"Archivo codificado guardado: {archivo_salida}")
    print(f"Tamaño codificado: {len(datos_salida)} bytes")
    print(f"Redundancia: {len(datos_salida) / len(datos):.2f}x")
    
    return palabras_codigo




# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def obtener_carpeta_script():
    """Obtiene la ruta de la carpeta donde está el script"""
    # Obtener la ruta absoluta del archivo del script
    ruta_script = os.path.abspath(__file__)
    # Obtener el directorio donde está el script
    carpeta_script = os.path.dirname(ruta_script)
    return carpeta_script


def listar_archivos_txt():
    """Lista todos los archivos .txt en la carpeta del script (Reed-Solomon)"""
    carpeta_script = obtener_carpeta_script()
    archivos = []
    
    try:
        for archivo in os.listdir(carpeta_script):
            ruta_completa = os.path.join(carpeta_script, archivo)
            if os.path.isfile(ruta_completa) and archivo.lower().endswith('.txt'):
                # Excluir archivos de salida
                if archivo not in ['A2.txt', 'A3.txt', 'A1_decodificado.txt']:
                    archivos.append(archivo)
    except Exception as e:
        print(f"⚠ Error al listar archivos: {e}")
    
    return sorted(archivos)


def seleccionar_archivo():
    """Permite al usuario seleccionar un archivo de la carpeta del script"""
    carpeta_script = obtener_carpeta_script()
    archivos = listar_archivos_txt()
    
    if len(archivos) == 0:
        print("\n⚠ No se encontraron archivos .txt en la carpeta Reed-Solomon-Codificacion")
        print("   Creando archivo A1.txt con 'TEORIADELAINFORMACION'...")
        ruta_a1 = os.path.join(carpeta_script, "A1.txt")
        test_content = "TEORIADELAINFORMACION"
        with open(ruta_a1, 'w', encoding='ascii') as f:
            f.write(test_content)
        print(f"   Archivo A1.txt creado con {len(test_content)} caracteres")
        return ruta_a1
    
    print("\n" + "=" * 70)
    print("ARCHIVOS DISPONIBLES PARA CODIFICAR (carpeta Reed-Solomon-Codificacion):")
    print("=" * 70)
    for i, archivo in enumerate(archivos, 1):
        try:
            ruta_completa = os.path.join(carpeta_script, archivo)
            tamaño = os.path.getsize(ruta_completa)
            print(f"  [{i}] {archivo} ({tamaño} bytes)")
        except:
            print(f"  [{i}] {archivo}")
    
    print(f"  [0] Usar A1.txt (por defecto)")
    print("=" * 70)
    
    while True:
        try:
            seleccion = input("\nSeleccione el número del archivo a codificar (o Enter para A1.txt): ").strip()
            
            if seleccion == "" or seleccion == "0":
                # Usar A1.txt por defecto
                if "A1.txt" in archivos:
                    return os.path.join(carpeta_script, "A1.txt")
                else:
                    print("⚠ A1.txt no existe. Creando archivo con 'TEORIADELAINFORMACION'...")
                    ruta_a1 = os.path.join(carpeta_script, "A1.txt")
                    test_content = "TEORIADELAINFORMACION"
                    with open(ruta_a1, 'w', encoding='ascii') as f:
                        f.write(test_content)
                    print(f"   Archivo A1.txt creado con {len(test_content)} caracteres")
                    return ruta_a1
            
            indice = int(seleccion)
            if 1 <= indice <= len(archivos):
                return os.path.join(carpeta_script, archivos[indice - 1])
            else:
                print(f"⚠ Por favor, seleccione un número entre 1 y {len(archivos)}")
        except ValueError:
            print("⚠ Por favor, ingrese un número válido")
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario")
            return None


if __name__ == "__main__":
    """
    Función principal que solo realiza la codificación:
    1. Permite seleccionar un archivo de la carpeta
    2. Codifica el archivo usando Reed-Solomon
    3. Genera A2.txt con el archivo codificado
    """
    print("=" * 70)
    print("SISTEMA DE CODIFICACIÓN REED-SOLOMON")
    print("GF(16), N=15, K=9, t=3")
    print("=" * 70)
    
    # Seleccionar archivo a codificar
    archivo_entrada = seleccionar_archivo()
    
    if archivo_entrada is None:
        sys.exit() 
    
    # El archivo de salida también va en la carpeta del script
    carpeta_script = obtener_carpeta_script()
    archivo_salida = os.path.join(carpeta_script, "A2.txt")
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(archivo_entrada):
            print(f"\n Error: El archivo '{archivo_entrada}' no existe")
            sys.exit() 
        
        # Obtener solo el nombre del archivo para mostrar
        nombre_archivo_entrada = os.path.basename(archivo_entrada)
        nombre_archivo_salida = os.path.basename(archivo_salida)
        
        # Leer archivo
        print(f"\n[1] Leyendo archivo: {nombre_archivo_entrada}")
        with open(archivo_entrada, 'rb') as f:
            original_data = f.read()
        print(f"    Tamaño: {len(original_data)} bytes")
        
        rs = ReedSolomon()

        print("\nPolinomio generador g(x):", rs.polinomio_generador)

        # Codificar archivo
        print(f"\n[2] Codificando archivo con Reed-Solomon...")
        palabras_codigo = codificar_archivo(archivo_entrada, archivo_salida)
        
        print("\n" + "=" * 70)
        print("✓ CODIFICACIÓN COMPLETADA")
        print("=" * 70)
        print(f"\nArchivos (en carpeta Reed-Solomon):")
        print(f"  Entrada:  {nombre_archivo_entrada} ({len(original_data)} bytes)")
        print(f"  Salida:   {nombre_archivo_salida} ({os.path.getsize(archivo_salida)} bytes)")
        print(f"  Redundancia: {os.path.getsize(archivo_salida) / len(original_data):.2f}x")
        print(f"\nEl archivo '{nombre_archivo_salida}' ha sido generado correctamente en la carpeta Reed-Solomon.")
        
    except FileNotFoundError as e:
        print(f"\n Error: No se encontró el archivo {e.filename}")
    except PermissionError as e:
        print(f"\n Error: No se tiene permiso para acceder al archivo {e.filename}")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        import traceback
        traceback.print_exc()




