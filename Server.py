import os  # Importa el módulo os para manejar archivos y directorios
import asyncio  # Importa asyncio para trabajar con programación asíncrona
import websockets  # Importa la librería websockets para crear el servidor WebSocket
import random  # Importa random para generar nombres de usuario aleatorios
from datetime import datetime  # Importa datetime para generar timestamps

connected_users = {}  # Diccionario que mantiene las conexiones activas {websocket: username}
HIST_FOLDER = "Historial"  # Carpeta donde se guardarán los archivos de historial individuales
LOG_GENERAL = "Servidor_general.log"  # Archivo de log general del servidor
os.makedirs(HIST_FOLDER, exist_ok=True)  # Crea la carpeta de historiales si no existe

# === FUNCIONES DE LOG Y HISTORIAL ===

def guardar_en_historial(username, mensaje):  # Guarda un mensaje en el archivo de historial del usuario
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Obtiene la fecha y hora actual formateada
    path = os.path.join(HIST_FOLDER, f"{username}.txt")  # Ruta del archivo del usuario
    with open(path, "a", encoding="utf-8") as f:  # Abre el archivo en modo añadir
        f.write(f"{now} {mensaje}\n")  # Escribe el mensaje con timestamp
    guardar_log_general(mensaje)  # También guarda el mensaje en el log general

def guardar_log_general(mensaje):  # Guarda un mensaje en el log general del servidor
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")  # Timestamp actual
    with open(LOG_GENERAL, "a", encoding="utf-8") as f:  # Abre el archivo log en modo añadir
        f.write(f"{now} {mensaje}\n")  # Escribe el mensaje con timestamp

def registrar_evento_servidor(evento):  # Registra eventos especiales como inicio y apagado
    guardar_log_general(f"{evento}")  # Llama a la función de log general con el evento

# === FUNCIONES DE CHAT ===

async def notify_all(message, exclude=None):  # Envía un mensaje a todos los usuarios conectados, menos al excluido
    for ws in connected_users:  # Itera sobre las conexiones activas
        if ws != exclude:  # Si no es el excluido
            await ws.send(message)  # Envía el mensaje

async def register(websocket, username=None):  # Registra un nuevo usuario
    if not username:  # Si no se proporcionó un nombre
        username = f"Usuario_{random.randint(100, 999)}"  # Genera uno aleatorio
    connected_users[websocket] = username  # Asocia el websocket con el nombre de usuario
    join_msg = f"{username} se ha unido al chat."  # Mensaje de unión
    print(join_msg)  # Muestra en la consola del servidor
    guardar_en_historial(username, join_msg)  # Guarda el mensaje en el historial del usuario
    await notify_all(join_msg, exclude=websocket)  # Notifica a los demás usuarios
    await websocket.send(f"Te has conectado como {username}")  # Notifica al propio usuario
    return username  # Devuelve el nombre de usuario

async def unregister(websocket):  # Maneja la desconexión de un usuario
    username = connected_users.get(websocket)  # Obtiene el nombre asociado al websocket
    if username:  # Si existe
        leave_msg = f"{username} se ha desconectado."  # Mensaje de desconexión
        print(leave_msg)  # Muestra en la consola del servidor
        guardar_en_historial(username, leave_msg)  # Guarda el mensaje en el historial
        del connected_users[websocket]  # Elimina la conexión del diccionario
        await notify_all(leave_msg)  # Notifica a los demás usuarios

async def chat_server(websocket):  # Maneja la conexión y mensajes de un usuario
    username = await websocket.recv()  # Espera a recibir el nombre de usuario
    username = await register(websocket, username.strip())  # Registra el usuario
    try:  # Intenta recibir y procesar mensajes del cliente
        async for message in websocket:  # Espera y maneja los mensajes del cliente
            log_msg = f"{username}: {message}"  # Construye el mensaje con nombre
            print(f" {log_msg}")  # Muestra en consola
            guardar_en_historial(username, log_msg)  # Guarda en el historial
            await notify_all(log_msg)  # Notifica a los demás usuarios
    except websockets.ConnectionClosed:  # Si la conexión se cierra abruptamente
        pass  # No hace nada especial al cerrarse
    finally:  # Siempre se ejecuta al terminar la conexión
        await unregister(websocket)  # Asegura la desconexión limpia

# === FUNCIONES DE CONSOLA ===

def mostrar_historiales():  # Muestra historiales disponibles y permite consultar
    archivos = os.listdir(HIST_FOLDER)  # Lista los archivos en la carpeta de historiales
    usuarios = [f.replace(".txt", "") for f in archivos if f.endswith(".txt")]  # Obtiene nombres de usuarios
    if not usuarios:  # Si no hay archivos
        print("No hay historiales disponibles.")  # Informa al usuario
        return  # Finaliza la función

    salir = False  # Controla el bucle de historial
    while not salir:  # Mientras no se elija salir
        print("\nUsuarios con historial:")  # Título
        for idx, user in enumerate(usuarios, 1):  # Muestra usuarios enumerados
            print(f"{idx}. {user}")  # Imprime el índice y nombre
        eleccion = input("Ingrese número o nombre (o 'Volver' para regresar): ").strip()  # Entrada del admin

        if eleccion.lower() == "volver":  # Si decide salir del menú
            salir = True  # Cambia el estado de salida
            continue  # Salta el resto del bucle actual

        if eleccion.isdigit():  # Si elige por número
            idx = int(eleccion) - 1  # Ajusta el índice (base 0)
            if 0 <= idx < len(usuarios):  # Verifica que esté dentro del rango
                eleccion = usuarios[idx]  # Asigna el nombre real
            else:  # Si el número está fuera de rango
                print("Número fuera de rango.")  # Muestra error
                continue  # Vuelve a solicitar entrada

        if eleccion in usuarios:  # Si el nombre está en la lista
            path = os.path.join(HIST_FOLDER, f"{eleccion}.txt")  # Ruta del archivo
            with open(path, encoding="utf-8") as f:  # Abre el archivo
                print(f"\n Historial de {eleccion}:\n")  # Título
                print(f.read())  # Muestra contenido del archivo
        else:  # Si el nombre no se encuentra
            print(" Usuario no encontrado.")  # Muestra error

async def listen_for_commands():  # Escucha comandos desde la consola
    print("Comandos disponibles: Historial | Apagar")  # Mensaje inicial
    while True:  # Bucle infinito hasta que se apague
        cmd = await asyncio.to_thread(input, "\nComando del servidor:\n")  # Espera un comando del admin
        cmd = cmd.strip().lower()  # Limpia el comando
        if cmd == "apagar":  # Si quiere apagar
            print("Apagando servidor")  # Mensaje
            registrar_evento_servidor("Servidor apagado")  # Registra en log
            for ws in list(connected_users):  # Cierra cada conexión
                await ws.close()  # Cierra conexión WebSocket
            break  # Sale del bucle principal
        elif cmd == "historial":  # Si pide ver historiales
            mostrar_historiales()  # Llama a la función
        else:  # Si el comando no es válido
            print("Comando no reconocido. Usa 'Historial' o 'Apagar'.")  # Mensaje de error

# === MAIN DEL SERVIDOR ===

async def main():  # Función principal del servidor
    print("Bienvenido al servidor Luna")  # Mensaje de bienvenida
    print("Comandos disponibles una vez encendido: Historial | Apagar")  # Instrucciones
    start = input("¿Desea encender el servidor? (Si/No): ").strip().lower()  # Confirmación del usuario
    if start != "si":  # Si dice que no
        print("Servidor cancelado por el usuario.")  # Mensaje de cancelación
        return  # Sale sin ejecutar el servidor

    print(" Servidor encendido en ws://localhost:8765")  # Aviso de encendido
    registrar_evento_servidor("Servidor iniciado")  # Log del inicio
    async with websockets.serve(chat_server, "localhost", 8765):  # Inicia el servidor WebSocket
        await listen_for_commands()  # Escucha comandos del admin

asyncio.run(main())  # Lanza el servidor
