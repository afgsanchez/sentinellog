import os
import subprocess
import platform
import time

def run_django_and_open_browser():
    """
    Activa el entorno virtual, inicia el servidor Django y abre el navegador.
    """
    print("Iniciando tu proyecto Django...")

    # Obtener el directorio actual del script (donde está sentinellog.py y manage.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # La raíz del proyecto (donde está .venv) está un nivel arriba del script_dir
    project_root = os.path.join(script_dir, os.pardir) # os.pardir es '..'

    # Ruta al ejecutable de Python dentro del entorno virtual
    if platform.system() == "Windows":
        python_executable = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    else: # Linux o macOS
        python_executable = os.path.join(project_root, ".venv", "bin", "python")

    # Verifica si el entorno virtual existe
    if not os.path.exists(python_executable):
        print(f"Error: No se encontró el entorno virtual en '{python_executable}'.")
        print("Asegúrate de que el entorno virtual .venv existe en el nivel superior.")
        print("Si no lo tienes, ejecuta 'python -m venv .venv' desde la carpeta 'sentinellog' (la que contiene .venv y SentinelLog).")
        return

    # Comando para ejecutar el servidor Django
    # manage.py ya está en script_dir, no necesitamos ir a project_root para manage.py
    django_server_command = [python_executable, os.path.join(script_dir, "manage.py"), "runserver"]
    print("Iniciando servidor Django...")
    
    # Ejecutamos el proceso desde el directorio del manage.py (que es script_dir)
    django_process = subprocess.Popen(django_server_command, cwd=script_dir)

    # Esperar un momento para que el servidor se inicie
    print("Esperando 3 segundos a que el servidor se inicie...")
    time.sleep(3)

    # Abrir el navegador
    server_url = "http://127.0.0.1:8000/"
    print(f"Abriendo el navegador en: {server_url}")
    try:
        if platform.system() == "Windows":
            os.startfile(server_url)
        elif platform.system() == "Darwin": # macOS
            subprocess.run(["open", server_url])
        else: # Linux
            subprocess.run(["xdg-open", server_url])
    except Exception as e:
        print(f"Error al intentar abrir el navegador: {e}")
        print(f"Por favor, abre manualmente {server_url} en tu navegador.")

    print("\n¡Servidor Django en marcha!")
    print(f"Para detener el servidor, regresa a esta ventana y presiona Ctrl+C (o cierra la ventana de la terminal).")
    print(f"El proceso del servidor tiene PID: {django_process.pid}")

    # Mantener el script de Python vivo mientras el servidor Django se ejecuta
    try:
        django_process.wait()
    except KeyboardInterrupt:
        print("\nDetectado Ctrl+C. Deteniendo servidor Django...")
        django_process.terminate()
        django_process.wait()

    print("Servidor Django detenido.")

if __name__ == "__main__":
    run_django_and_open_browser()