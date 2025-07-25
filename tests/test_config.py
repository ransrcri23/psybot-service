"""
Configuración específica para las pruebas automatizadas
"""
import os
import sys
from pathlib import Path

# Configurar variables de entorno para testing ANTES de cualquier import
os.environ['DJANGO_SETTINGS_MODULE'] = 'psybot.settings'

# Usar variables de entorno si están disponibles (CI), sino defaults locales
os.environ.setdefault('MONGO_HOST', 'localhost')
os.environ.setdefault('MONGO_PORT', '27017')
os.environ.setdefault('MONGO_DB_NAME', 'psybot_test_db')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-local-testing')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('GEMINI_API_KEY', 'fake-key-for-testing')
os.environ.setdefault('GEMINI_MODEL', 'gemini-1.5-flash')
os.environ.setdefault('GEMINI_TEMPERATURE', '0.7')
os.environ.setdefault('GEMINI_MAX_TOKENS', '1000')

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("[CONFIG] Configuración de testing establecida:")
print(f"   - MongoDB: {os.environ.get('MONGO_HOST')}:{os.environ.get('MONGO_PORT')}")
print(f"   - Base de datos: {os.environ.get('MONGO_DB_NAME')}")
