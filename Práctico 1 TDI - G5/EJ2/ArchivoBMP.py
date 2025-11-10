import struct
import os


# Valida que el archivo tenga el formato .bmp correcto
def validar_formato_bmp(nombre_archivo):
    # Ruta absoluta al archivo en la misma carpeta del script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio, nombre_archivo)

    # Verificar extensión
    if not nombre_archivo.lower().endswith('.bmp'):
        return False, "El archivo debe tener extensión .bmp"
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta_archivo):
        return False, "El archivo no existe"
    
    # Verificar que es un archivo (no un directorio)
    if not os.path.isfile(ruta_archivo):
        return False, "El nombre especificado no es un archivo"
    
    try:
        with open(ruta_archivo, 'rb') as archivo:
            # Leer los primeros 2 bytes para verificar la firma BMP
            signature = archivo.read(2)
            
            # Verificar que comience con "BM"
            if signature != b'BM':
                return False, "El archivo no tiene la firma BMP válida (debe comenzar con 'BM')"
            
            return True, "Archivo .bmp válido"
    
    except Exception as e:
        return False, f"Error al leer el archivo: {str(e)}"


# Lee y muestra los datos de la cabecera del archivo .bmp
def mostrar_cabecera_bmp(nombre_archivo):
    # Ruta absoluta al archivo en la misma carpeta del script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(directorio, nombre_archivo)

    try:
        with open(ruta_archivo, 'rb') as archivo:
            print("\n" + "="*60)
            print("DATOS DE LA CABECERA DEL ARCHIVO BMP")
            print("="*60)
            
            # Leer la cabecera completa (14 bytes para cabecera + 40 bytes para propiedades)
            header = archivo.read(54)
            
            # Parsear los datos de la cabecera (primeros 14 bytes)
            signature = header[0:2].decode('ascii')
            file_size = struct.unpack('<I', header[2:6])[0]
            reserved = struct.unpack('<I', header[6:10])[0]
            data_offset = struct.unpack('<I', header[10:14])[0]
            
            # Parsear los datos de las propiedades de la imagen (siguientes 40 bytes)
            size = struct.unpack('<I', header[14:18])[0]
            width = struct.unpack('<I', header[18:22])[0]
            height = struct.unpack('<I', header[22:26])[0]
            planes = struct.unpack('<H', header[26:28])[0]
            bit_count = struct.unpack('<H', header[28:30])[0]
            compression = struct.unpack('<I', header[30:34])[0]
            image_size = struct.unpack('<I', header[34:38])[0]
            x_pixels_per_m = struct.unpack('<I', header[38:42])[0]
            y_pixels_per_m = struct.unpack('<I', header[42:46])[0]
            colors_used = struct.unpack('<I', header[46:50])[0]
            colors_important = struct.unpack('<I', header[50:54])[0]
            
            # Mostrar la información de la cabecera
            print("\n=== CABECERA (14 bytes) ===")
            print(f"Signature: {signature} (Siempre es 'BM')")
            print(f"FileSize: {file_size} bytes")
            print(f"Reserved: {reserved} (No se usa)")
            print(f"DataOffset: {data_offset} bytes (Posición del comienzo de los datos de imagen)")
            
            # Mostrar la información de las propiedades de la imagen
            print("\n=== PROPIEDADES DE LA IMAGEN (40 bytes) ===")
            print(f"Size: {size} bytes (Tamaño de esta sección)")
            print(f"Width: {width} píxeles (Anchura de la imagen)")
            print(f"Height: {height} píxeles (Altura de la imagen)")
            print(f"Planes: {planes} (Número de planos, siempre es 1)")
            print(f"BitCount: {bit_count} bits por píxel")
            
            # Descripción del tipo de compresión
            compression_desc = {
                0: "Sin compresión",
                1: "Compresión RLE 8-bit",
                2: "Compresión RLE 4-bit"
            }.get(compression, f"Compresión desconocida ({compression})")
            print(f"Compression: {compression} ({compression_desc})")
            
            print(f"ImageSize: {image_size} bytes (Tamaño de la imagen comprimida)")
            print(f"XPixelsPerM: {x_pixels_per_m} píxeles por metro (Resolución horizontal)")
            print(f"YPixelsPerM: {y_pixels_per_m} píxeles por metro (Resolución vertical)")
            print(f"ColorsUsed: {colors_used} (Número de colores usados)")
            print(f"ColorsImportant: {colors_important} (Número de colores importantes)")
            
            # Información adicional calculada
            print("\n=== INFORMACIÓN ADICIONAL ===")
            
            # Tamaño de la paleta de color
            if bit_count <= 8:
                paleta_size = data_offset - 54
                print(f"Tamaño de la paleta de color: {paleta_size} bytes")
                if paleta_size > 0:
                    print(f"Número de colores en la paleta: {paleta_size // 4}")
            
            # Resolución en DPI (puntos por pulgada)
            if x_pixels_per_m > 0:
                dpi_x = int(x_pixels_per_m / 39.3701)  # Convertir de píxeles/metro a DPI
                dpi_y = int(y_pixels_per_m / 39.3701)
                print(f"Resolución: {dpi_x} x {dpi_y} DPI")
            
            # Tamaño de los datos de imagen
            datos_imagen_size = file_size - data_offset
            print(f"Tamaño de los datos de imagen: {datos_imagen_size} bytes")
            
            # Verificar si el tamaño de imagen es consistente
            if image_size == 0:
                print("Nota: ImageSize es 0, lo que indica que no hay compresión")
            elif image_size > 0:
                print(f"Nota: Imagen comprimida, tamaño real: {image_size} bytes")
            
            # Información sobre el formato de color
            color_format = {
                1: "Monocromático (1 bit por píxel)",
                4: "16 colores (4 bits por píxel)",
                8: "256 colores (8 bits por píxel)",
                16: "65,536 colores (16 bits por píxel)",
                24: "16,777,216 colores (24 bits por píxel)",
                32: "4,294,967,296 colores (32 bits por píxel)"
            }.get(bit_count, f"Formato desconocido ({bit_count} bits por píxel)")
            print(f"Formato de color: {color_format}")
            
    except Exception as e:
        print(f"Error al leer la cabecera: {str(e)}")


# Función principal del programa
if __name__ == "__main__":
  
    print("PROGRAMA DE ANÁLISIS DE ARCHIVOS BMP")
    print("="*50)
    
    # Solicitar nombre del archivo
    nombre_archivo = input("\nIngrese el nombre del archivo .bmp: ").strip()
    
    # Validar el archivo
    es_valido, mensaje = validar_formato_bmp(nombre_archivo)
    
    if es_valido:
        print(f"✓ {mensaje}")
        # Mostrar la cabecera
        mostrar_cabecera_bmp(nombre_archivo)
    else:
        print(f"✗ {mensaje}")
        print("Por favor, verifique que el archivo existe y tiene el formato correcto.")
    
    print("\nPrograma finalizado.")
