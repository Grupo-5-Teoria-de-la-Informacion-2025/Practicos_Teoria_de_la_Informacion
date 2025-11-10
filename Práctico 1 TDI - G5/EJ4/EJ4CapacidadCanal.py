"""
Capacidad de canal
"""

import numpy as np
import csv
import os

def mutual_information(p, P):
    joint = p[:, None] * P
    p_y = joint.sum(axis=0)
    mask = joint > 0
    ratio = np.zeros_like(P)
    nz_py = p_y > 0
    ratio[:, nz_py] = P[:, nz_py] / p_y[nz_py]
    logterm = np.zeros_like(ratio)
    logterm[mask] = np.log2(ratio[mask])
    I = np.sum(joint[mask] * logterm[mask])
    return float(I)

def blahut_arimoto(P, tol=1e-9, max_iter=10000):
    R, M = P.shape
    p = np.ones(R) / R
    for it in range(max_iter):
        joint = p[:, None] * P
        p_y = joint.sum(axis=0)
        ratio = np.zeros_like(P)
        nz_py = p_y > 0
        ratio[:, nz_py] = np.where(P[:, nz_py] > 0, P[:, nz_py] / p_y[nz_py], 1.0)
        log_ratio = np.zeros_like(ratio)
        mask = P > 0
        log_ratio[mask] = np.log(ratio[mask])
        s = np.sum(P * log_ratio, axis=1)
        r = np.exp(s)
        p_new = r / np.sum(r)
        if np.linalg.norm(p_new - p, ord=1) < tol:
            p = p_new
            break
        p = p_new
    C = mutual_information(p, P)
    return p, C, it+1

def ejecutar(archivo_entrada, archivo_salida):
    # Obtener la ruta del directorio actual (donde están los CSV de entrada y se guardarán los resultados)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_actual, archivo_entrada)
    ruta_salida = os.path.join(directorio_actual, archivo_salida)
    
    # Leer CSV
    P = np.loadtxt(ruta_entrada, delimiter=",")
    R, M = P.shape
    print(f"\nMatriz leída ({R}x{M}):\n", P)

    # Calcular capacidad
    p_star, C_bits, iters = blahut_arimoto(P)
    p_uniform = np.ones(R) / R
    I_uniform = mutual_information(p_uniform, P)

    print("\n--- Resultado ---")
    print(f"Iteraciones: {iters}")
    print(f"Distribución óptima p*(x): {np.round(p_star,6)}")
    print(f"Capacidad C = {C_bits:.6f} bits")
    print(f"I(X;Y) con entrada uniforme = {I_uniform:.6f} bits")

    # Guardar CSV salida
    with open(ruta_salida, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["p*(x)"])
        for val in p_star:
            writer.writerow([val])
        writer.writerow([])
        writer.writerow(["Capacidad (bits)", C_bits])
        writer.writerow(["I uniforme (bits)", I_uniform])
        writer.writerow(["Iteraciones", iters])

    print(f"\nResultados guardados en {ruta_salida}")


if __name__ == "__main__":
    while True:
        print("\n=== Cálculo de Capacidad de Canal ===")
        print("1) Canal Binario (R=2)")
        print("2) Canal Ternario (R=3)")
        print("3) Canal Cuaternario (R=4)")
        print("0) Salir")
        opcion = input("Seleccione opción: ")

        if opcion == "1":
            ejecutar("canal2.csv", "resultado2.csv")
        elif opcion == "2":
            ejecutar("canal3.csv", "resultado3.csv")
        elif opcion == "3":
            ejecutar("canal4.csv", "resultado4.csv")
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intente nuevamente.")



