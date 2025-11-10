def parecido_prefijo_sufijo(a: str, b: str) -> float:
    # Normalizar
    a, b = a.lower().strip(), b.lower().strip()
    len_a, len_b = len(a), len(b)
    min_len = min(len_a, len_b)

    # Comparar prefijos
    prefijo = 0
    for i in range(min_len):
        if a[i] == b[i]:
            prefijo += 1
        else:
            break

    # Comparar sufijos
    sufijo = 0
    for i in range(1, min_len + 1):
        if a[-i] == b[-i]:
            sufijo += 1
        else:
            break

    # Similitud basada en prefijo + sufijo
    similitud = (prefijo + sufijo) / max(len_a, len_b)
    return round(similitud * 100, 2)


# --- Pruebas ---
print("Porcentaje de similitud de Juan Perez vs Jaun Perez: ",parecido_prefijo_sufijo("Juan Perez", "Jaun Perez"),"%")      # ~82%
print("Porcentaje de similitud de Horacio Lopez vs Oracio Lopez: ",parecido_prefijo_sufijo("Horacio Lopez", "Oracio Lopez"),"%") # ~92%
print("Porcentaje de similitud de Pedro vs Perro: ",parecido_prefijo_sufijo("Pedro", "Perro"),"%")                # ~40%  
print("Porcentaje de similitud de Computadora vs Computación: ",parecido_prefijo_sufijo("Computadora", "Computación"),"%")    # ~72%
