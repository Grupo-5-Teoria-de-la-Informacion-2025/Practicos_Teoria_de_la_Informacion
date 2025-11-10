import os

# Definimos longitudes fijas por campo
LONG_NOMBRE = 30
LONG_DIRECCION = 40
LONG_DNI = 8
LONG_BINARIOS = 8   # 8 campos S/N, uno por carácter

# Campos bivaluados de ejemplo
CAMPOS_BINARIOS = [
    "Estudios primarios",
    "Estudios secundarios",
    "Estudios universitarios",
    "Vivienda propia",
    "Obra social",
    "Trabaja",
    "Casado",
    "Hijos"
]

def formatear_fijo(nombre, direccion, dni, binarios):
    """Devuelve un registro de longitud fija como string."""
    nombre_f = nombre.ljust(LONG_NOMBRE)[:LONG_NOMBRE]
    direccion_f = direccion.ljust(LONG_DIRECCION)[:LONG_DIRECCION]
    dni_f = dni.zfill(LONG_DNI)[:LONG_DNI]
    bin_f = "".join(["S" if b else "N" for b in binarios])
    return nombre_f + direccion_f + dni_f + bin_f

def parsear_fijo(linea):
    """Lee un registro de longitud fija y lo convierte en dict."""
    nombre = linea[:LONG_NOMBRE].strip()
    direccion = linea[LONG_NOMBRE:LONG_NOMBRE+LONG_DIRECCION].strip()
    dni = linea[LONG_NOMBRE+LONG_DIRECCION:LONG_NOMBRE+LONG_DIRECCION+LONG_DNI].strip()
    binarios = linea[-LONG_BINARIOS:]
    binarios = [c == "S" for c in binarios]
    return {"nombre": nombre, "direccion": direccion, "dni": dni, "binarios": binarios}

def guardar_fijo(personas, archivo="fijos.dat"):
    # Obtener la ruta del directorio actual (donde guardar los archivos)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio_actual, archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        for p in personas:
            registro = formatear_fijo(p["nombre"], p["direccion"], p["dni"], p["binarios"])
            f.write(registro + "\n")

def leer_fijo(archivo="fijos.dat"):
    personas = []
    # Obtener la ruta del directorio actual (donde están los archivos)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio_actual, archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            personas.append(parsear_fijo(linea.strip()))
    return personas

def guardar_variable(personas, archivo="variable.dat"):
    # Obtener la ruta del directorio actual (donde guardar los archivos)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio_actual, archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        for p in personas:
            bin_str = "|".join(["S" if b else "N" for b in p["binarios"]])
            registro = f"{p['nombre']}|{p['direccion']}|{p['dni']}|{bin_str}"
            f.write(registro + "\n")

def leer_variable(archivo="variable.dat"):
    personas = []
    # Obtener la ruta del directorio actual (donde están los archivos)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio_actual, archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split("|")
            nombre, direccion, dni, *bin_str = partes
            binarios = [c == "S" for c in bin_str]
            personas.append({"nombre": nombre, "direccion": direccion, "dni": dni, "binarios": binarios})
    return personas


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    # Ejemplo con 20 personas (puedes reemplazar con input real)
    personas = []
    for i in range(1, 21):
        personas.append({
            "nombre": f"Persona{i} Apellido{i}",
            "direccion": f"Calle {i} Nro {100+i}",
            "dni": str(30000000+i),
            "binarios": [(i+j) % 2 == 0 for j in range(8)]  # alternamos S/N
        })

    # Guardar en ambos archivos
    guardar_fijo(personas)
    guardar_variable(personas)

    # Leer y mostrar
    print("Lectura desde fijos.dat:")
    for p in leer_fijo():
        print(p)

    print("\nLectura desde variable.dat:")
    for p in leer_variable():
        print(p)

    # Comparar tamaños
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_fijo = os.path.join(directorio_actual, "fijos.dat")
    ruta_var = os.path.join(directorio_actual, "variable.dat")
    size_fijo = os.path.getsize(ruta_fijo)
    size_var = os.path.getsize(ruta_var)
    print(f"\nTamaño fijos.dat: {size_fijo} bytes")
    print(f"Tamaño variable.dat: {size_var} bytes")
    print(f"Archivos .dat guardados en {directorio_actual}")
    print(f"En el explorador de archivos, en propiedades, se puede ver el tamaño de los archivos")
