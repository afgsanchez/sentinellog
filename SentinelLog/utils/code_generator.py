import hashlib
import random
import os

# Ruta relativa segura para guardar los códigos hasheados
ARCHIVO_CODIGOS = 'codigos_guardados.txt'

def generar_codigo():
    """Genera un código aleatorio de 6 dígitos como cadena."""
    return str(random.randint(100000, 999999))

def hash_sha256(codigo):
    """Devuelve el hash SHA-256 del código proporcionado."""
    return hashlib.sha256(codigo.encode()).hexdigest()

def guardar_codigo(hash_codigo):
    """Guarda el hash del código en el archivo de almacenamiento."""
    with open(ARCHIVO_CODIGOS, 'a') as f:
        f.write(hash_codigo + '\n')

def codigo_ya_existe(hash_codigo):
    """Verifica si el hash del código ya existe en el archivo."""
    if not os.path.exists(ARCHIVO_CODIGOS):
        return False
    with open(ARCHIVO_CODIGOS, 'r') as f:
        return hash_codigo in f.read().splitlines()

def generar_codigo_unico():
    """Genera un código único que no haya sido generado previamente."""
    intentos = 0
    while intentos < 1000:
        codigo = generar_codigo()
        hash_codigo = hash_sha256(codigo)
        if not codigo_ya_existe(hash_codigo):
            guardar_codigo(hash_codigo)
            return codigo
        intentos += 1
    raise Exception("No se pudo generar un código único después de muchos intentos.")

