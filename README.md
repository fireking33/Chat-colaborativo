 Chat colaborativo en tiempo real con WebSocket

Este proyecto implementa un **chat colaborativo en consola**, permitiendo la comunicación en tiempo real entre varios usuarios conectados mediante **WebSocket**. La ejecución se basa en Python e incluye funcionalidad de mensajes, nombres automáticos y un historial por usuario.



 Objetivo

Permitir que varios estudiantes interactúen en tiempo real desde terminal, usando una conexión persistente (`WebSocket`), sin técnicas tradicionales como `polling` o `long-polling`.



 Estructura del proyecto
Chat-colaborativo/
├── Historial/
├── Client.py
├── Server.py
├── README.md
└── Servidor_general.log



 Tecnologías utilizadas

- **Lenguaje:** Python 3.11 o superior
- **Librerías externas:**
  - [`websockets`](https://pypi.org/project/websockets/) – Comunicación WebSocket entre cliente y servidor
  - [`aioconsole`](https://pypi.org/project/aioconsole/) – Entrada/salida asincrónica en consola



 Pasos para ejecutar el programa

### 2. Clonar el repositorio

Selecciona la carpeta de tu agrado y ejecuta el siguiente comando


git clone https://github.com/fireking33/Chat-colaborativo.git


### 2. Instalar dependencias

Solo la primera vez, ejecuta:

```bash
pip install websockets
pip install aioconsole
```

### 3. Ejecutar el servidor (en una terminal)





python Server.py


### 4. Ejecutar el servidor (en una terminal)


cd Chat-colaborativo

python Client.py


 Características implementadas

-✅ Comunicación en tiempo real vía WebSocket
-✅ Asignación automática de nombre si no se ingresa uno
-✅ Mensajes se muestran con nombre de usuario
-✅ Notificaciones de conexión y desconexión
-✅ Historial por usuario almacenado en archivos .txt
-✅ Mensajes persistentes en sesión por usuario
-✅ Interfaz completamente por consola (sin GUI)
-✅ Código organizado y entendible para defensa
