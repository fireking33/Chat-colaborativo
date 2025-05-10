import asyncio  # Importa asyncio para manejar operaciones asíncronas
import websockets  # Importa la librería websockets para la conexión al servidor WebSocket
from aioconsole import ainput  # Importa ainput para permitir entrada asincrónica desde consola

async def receive_messages(websocket, my_username):  # Función para recibir mensajes del servidor
    try:  # Intenta recibir mensajes
        async for message in websocket:  # Escucha mensajes entrantes continuamente
            if message.startswith(f"{my_username}:"):  # Si el mensaje es del propio usuario
                continue  # Lo ignora para no mostrarlo
            print(f"\n{message}")  # Imprime el mensaje recibido
            print("Escribe tu mensaje: ", end="", flush=True)  # Reimprime el prompt de entrada
    except websockets.ConnectionClosed:  # Si el servidor cierra la conexión
        print("\nEl servidor cerró la conexión.")  # Muestra un mensaje de cierre

async def send_messages(websocket):  # Función para enviar mensajes al servidor
    print("Escribe \"Salir del chat\" para salir del chat en cualquier momento.\n")  # Instrucción inicial
    while True:  # Bucle infinito para enviar múltiples mensajes
        msg = await ainput("Escribe tu mensaje: ")  # Espera mensaje del usuario
        if msg.strip().lower() == "salir del chat":  # Si el mensaje es el comando para salir
            await websocket.close()  # Cierra la conexión WebSocket
            print("Has salido del chat.")  # Mensaje de salida
            break  # Sale del bucle
        await websocket.send(msg)  # Envía el mensaje al servidor

async def chat_client():  # Función principal del cliente
    uri = "ws://localhost:8765"  # Dirección del servidor WebSocket
    try:  # Intenta conectarse al servidor y manejar la sesión
        async with websockets.connect(uri) as websocket:  # Establece conexión con el servidor
            username = await ainput("Ingrese su nombre (o deje vacío para uno aleatorio): ")  # Pide nombre de usuario
            await websocket.send(username.strip())  # Envía el nombre al servidor

            bienvenida = await websocket.recv()  # Espera el mensaje de bienvenida del servidor
            print(f"\n{bienvenida}")  # Muestra el mensaje de bienvenida

            my_username = bienvenida.replace("Te has conectado como ", "").strip()  # Extrae el nombre de usuario

            await asyncio.gather(  # Ejecuta la recepción y envío de mensajes en paralelo
                receive_messages(websocket, my_username),  # Tarea para recibir mensajes
                send_messages(websocket)  # Tarea para enviar mensajes
            )
    except Exception as e:  # Captura cualquier error de conexión
        print(f"\nError de conexión: {e}")  # Muestra el error

if __name__ == "__main__":  # Verifica que el script sea ejecutado directamente
    asyncio.run(chat_client())  # Ejecuta la función principal del cliente
