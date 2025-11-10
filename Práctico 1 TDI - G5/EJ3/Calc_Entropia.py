import os
import math
from collections import Counter

# Clase para calcular entropía y redundancia de archivos 
class CalculadoraEntropia:
    
    def __init__(self):
        self.resultados = {}
    
    # Calcula la entropía considerando símbolos independientes
    def calcular_entropia_independiente(self, datos):
        
        if not datos:
            return 0, 0
        
        # Contar frecuencias de cada byte
        frecuencias = Counter(datos)
        total_bytes = len(datos)
        
        # Calcular probabilidades y entropía
        entropia = 0
        for frecuencia in frecuencias.values():
            probabilidad = frecuencia / total_bytes
            if probabilidad > 0:
                entropia -= probabilidad * math.log2(probabilidad)
        
        # Calcular redundancia (entropía máxima - entropía actual)
        entropia_maxima = 8  # Para bytes (8 bits)
        redundancia = entropia_maxima - entropia
        
        return entropia, redundancia

    # Calcula la entropía considerando dependencias entre símbolos
    def calcular_entropia_dependiente(self, datos, orden=1):
        
        if len(datos) < orden + 1:
            return 0, 0
        
        # Crear contexto de n-gramas
        ngramas = []
        for i in range(len(datos) - orden):
            ngrama = tuple(datos[i:i+orden])
            ngramas.append(ngrama)
        
        # Contar frecuencias de n-gramas
        frecuencias_ngramas = Counter(ngramas)
        total_ngramas = len(ngramas)
        
        # Calcular entropía condicional
        entropia_condicional = 0
        for ngrama, frecuencia in frecuencias_ngramas.items():
            probabilidad_ngrama = frecuencia / total_ngramas
            
            # Contar símbolos que siguen a este n-grama
            simbolos_siguientes = []
            for i in range(len(datos) - orden):
                if tuple(datos[i:i+orden]) == ngrama:
                    if i + orden < len(datos):
                        simbolos_siguientes.append(datos[i + orden])
            
            if simbolos_siguientes:
                frecuencias_siguientes = Counter(simbolos_siguientes)
                entropia_parcial = 0
                for freq in frecuencias_siguientes.values():
                    prob_condicional = freq / len(simbolos_siguientes)
                    if prob_condicional > 0:
                        entropia_parcial -= prob_condicional * math.log2(prob_condicional)
                
                entropia_condicional += probabilidad_ngrama * entropia_parcial
        
        # Calcular redundancia
        entropia_maxima = 8
        redundancia = entropia_maxima - entropia_condicional
        
        return entropia_condicional, redundancia
    
    # Analiza un archivo y calcula entropía y redundancia
    def analizar_archivo(self, nombre_archivo):
        try:
            # Obtener ruta absoluta en la misma carpeta que el script
            directorio = os.path.dirname(os.path.abspath(__file__))
            ruta_archivo = os.path.join(directorio, nombre_archivo)

            with open(ruta_archivo, 'rb') as f:
                datos = f.read()
            
            # Obtener información del archivo
            extension = os.path.splitext(nombre_archivo)[1].lower()
            tamaño = len(datos)
            
            # Calcular entropía independiente
            entropia_indep, redundancia_indep = self.calcular_entropia_independiente(datos)
            
            # Calcular entropía dependiente (orden 1)
            entropia_dep1, redundancia_dep1 = self.calcular_entropia_dependiente(datos, 1)
            
            # Calcular entropía dependiente (orden 2)
            entropia_dep2, redundancia_dep2 = self.calcular_entropia_dependiente(datos, 2)
            
            resultado = {
                'nombre': nombre_archivo,
                'extension': extension,
                'tamaño': tamaño,
                'entropia_independiente': entropia_indep,
                'redundancia_independiente': redundancia_indep,
                'entropia_dependiente_1': entropia_dep1,
                'redundancia_dependiente_1': redundancia_dep1,
                'entropia_dependiente_2': entropia_dep2,
                'redundancia_dependiente_2': redundancia_dep2
            }
            
            return resultado
            
        except Exception as e:
            print(f"Error al analizar {nombre_archivo}: {str(e)}")
            return None
    
    # Genera un reporte detallado
    def generar_reporte(self, resultado):
        if not resultado:
            print("No hay datos para generar reporte.")
            return
        
        print("\n" + "="*80)
        print("REPORTE DETALLADO DE ANÁLISIS DE ENTROPÍA")
        print("="*80)
        
        # Estadísticas generales
        archivo = resultado['nombre']
        print(f"\nINFORMACIÓN DEL ARCHIVO:")
        print(f"Nombre: {archivo}")
        print(f"Extensión: {resultado['extension']}")
        print(f"Tamaño: {resultado['tamaño']} bytes")
        
        # Estadísticas de entropía y redundancia
        print(f"\nENTROPÍA Y REDUNDANCIA:")
        print(f"Entropía Independiente: {resultado['entropia_independiente']:.3f} bits")
        print(f"Redundancia Independiente: {resultado['redundancia_independiente']:.3f} bits")
        print(f"Entropía Dependiente (Orden 1): {resultado['entropia_dependiente_1']:.3f} bits")
        print(f"Redundancia Dependiente (Orden 1): {resultado['redundancia_dependiente_1']:.3f} bits")
        print(f"Entropía Dependiente (Orden 2): {resultado['entropia_dependiente_2']:.3f} bits")
        print(f"Redundancia Dependiente (Orden 2): {resultado['redundancia_dependiente_2']:.3f} bits")

        # Interpretación de resultados
        print(f"\nINTERPRETACIÓN:")
        print(f"• Archivos con entropía < 4 bits: Muy compresibles (texto, patrones repetitivos)")
        print(f"• Archivos con entropía > 6 bits: Difícil de comprimir (datos aleatorios, encriptados)")
        print(f"• Diferencia alta entre independiente y dependiente: Mucha estructura y patrones")
        print(f"• Diferencia baja: Datos más aleatorios")

# Función principal de la aplicación
if __name__ == "__main__":
    
    print("CALCULADORA DE ENTROPÍA Y REDUNDANCIA ")
    print("="*60)
    
    calc = CalculadoraEntropia()
    
    # Pedir nombre del archivo
    archivo = input("Ingrese el nombre del archivo (en la misma carpeta): ").strip()
    
    # Analizar archivo y generar reporte
    resultado = calc.analizar_archivo(archivo)
    if resultado:
        calc.generar_reporte(resultado)
    else:
        print("✗ No se pudo analizar el archivo")
