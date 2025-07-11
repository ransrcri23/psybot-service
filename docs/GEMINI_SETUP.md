# Configuración de Gemini AI

Este documento describe cómo configurar y usar Gemini AI en el proyecto PsyBot.

## Instalación

Las dependencias necesarias ya están incluidas en `requirements.txt`:

```
google-generativeai==0.8.3
python-dotenv==1.0.0
```

## Configuración

### 1. Variables de Entorno

Agrega las siguientes variables al archivo `.env`:

```env
# Gemini AI Configuration
GEMINI_API_KEY=tu-api-key-aquí
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000
```

### 2. Obtener API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la API key y agrégala a tu archivo `.env`

### 3. Verificar Configuración

Después de configurar la API key, puedes verificar que todo esté funcionando usando los endpoints de prueba:

#### GET `/api/gemini/test/`
Verifica que la configuración básica de Gemini esté funcionando.

#### POST `/api/gemini/chat/`
Prueba el chat con Gemini enviando un mensaje.

```json
{
  "message": "Hola, ¿cómo estás?",
  "context": "Contexto opcional para la conversación"
}
```

## Uso

### Cliente de Gemini

El cliente de Gemini está disponible en `psybot.utils.gemini_client`:

```python
from psybot.utils.gemini_client import gemini_client

# Generar texto
response = gemini_client.generate_text("Tu prompt aquí")

# Generar respuesta de chat
response = gemini_client.generate_chat_response("Mensaje del usuario", "Contexto opcional")

# Verificar configuración
is_configured = gemini_client.is_configured()
```

### Parámetros de Configuración

- **GEMINI_API_KEY**: Tu API key de Google AI Studio
- **GEMINI_MODEL**: Modelo a usar (por defecto: gemini-1.5-flash)
- **GEMINI_TEMPERATURE**: Creatividad de las respuestas (0.0-2.0, por defecto: 0.7)
- **GEMINI_MAX_TOKENS**: Número máximo de tokens en la respuesta (por defecto: 1000)

### Modelos Disponibles

- `gemini-1.5-flash`: Rápido y eficiente
- `gemini-1.5-pro`: Más potente, mejor para tareas complejas
- `gemini-1.0-pro`: Versión anterior, estable

## Estructura de Archivos

```
psybot/
├── utils/
│   ├── __init__.py
│   └── gemini_client.py      # Cliente principal de Gemini
├── views/
│   ├── __init__.py
│   └── gemini_test.py        # Vistas de prueba
└── settings.py               # Configuración de Django
```

## Ejemplo de Integración

```python
# En una vista de Django
from psybot.utils.gemini_client import gemini_client

def mi_vista(request):
    mensaje = request.data.get('mensaje')
    respuesta = gemini_client.generate_chat_response(mensaje)
    
    return Response({
        'respuesta': respuesta
    })
```

## Manejo de Errores

El cliente de Gemini maneja automáticamente los errores y devuelve `None` en caso de fallo. Siempre verifica la respuesta antes de usarla:

```python
response = gemini_client.generate_text("Mi prompt")
if response:
    # Usar la respuesta
    print(response)
else:
    # Manejar error
    print("Error generando respuesta")
```

## Seguridad

- **Nunca** incluyas tu API key en el código fuente
- Usa siempre variables de entorno
- El archivo `.env` está en `.gitignore` para evitar subir credenciales
- Usa el archivo `.env.example` como plantilla para otros desarrolladores
