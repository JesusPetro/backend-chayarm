# backend-chayarm

Backend desarrollado con FastAPI que gestiona la comunicación con un dispositivo ESP32 vía puerto serie y expone endpoints REST para interactuar con él.

## 🔍 Descripción

Este servicio se encarga de:

- Recibir peticiones HTTP desde el frontend.
- Traducir comandos de color (head, body) a códigos internos.
- Enviar/comunicar dichos códigos al ESP32 mediante un puerto serie.
- Leer la respuesta del ESP32 y devolverla al cliente.

## 📂 Estructura del proyecto

```
backend-chayarm/
├── api/
│   └── v1/
│       └── esp32.py         # Definición de endpoints y lógica de enrutamiento
├── services/
│   ├── esp32Services.py     # Clase `Conexion` para conexión serie
│   └── muñecoServices.py    # (Vacío o placeholder)
├── main.py                  # Inicialización de FastAPI, CORS y routers
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto
```

## ⚙️ Instalación

1. **Clona el repositorio**

   ```bash
   git clone <URL-del-repositorio>
   cd backend-chayarm
   ```

2. **Crea y activa un entorno virtual**

   ```bash
   python -m venv env
   source env/bin/activate      # Linux / macOS
   env\Scripts\activate       # Windows
   ```

3. **Instala las dependencias**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 🚀 Ejecución

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- El servidor quedará escuchando en `http://localhost:8000`.
- La documentación interactiva de la API estará disponible en `http://localhost:8000/docs`.

## 🔌 Endpoints disponibles

### 1. `/esp32/color` – POST

Envía al ESP32 un par de colores (`head`, `body`) y obtiene la respuesta.

- **Request Body**
  ```json
  {
    "head": "<código_hex_sin_#>", // p.ej. "FFD700"
    "body": "<código_hex_sin_#>" // p.ej. "FF6347"
  }
  ```
- **Response**
  - Texto plano: mensaje recibido desde el ESP32.
  - En caso de error de conexión, devuelve un HTTP 404 o excepción interna.

### 2. `/` – GET

Endpoint de prueba que retorna un mensaje fijo:

```json
{ "message": "Not timed" }
```

## 🛠 Servicios internos

- **`services/esp32Services.py`**  
  Clase `Conexion` que:

  1. Abre el puerto serie (por defecto `COM4`, 115200 baud).
  2. `enviar_mensaje(msg)`: escribe en el puerto.
  3. `recibir_mensaje()`: lee línea terminada en `\n`.
  4. `cerrar()`: cierra la conexión.

- **`services/muñecoServices.py`**  
  Placeholder para futuras lógicas sobre manejo de “muñecos” (actualmente vacío).

## 🎨 CORS

Configurado para permitir peticiones desde `http://localhost:5173`. Ajusta la lista `origins` en `main.py` si necesitas añadir otros orígenes.

## 📄 Requisitos

Todos los paquetes usados están en `requirements.txt`. Los principales son:

- `fastapi`
- `uvicorn`
- `pydantic`
- `pyserial`

## 📝 Notas

- Asegúrate de tener permiso para acceder al puerto serie en tu sistema.
- Cambia el parámetro `puerto` en `Conexion` si tu ESP32 está en un puerto distinto.

---
