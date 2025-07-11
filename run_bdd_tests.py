#!/usr/bin/env python3
"""
Script para ejecutar pruebas BDD con behave y generar reportes Allure
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def setup_directories():
    """Crear directorios necesarios para los reportes"""
    directories = [
        "tests/bdd/reports",
        "tests/bdd/reports/allure-results",
        "tests/bdd/reports/allure-report",
        "tests/bdd/reports/junit"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Directorio creado/verificado: {directory}")


def run_behave_tests(tags=None, feature=None):
    """Ejecutar pruebas con behave"""
    print("Ejecutando pruebas BDD con behave...")
    
    # Comando base
    cmd = [
        "python", "-m", "behave",
        "tests/bdd/features/",
        "--format", "allure_behave.formatter:AllureFormatter",
        "--outdir", "tests/bdd/reports/allure-results",
        "--format", "junit",
        "--junit-directory", "tests/bdd/reports/junit",
        "--no-capture",
        "--no-capture-stderr"
    ]
    
    # Agregar filtros si se especifican
    if tags:
        cmd.extend(["--tags", tags])
    
    if feature:
        cmd.append(f"tests/bdd/features/{feature}")
    
    print(f"Ejecutando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Pruebas ejecutadas exitosamente")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando pruebas: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def generate_allure_report():
    """Generar reporte HTML con Allure"""
    print("Generando reporte Allure...")
    
    # Verificar si allure está instalado
    try:
        subprocess.run(["allure", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Allure CLI no está instalado. Instalando...")
        install_allure()
        
    # Generar reporte
    cmd = [
        "allure", "generate",
        "tests/bdd/reports/allure-results",
        "--output", "tests/bdd/reports/allure-report",
        "--clean"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Reporte Allure generado exitosamente")
        print("Reporte disponible en: tests/bdd/reports/allure-report/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generando reporte Allure: {e}")
        return False


def open_allure_report():
    """Abrir reporte Allure en el navegador"""
    print("Abriendo reporte Allure...")
    
    cmd = [
        "allure", "open",
        "tests/bdd/reports/allure-report"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error abriendo reporte: {e}")
        return False


def install_allure():
    """Instalar Allure CLI"""
    print("Instalando Allure CLI...")
    
    # Para Windows
    if os.name == 'nt':
        try:
            subprocess.run(["scoop", "install", "allure"], check=True)
            print("Allure instalado con Scoop")
            return True
        except:
            print("Scoop no disponible. Instalar manualmente desde: https://github.com/allure-framework/allure2/releases")
            return False
    
    # Para macOS
    elif sys.platform == 'darwin':
        try:
            subprocess.run(["brew", "install", "allure"], check=True)
            print("Allure instalado con Homebrew")
            return True
        except:
            print("Homebrew no disponible. Instalar manualmente desde: https://github.com/allure-framework/allure2/releases")
            return False
    
    # Para Linux
    else:
        print("Para Linux, instalar manualmente desde: https://github.com/allure-framework/allure2/releases")
        return False


def main():
    parser = argparse.ArgumentParser(description="Ejecutar pruebas BDD con behave y Allure")
    parser.add_argument("--tags", "-t", help="Filtrar por tags (ej: @smoke, @crear_paciente)")
    parser.add_argument("--feature", "-f", help="Ejecutar feature específico (ej: crear_paciente.feature)")
    parser.add_argument("--no-report", action="store_true", help="No generar reporte Allure")
    parser.add_argument("--open", "-o", action="store_true", help="Abrir reporte automáticamente")
    
    args = parser.parse_args()
    
    print("Iniciando ejecución de pruebas BDD")
    print("=" * 50)
    
    # Configurar directorios
    setup_directories()
    
    # Ejecutar pruebas
    success = run_behave_tests(tags=args.tags, feature=args.feature)
    
    if not success:
        print("Las pruebas fallaron")
        sys.exit(1)
    
    # Generar reporte si se solicita
    if not args.no_report:
        report_success = generate_allure_report()
        
        if report_success and args.open:
            open_allure_report()
    
    print("Proceso completado exitosamente")


if __name__ == "__main__":
    main()
