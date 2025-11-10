import math
import time

def fermat_factorization(n: int) -> tuple:
    """
    Implementa el Algoritmo de Factorización de Fermat.
    Busca factores primos p y q para un módulo n = p * q.
    Funciona eficientemente si p y q son cercanos entre sí.
    """
    if n <= 0 or not isinstance(n, int):
        return (None, None, "El número N debe ser un entero positivo.")
    
    # Manejo de casos triviales
    if n % 2 == 0:
        return (2, n // 2, "Factorización trivial: N es par.")
    
    # 1. Comenzar con 'a' como la raíz cuadrada de N (redondeada al siguiente entero)
    a = math.isqrt(n)
    if a * a == n:
        return (a, a, "N es un cuadrado perfecto.")

    a += 1
    
    # El límite superior se establece en un valor razonable (ej. hasta n/2)
    max_a = (n + 1) // 2
    
    start_time = time.time()
    
    while a < max_a:
        # 2. Calcular b^2 = a^2 - n
        b_squared = a * a - n
        
        # 3. Comprobar si b^2 es un cuadrado perfecto
        b = math.isqrt(b_squared)
        
        if b * b == b_squared:
            # Factores encontrados: p = a - b y q = a + b
            p = a - b
            q = a + b
            return (p, q, f"Factores encontrados: p={p}, q={q}")
        
        a += 1
        
        if time.time() - start_time > 10: 
             return (None, None, "Factorización excedió el tiempo límite. Los factores están muy separados.")

    return (None, None, "Factorización fallida. Los factores están muy separados o N es primo.")

# --- Bloque de Ejecución ---
if __name__ == "__main__":
    
    # --- Valor para el ejercicio 13 (n=2291) ---
    print("El número N para el ejercicio anterior fue 2291.")
    
    while True:
        try:
            # Solicitar al usuario el número a factorizar
            N_input = input("Introduce el número N (módulo RSA) a factorizar: ")
            N = int(N_input)
            break
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")
            
    print(f"\nIniciando la factorización de N = {N}...")
    p, q, mensaje = fermat_factorization(N)
    
    if p and q:
        print("\n--- Resultado de Factorización ---")
        print(f"Módulo N: {N}")
        print(f"Factor p: {p}")
        print(f"Factor q: {q}")
        print(f"Verificación: {p} * {q} = {p * q}")
    else:
        print(f"\n--- Resultado de Factorización ---")
        print(f"Error/Aviso: {mensaje}")