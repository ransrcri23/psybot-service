from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from .models import PHQ9Assessment
from pacientes.models import Paciente

class PHQ9AssessmentSerializer(DocumentSerializer):
    class Meta:
        model = PHQ9Assessment
        fields = ['id', 'patient_id', 'responses', 'total_score', 'date_created']
        read_only_fields = ['id', 'total_score', 'date_created']

    def validate_patient_id(self, value):
        """Validar que el paciente existe"""
        if not Paciente.objects(id=value).first():
            raise serializers.ValidationError("El paciente especificado no existe")
        return value

    def validate_responses(self, value):
        """Validar que sean exactamente 9 respuestas"""
        if len(value) != 9:
            raise serializers.ValidationError("PHQ-9 debe tener exactamente 9 respuestas")
        
        # Validar que cada respuesta esté entre 0-3
        for i, response in enumerate(value):
            if not (0 <= response <= 3):
                raise serializers.ValidationError(f"La respuesta {i+1} debe estar entre 0 y 3")
        
        return value