#!/usr/bin/env python3
"""
Script para ejecutar las pruebas automatizadas del proyecto PsyBot
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Exitoso")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Falló")
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    """Función principal para ejecutar las pruebas"""
    print("🧪 Iniciando pruebas automatizadas para PsyBot Service")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("manage.py").exists():
        print("❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto.")
        sys.exit(1)
    
    # Configurar variables de entorno para testing
    os.environ['DJANGO_SETTINGS_MODULE'] = 'psybot.settings'
    os.environ['SECRET_KEY'] = 'test-secret-key-for-local-testing'
    os.environ['DEBUG'] = 'True'
    
    # Lista de comandos a ejecutar
    commands = [
        ('python -c "import tests.test_config; import pytest; pytest.main([\'tests/unit/\', \'-v\', \'--tb=short\', \'--disable-warnings\'])"', "Ejecutando pruebas unitarias"),
        ('python -c "import tests.test_config; import pytest; pytest.main([\'tests/unit/\', \'--tb=short\', \'--disable-warnings\', \'--quiet\'])"', "Resumen de pruebas"),
    ]
    
    success_count = 0
    total_commands = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"✅ Comandos exitosos: {success_count}/{total_commands}")
    
    if success_count == total_commands:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
