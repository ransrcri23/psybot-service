"""
Configuración específica para las pruebas automatizadas
"""
import os
import sys
from pathlib import Path

# Configurar variables de entorno para testing ANTES de cualquier import
os.environ['DJANGO_SETTINGS_MODULE'] = 'psybot.settings'
os.environ['MONGO_HOST'] = 'localhost'
os.environ['MONGO_PORT'] = '27017'
os.environ['MONGO_DB_NAME'] = 'psybot_test_db'
os.environ['SECRET_KEY'] = 'test-secret-key-for-local-testing'
os.environ['DEBUG'] = 'True'

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("[CONFIG] Configuración de testing establecida:")
print(f"   - MongoDB: {os.environ.get('MONGO_HOST')}:{os.environ.get('MONGO_PORT')}")
print(f"   - Base de datos: {os.environ.get('MONGO_DB_NAME')}")
