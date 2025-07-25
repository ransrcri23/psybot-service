import pytest
import os
import uuid
from valoraciones.models import PHQ9Assessment
from pacientes.models import Paciente
from datetime import datetime

# Configurar host para testing local
os.environ['MONGO_HOST'] = 'localhost'

@pytest.mark.django_db
def test_crear_valoracion():
    """Test creación de valoración PHQ-9 usando el modelo directamente"""
    # Generar identificación única
    identificacion_unica = str(uuid.uuid4())[:8]
    
    # Primero crear un paciente
    paciente = Paciente(
        nombre="Ana",
        apellido="García",
        identificacion=identificacion_unica,
        fecha_nacimiento=datetime(1990, 5, 15)
    )
    paciente.save()
    
    # Crear valoración PHQ-9
    assessment = PHQ9Assessment(
        patient_id=str(paciente.id),
        responses=[2, 1, 2, 1, 2, 1, 2, 1, 2],  # 9 respuestas PHQ-9
        total_score=14
    )
    assessment.save()
    
    # Verificar que se guardó correctamente
    assert assessment.patient_id == str(paciente.id)
    assert len(assessment.responses) == 9
    assert assessment.total_score == 14
    assert assessment.id is not None
    
    # Verificar que se puede recuperar de la base de datos
    assessment_recuperado = PHQ9Assessment.objects(id=assessment.id).first()
    assert assessment_recuperado is not None
    assert assessment_recuperado.total_score == 14

