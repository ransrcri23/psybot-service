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


class AnalyzeAssessmentSerializer(serializers.Serializer):
    """
    Serializer para los parámetros de análisis individual de PHQ-9
    """
    assessment_id = serializers.UUIDField(required=True, help_text="ID de la valoración PHQ-9 a analizar")
    
    def validate_assessment_id(self, value):
        """Validar que la valoración existe"""
        if not PHQ9Assessment.objects(id=value).first():
            raise serializers.ValidationError("La valoración PHQ-9 especificada no existe")
        return value


class AnalyzeTrendsSerializer(serializers.Serializer):
    """
    Serializer para los parámetros de análisis de tendencias
    """
    patient_id = serializers.UUIDField(required=True, help_text="ID del paciente para análisis de tendencias")
    
    def validate_patient_id(self, value):
        """Validar que el paciente existe y tiene valoraciones"""
        if not Paciente.objects(id=value).first():
            raise serializers.ValidationError("El paciente especificado no existe")
        
        # Verificar que el paciente tiene valoraciones
        if not PHQ9Assessment.objects(patient_id=value).first():
            raise serializers.ValidationError("No se encontraron valoraciones para este paciente")
        
        return value
