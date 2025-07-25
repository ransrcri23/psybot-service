import pytest
import os
import uuid
from valoraciones.models import PHQ9Assessment
from pacientes.models import Paciente
from datetime import datetime

# Configurar host para testing local
os.environ['MONGO_HOST'] = 'localhost'

@pytest.mark.django_db
def test_analisis_tendencias():
    """Test análisis de tendencias básico con múltiples valoraciones"""
    
    # Generar identificación única
    identificacion_unica = str(uuid.uuid4())[:8]
    
    # Crear paciente de prueba
    paciente = Paciente(
        nombre="Carlos",
        apellido="López",
        identificacion=identificacion_unica,
        fecha_nacimiento=datetime(1985, 3, 10)
    )
    paciente.save()
    
    # Crear múltiples valoraciones para simular tendencias
    # Valoración 1: Score alto (depresivo)
    assessment1 = PHQ9Assessment(
        patient_id=str(paciente.id),
        responses=[3, 3, 2, 3, 2, 3, 2, 2, 3],  # Score: 23
        total_score=23,
        date_created=datetime(2024, 1, 1)
    )
    assessment1.save()
    
    # Valoración 2: Score medio (mejorando)
    assessment2 = PHQ9Assessment(
        patient_id=str(paciente.id),
        responses=[2, 2, 1, 2, 1, 2, 1, 1, 2],  # Score: 14
        total_score=14,
        date_created=datetime(2024, 2, 1)
    )
    assessment2.save()
    
    # Valoración 3: Score bajo (mucho mejor)
    assessment3 = PHQ9Assessment(
        patient_id=str(paciente.id),
        responses=[1, 1, 0, 1, 0, 1, 0, 0, 1],  # Score: 5
        total_score=5,
        date_created=datetime(2024, 3, 1)
    )
    assessment3.save()
    
    # Verificar que se guardaron las 3 valoraciones
    assessments = PHQ9Assessment.objects(patient_id=str(paciente.id))
    assert len(assessments) == 3
    
    # Verificar que muestran una tendencia de mejora
    scores = [a.total_score for a in assessments.order_by('date_created')]
    assert scores == [23, 14, 5]  # Tendencia decreciente = mejora
    
    # Verificar que la primera valoración es la más alta
    assert max(scores) == 23
    # Verificar que la última valoración es la más baja
    assert min(scores) == 5
