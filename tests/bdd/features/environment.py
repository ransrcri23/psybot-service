"""
Configuración del entorno para pruebas BDD con behave
"""

import os
import requests
import json


def before_all(context):
    """
    Configuración inicial antes de ejecutar todas las pruebas
    """
    # Configurar base URL para las pruebas
    
    # Configurar base URL para las pruebas
    context.base_url = "http://localhost:8000"
    
    # Configurar headers por defecto
    context.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Inicializar sesión de requests
    context.session = requests.Session()
    context.session.headers.update(context.headers)
    
    # Variables para almacenar datos de prueba
    context.test_data = {}
    context.created_patients = []
    
    print("Entorno de pruebas BDD configurado")


def after_all(context):
    """
    Limpieza después de ejecutar todas las pruebas
    """
    # Limpiar datos de prueba si es necesario
    cleanup_test_data(context)
    
    # Limpieza completada
    
    print("Limpieza del entorno de pruebas completada")


def before_scenario(context, scenario):
    """
    Configuración antes de cada escenario
    """
    # Limpiar datos del escenario anterior
    context.response = None
    context.response_data = None
    context.status_code = None
    
    # Configuración de scenario completada


def after_scenario(context, scenario):
    """
    Limpieza después de cada escenario
    """
    # Limpiar datos creados en este escenario si es necesario
    if hasattr(context, 'created_in_scenario'):
        for patient_id in context.created_in_scenario:
            try:
                # Intentar limpiar paciente creado
                cleanup_patient(context, patient_id)
            except Exception as e:
                print(f"No se pudo limpiar paciente {patient_id}: {e}")


def cleanup_test_data(context):
    """
    Limpia todos los datos de prueba creados
    """
    if hasattr(context, 'created_patients'):
        for patient_id in context.created_patients:
            try:
                cleanup_patient(context, patient_id)
            except Exception as e:
                print(f"No se pudo limpiar paciente {patient_id}: {e}")


def cleanup_patient(context, patient_id):
    """
    Elimina un paciente específico
    """
    try:
        url = f"{context.base_url}/api/pacientes/{patient_id}/"
        response = context.session.delete(url)
        if response.status_code == 204:
            print(f"Paciente {patient_id} eliminado correctamente")
    except Exception as e:
        print(f"Error eliminando paciente {patient_id}: {e}")
