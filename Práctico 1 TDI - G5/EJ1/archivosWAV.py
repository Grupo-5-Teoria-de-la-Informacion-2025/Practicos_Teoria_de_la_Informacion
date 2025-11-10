import struct
import os

def validar_formato_wav(nombre_archivo):
    #Valida que el archivo tenga el formato .wav correcto
    
    # Verificar extensión
    if not nombre_archivo.lower().endswith('.wav'):
        return False, "El archivo debe tener extensión .wav"
    
    # Verificar que el archivo existe
    if not os.path.exists(nombre_archivo):
        return False, "El archivo no existe"
    
    # Verificar que es un archivo (no un directorio)
    if not os.path.isfile(nombre_archivo):
        return False, "El nombre especificado no es un archivo"
    
    try:
        with open(nombre_archivo, 'rb') as archivo:
            # Leer los primeros 12 bytes para verificar el formato WAV
            header = archivo.read(12)
            
            # Verificar que comience con "RIFF"
            if header[:4] != b'RIFF':
                return False, "El archivo no tiene el formato RIFF válido"
            
            # Verificar que tenga el identificador "WAVE"
            if header[8:12] != b'WAVE':
                return False, "El archivo no tiene el identificador WAVE válido"
            
            return True, "Archivo .wav válido"
    
    except Exception as e:
        return False, f"Error al leer el archivo: {str(e)}"

def mostrar_cabecera_wav(nombre_archivo):
    #Lee y muestra los datos de la cabecera del archivo .wav
    
    try:
        with open(nombre_archivo, 'rb') as archivo:
            print("\n" + "="*50)
            print("DATOS DE LA CABECERA DEL ARCHIVO WAV")
            print("="*50)
            
            # Leer la cabecera completa (44 bytes)
            header = archivo.read(44)
            
            # Parsear los datos de la cabecera
            riff_id = header[0:4].decode('ascii')
            file_size = struct.unpack('<I', header[4:8])[0]
            wave_id = header[8:12].decode('ascii')
            fmt_id = header[12:16].decode('ascii')
            fmt_size = struct.unpack('<I', header[16:20])[0]
            audio_format = struct.unpack('<H', header[20:22])[0]
            num_channels = struct.unpack('<H', header[22:24])[0]
            sample_rate = struct.unpack('<I', header[24:28])[0]
            byte_rate = struct.unpack('<I', header[28:32])[0]
            block_align = struct.unpack('<H', header[32:34])[0]
            bits_per_sample = struct.unpack('<H', header[34:36])[0]
            data_id = header[36:40].decode('ascii')
            data_size = struct.unpack('<I', header[40:44])[0]
            
            # Mostrar la información usando los nombres del formato canónico WAV
            print("\n=== THE 'RIFF' CHUNK DESCRIPTOR ===")
            print(f"ChunkID: {riff_id} (Contiene las letras 'RIFF' en formato ASCII)")
            print(f"ChunkSize: {file_size} bytes (Tamaño del resto del chunk)")
            print(f"Format: {wave_id} (Contiene las letras 'WAVE' en formato ASCII)")
            
            print("\n=== THE 'FMT' SUB-CHUNK ===")
            print(f"Subchunk1ID: {fmt_id} (Contiene las letras 'fmt ' en formato ASCII)")
            print(f"Subchunk1Size: {fmt_size} bytes (16 para PCM)")
            
            # AudioFormat con descripción
            format_desc = "PCM (Linear quantization)" if audio_format == 1 else f"Formato comprimido {audio_format}"
            print(f"AudioFormat: {audio_format} ({format_desc})")
            
            # NumChannels con descripción
            if num_channels == 1:
                channels_desc = "Mono"
            elif num_channels == 2:
                channels_desc = "Stereo"
            else:
                channels_desc = f"{num_channels} canales"
            print(f"NumChannels: {num_channels} ({channels_desc})")
            
            print(f"SampleRate: {sample_rate} Hz (Frecuencia de muestreo)")
            print(f"ByteRate: {byte_rate} bytes/segundo (SampleRate * NumChannels * BitsPerSample/8)")
            print(f"BlockAlign: {block_align} bytes (NumChannels * BitsPerSample/8)")
            print(f"BitsPerSample: {bits_per_sample} bits por muestra")
            
            print("\n=== THE 'DATA' SUB-CHUNK ===")
            print(f"Subchunk2ID: {data_id} (Contiene las letras 'data' en formato ASCII)")
            print(f"Subchunk2Size: {data_size} bytes (Tamaño de los datos de audio)")
            
            # Mostrar información técnica adicional
            print("\n=== INFORMACIÓN TÉCNICA ===")
            print(f"File offset de datos: 44 bytes")
            print(f"Tamaño total del archivo: {file_size + 8} bytes")
            
            # Información adicional calculada
            duracion = data_size / byte_rate if byte_rate > 0 else 0
            print(f"Duración estimada: {duracion:.2f} segundos")
            
            # Verificar cálculos según la especificación
            print(f"\n=== VERIFICACIÓN DE CÁLCULOS ===")
            byte_rate_calculado = sample_rate * num_channels * bits_per_sample // 8
            block_align_calculado = num_channels * bits_per_sample // 8
            print(f"ByteRate calculado: {byte_rate_calculado} bytes/segundo")
            print(f"BlockAlign calculado: {block_align_calculado} bytes")
            print(f"¿ByteRate correcto?: {'✓' if byte_rate == byte_rate_calculado else '✗'}")
            print(f"¿BlockAlign correcto?: {'✓' if block_align == block_align_calculado else '✗'}")
            
    except Exception as e:
        print(f"Error al leer la cabecera: {str(e)}")

if __name__ == "__main__":
  
    print("PROGRAMA DE ANÁLISIS DE ARCHIVOS WAV")
    print("="*40)
    
    # Solicitar nombre del archivo
    nombre_archivo = input("\nIngrese el nombre del archivo .wav: ").strip()
    
    # Obtener el directorio donde está guardado este script
    directorio = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta completa al archivo
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    
    # Validar el archivo
    es_valido, mensaje = validar_formato_wav(ruta_archivo)
    
    if es_valido:
        print(f"✓ {mensaje}")
        # Mostrar la cabecera
        mostrar_cabecera_wav(ruta_archivo)
    else:
        print(f"✗ {mensaje}")
        print("Por favor, verifique que el archivo existe y tiene el formato correcto.")
    
    print("\nPrograma finalizado.")
