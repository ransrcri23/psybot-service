import pytest
import os
import uuid
from pacientes.models import Paciente
from datetime import datetime

# Configurar host para testing local
os.environ['MONGO_HOST'] = 'localhost'

@pytest.mark.django_db
def test_crear_paciente():
    """Test creación de paciente usando el modelo directamente"""
    # Generar identificación única para cada test
    identificacion_unica = str(uuid.uuid4())[:8]  # 8 caracteres únicos
    
    # Crear paciente directamente con el modelo
    paciente = Paciente(
        nombre="Juan",
        apellido="Perez",
        identificacion=identificacion_unica,
        fecha_nacimiento=datetime(1980, 1, 1)
    )
    paciente.save()
    
    # Verificar que se guardó correctamente
    assert paciente.nombre == "Juan"
    assert paciente.apellido == "Perez"
    assert paciente.identificacion == identificacion_unica
    assert paciente.id is not None
    
    # Verificar que se puede recuperar de la base de datos
    paciente_recuperado = Paciente.objects(id=paciente.id).first()
    assert paciente_recuperado is not None
    assert paciente_recuperado.nombre == "Juan"
