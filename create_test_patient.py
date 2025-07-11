#!/usr/bin/env python
import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psybot.settings')
django.setup()

from pacientes.models import Paciente

# Crear paciente de prueba
try:
    # Intentar crear el paciente
    paciente = Paciente(
        nombre="Juan",
        apellido="Pérez",
        identificacion="PATIENT_TEST_123",
        fecha_nacimiento=date(1990, 5, 15)
    )
    paciente.save()
    print(f"Paciente creado exitosamente: {paciente}")
    print(f"ID del paciente: {paciente.id}")
    
except Exception as e:
    print(f"Error al crear paciente: {e}")
    # Verificar si ya existe
    try:
        paciente = Paciente.objects.get(identificacion="PATIENT_TEST_123")
        print(f"Paciente ya existe: {paciente}")
        print(f"ID del paciente: {paciente.id}")
    except Paciente.DoesNotExist:
        print("El paciente no existe y no se pudo crear")
