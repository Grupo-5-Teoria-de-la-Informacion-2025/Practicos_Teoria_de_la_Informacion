def transformada_inversa_burrows_wheeler(cadena_transformada, mostrar_proceso=True):
    
    #Aplica la transformada inversa de Burrows-Wheeler para recuperar la cadena original.
    
    
    if not cadena_transformada:
        return ""
    
    n = len(cadena_transformada)
    
    if mostrar_proceso:
        print("\nPROCESO DE RECUPERACION DE LA CADENA ORIGINAL")
        print("Cadena transformada:", cadena_transformada)
        print("Longitud:", n, "caracteres")
        print("=" * 50)
    
    # Crear lista de caracteres con sus posiciones originales
    posiciones_caracteres = [(cadena_transformada[i], i) for i in range(n)]
    
    if mostrar_proceso:
        print("\n1. CREANDO POSICIONES DE CARACTERES:")
        for i, (caracter, posicion) in enumerate(posiciones_caracteres):
            print("   Posicion", i, ":", caracter, "(posicion original:", posicion, ")")
    
    # Ordenar por caracter (orden lexicografico)
    posiciones_caracteres.sort()
    
    if mostrar_proceso:
        print("\n2. ORDENANDO POR CARACTER (primera columna de la matriz):")
        for i, (caracter, posicion) in enumerate(posiciones_caracteres):
            print("   Posicion", i, ":", caracter, "(viene de posicion original:", posicion, ")")
    
    # Crear el mapeo LF (Last-to-First mapping)
    mapeo_lf = [0] * n
    for i in range(n):
        mapeo_lf[posiciones_caracteres[i][1]] = i
    
    if mostrar_proceso:
        print("\n3. CREANDO MAPEO LF (Last-to-First):")
        print("   El mapeo LF conecta cada posicion en la ultima columna con su posicion en la primera columna")
        for i in range(n):
            print("   LF[", i, "] =", mapeo_lf[i], "(posicion", i, "-> posicion", mapeo_lf[i], ")")
    
    # Encontrar la posicion del caracter de fin de cadena ($)
    posicion_inicio = 0
    for i in range(n):
        if cadena_transformada[i] == '$':
            posicion_inicio = i
            break
    
    if mostrar_proceso:
        print("\n4. ENCONTRANDO PUNTO DE INICIO:")
        print("   Caracter de fin de cadena '$' esta en posicion:", posicion_inicio)
        print("   Comenzamos la reconstruccion desde esta posicion")
    
    # Reconstruir la cadena original
    cadena_original = []
    posicion_actual = posicion_inicio
    
    if mostrar_proceso:
        print("\n5. RECONSTRUYENDO LA CADENA ORIGINAL:")
        print("   Proceso paso a paso:")
    
    for paso in range(n):
        caracter = cadena_transformada[posicion_actual]
        cadena_original.append(caracter)
        
        if mostrar_proceso:
            cadena_parcial = ''.join(reversed(cadena_original))
            print("   Paso", paso + 1, ": Posicion", posicion_actual, "->", caracter, "| Cadena parcial:", cadena_parcial)
        
        # Mover a la siguiente posicion usando el mapeo LF
        posicion_actual = mapeo_lf[posicion_actual]
    
    # La cadena se construye en orden inverso, asi que la invertimos
    resultado = ''.join(reversed(cadena_original))
    
    if mostrar_proceso:
        print("\n6. RESULTADO FINAL:")
        print("   Cadena reconstruida (invertida):", resultado)
        print("=" * 50)
    
    return resultado

#Funcion principal que lee una cadena transformada por teclado
#y recupera la cadena original usando la transformada inversa de Burrows-Wheeler.
if __name__ == "__main__":
    
    print("=== Transformada Inversa de Burrows-Wheeler ===")
    print("Este programa recupera la cadena original a partir de una cadena transformada.")
    print("La cadena transformada debe haber sido generada por la transformada de Burrows-Wheeler.")
    print("El programa mostrara el proceso paso a paso de como se recupera la cadena.")
    print()
    
    try:
        # Leer la cadena transformada por teclado
        entrada_transformada = input("Ingrese la cadena transformada: ").strip()
        
        if not entrada_transformada:
            print("Error: No se ingreso ninguna cadena.")
            exit()
        
        # Aplicar la transformada inversa con proceso detallado
        cadena_original = transformada_inversa_burrows_wheeler(entrada_transformada, mostrar_proceso=True)
        
        # Mostrar resumen final
        print("\nRESUMEN FINAL:")
        print("   Cadena transformada ingresada:", entrada_transformada)
        print("   Cadena original recuperada:", cadena_original)
        print("   Longitud de la cadena:", len(cadena_original), "caracteres")
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print("Error inesperado:", e)



 