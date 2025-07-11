from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PHQ9Assessment
from .serializers import PHQ9AssessmentSerializer, AnalyzeAssessmentSerializer, AnalyzeTrendsSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from psybot.utils.gemini_client import gemini_client
from pacientes.models import Paciente
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PHQ9AssessmentViewSet(ModelViewSet):
    serializer_class = PHQ9AssessmentSerializer
    
    def get_queryset(self):
        return PHQ9Assessment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=AnalyzeAssessmentSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'status': {'type': 'string'},
                'patient_info': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string'},
                        'edad': {'type': 'integer'},
                        'identificacion': {'type': 'string'}
                    }
                },
                'assessment_info': {
                    'type': 'object',
                    'properties': {
                        'total_score': {'type': 'integer'},
                        'responses': {'type': 'array', 'items': {'type': 'integer'}},
                        'date_created': {'type': 'string'},
                        'severity_level': {'type': 'string'}
                    }
                },
                'clinical_analysis': {'type': 'string'}
            }
        }
    },
    description="Genera un análisis clínico detallado de una valoración PHQ-9 específica usando Gemini AI"
)
@api_view(['POST'])
def analyze_phq9_with_gemini(request):
    """
    Análisis de resultados PHQ-9 y generación de recomendaciones para psicólogos clínicos
    """
    try:
        # Validar parámetros de entrada
        serializer = AnalyzeAssessmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Parámetros inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        assessment_id = serializer.validated_data['assessment_id']
        
        # Obtener la valoración PHQ-9
        assessment = PHQ9Assessment.objects(id=assessment_id).first()
        if not assessment:
            return Response({
                'status': 'error',
                'message': 'La valoración PHQ-9 especificada no existe'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener información del paciente
        paciente = Paciente.objects(id=assessment.patient_id).first()
        if not paciente:
            return Response({
                'status': 'error',
                'message': 'No se encontró la información del paciente'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Calcular edad del paciente
        edad = datetime.now().year - paciente.fecha_nacimiento.year
        
        # Generar prompt especializado para psicólogos clínicos
        prompt = create_clinical_analysis_prompt(assessment, paciente, edad)
        
        # Llamar a Gemini AI
        response = gemini_client.generate_text(prompt)
        if not response:
            return Response({
                'status': 'error',
                'message': 'Error al generar el análisis con Gemini AI'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'status': 'success',
            'patient_info': {
                'nombre': f"{paciente.nombre} {paciente.apellido}",
                'edad': edad,
                'identificacion': paciente.identificacion
            },
            'assessment_info': {
                'total_score': assessment.total_score,
                'responses': assessment.responses,
                'date_created': assessment.date_created.isoformat(),
                'severity_level': get_severity_level(assessment.total_score)
            },
            'clinical_analysis': response
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error en el análisis PHQ-9 con Gemini: {e}")
        return Response({
            'status': 'error',
            'message': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    request=AnalyzeTrendsSerializer,
    responses={
        200: {
            'type': 'object',
            'properties': {
                'status': {'type': 'string'},
                'patient_info': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string'},
                        'identificacion': {'type': 'string'}
                    }
                },
                'assessments_count': {'type': 'integer'},
                'assessments_data': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'string'},
                            'total_score': {'type': 'integer'},
                            'date_created': {'type': 'string'},
                            'severity_level': {'type': 'string'}
                        }
                    }
                },
                'trend_analysis': {'type': 'string'}
            }
        }
    },
    description="Analiza la evolución del paciente basado en múltiples valoraciones PHQ-9 usando Gemini AI"
)
@api_view(['POST'])
def analyze_multiple_phq9_trends(request):
    """
    Análisis de tendencias basado en múltiples valoraciones PHQ-9 de un paciente
    """
    try:
        # Validar parámetros de entrada
        serializer = AnalyzeTrendsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Parámetros inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        patient_id = serializer.validated_data['patient_id']
        
        # Obtener todas las valoraciones del paciente
        assessments = PHQ9Assessment.objects(patient_id=patient_id).order_by('date_created')
        if not assessments:
            return Response({
                'status': 'error',
                'message': 'No se encontraron valoraciones para este paciente'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener información del paciente
        paciente = Paciente.objects(id=patient_id).first()
        if not paciente:
            return Response({
                'status': 'error',
                'message': 'No se encontró la información del paciente'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generar prompt para análisis de tendencias
        prompt = create_trend_analysis_prompt(assessments, paciente)
        
        # Llamar a Gemini AI
        response = gemini_client.generate_text(prompt)
        if not response:
            return Response({
                'status': 'error',
                'message': 'Error al generar el análisis de tendencias con Gemini AI'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Preparar datos de las valoraciones
        assessment_data = []
        for assessment in assessments:
            assessment_data.append({
                'id': str(assessment.id),
                'total_score': assessment.total_score,
                'date_created': assessment.date_created.isoformat(),
                'severity_level': get_severity_level(assessment.total_score)
            })
        
        return Response({
            'status': 'success',
            'patient_info': {
                'nombre': f"{paciente.nombre} {paciente.apellido}",
                'identificacion': paciente.identificacion
            },
            'assessments_count': len(assessments),
            'assessments_data': assessment_data,
            'trend_analysis': response
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error en el análisis de tendencias PHQ-9: {e}")
        return Response({
            'status': 'error',
            'message': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_clinical_analysis_prompt(assessment, paciente, edad):
    """
    Crea un prompt especializado para análisis clínico de PHQ-9
    """
    # Mapeo de preguntas PHQ-9
    phq9_questions = [
        "Poco interés o placer en hacer cosas",
        "Sentirse decaído(a), deprimido(a) o sin esperanza",
        "Dificultad para conciliar el sueño, o despertarse frecuentemente",
        "Sentirse cansado(a) o con poca energía",
        "Poco apetito o comer en exceso",
        "Sentirse mal acerca de sí mismo(a) o sentir que es un fracaso",
        "Dificultad para concentrarse en actividades",
        "Moverse o hablar tan lento que otras personas lo han notado",
        "Pensamientos de lastimarse o que estaría mejor muerto(a)"
    ]
    
    # Crear desglose de respuestas
    responses_breakdown = ""
    for i, (question, response) in enumerate(zip(phq9_questions, assessment.responses), 1):
        severity_text = ["Nunca", "Algunos días", "Más de la mitad de los días", "Casi todos los días"][response]
        responses_breakdown += f"\n{i}. {question}: {response} ({severity_text})"
    
    prompt = f"""
    ANÁLISIS CLÍNICO PHQ-9 PARA PROFESIONAL DE SALUD MENTAL
    
    INFORMACIÓN DEL PACIENTE:
    - Nombre: {paciente.nombre} {paciente.apellido}
    - Edad: {edad} años
    - Fecha de evaluación: {assessment.date_created.strftime('%Y-%m-%d %H:%M')}
    
    RESULTADOS PHQ-9:
    - Puntaje total: {assessment.total_score}/27
    - Nivel de severidad: {get_severity_level(assessment.total_score)}
    
    DESGLOSE DE RESPUESTAS:{responses_breakdown}
    
    Como psicólogo clínico especializado, proporciona:
    
    1. INTERPRETACIÓN CLÍNICA:
       - Análisis detallado del estado depresivo actual
       - Identificación de síntomas predominantes
       - Patrones de severidad por dominio sintomático
    
    2. ÁREAS DE ATENCIÓN PRIORITARIA:
       - Síntomas que requieren intervención inmediata
       - Factores de riesgo identificados
       - Elementos protectores presentes
    
    3. RECOMENDACIONES TERAPÉUTICAS:
       - Modalidades de tratamiento sugeridas
       - Frecuencia de sesiones recomendada
       - Consideraciones para derivación a psiquiatría
    
    4. SEGUIMIENTO Y MONITOREO:
       - Indicadores a vigilar en próximas sesiones
       - Frecuencia de re-evaluación sugerida
       - Señales de alerta para intervención de crisis
    
    5. CONSIDERACIONES ADICIONALES:
       - Aspectos psicoeducativos relevantes
       - Recursos de apoyo recomendados
       - Estrategias de autocuidado apropiadas
    
    Por favor, proporciona un análisis profesional, basado en evidencia y orientado a la práctica clínica.
    """
    
    return prompt


def create_trend_analysis_prompt(assessments, paciente):
    """
    Crea un prompt para análisis de tendencias en múltiples valoraciones PHQ-9
    """
    # Preparar datos de tendencias
    scores_timeline = []
    for assessment in assessments:
        scores_timeline.append({
            'fecha': assessment.date_created.strftime('%Y-%m-%d'),
            'puntaje': assessment.total_score,
            'nivel': get_severity_level(assessment.total_score)
        })
    
    timeline_text = "\n".join([
        f"- {item['fecha']}: {item['puntaje']}/27 ({item['nivel']})"
        for item in scores_timeline
    ])
    
    # Convertir a lista para poder usar índices negativos
    assessments_list = list(assessments)
    
    prompt = f"""
    ANÁLISIS DE TENDENCIAS PHQ-9 - EVOLUCIÓN CLÍNICA
    
    PACIENTE: {paciente.nombre} {paciente.apellido}
    NÚMERO DE EVALUACIONES: {len(assessments_list)}
    PERÍODO: {assessments_list[0].date_created.strftime('%Y-%m-%d')} a {assessments_list[-1].date_created.strftime('%Y-%m-%d')}
    
    EVOLUCIÓN DE PUNTAJES:
    {timeline_text}
    
    Como psicólogo clínico especializado, analiza la evolución del paciente y proporciona:
    
    1. ANÁLISIS DE TENDENCIAS:
       - Patrón de evolución (mejora, empeoramiento, estabilidad)
       - Velocidad de cambio observada
       - Fluctuaciones significativas identificadas
    
    2. INTERPRETACIÓN CLÍNICA:
       - Posible respuesta al tratamiento actual
       - Identificación de períodos críticos
       - Factores que pueden influir en los cambios
    
    3. PRONÓSTICO:
       - Expectativas realistas de evolución
       - Factores que favorecen o dificultan la recuperación
       - Tiempo estimado para objetivos terapéuticos
    
    4. AJUSTES TERAPÉUTICOS RECOMENDADOS:
       - Modificaciones en el plan de tratamiento
       - Intensidad de intervención sugerida
       - Modalidades adicionales a considerar
    
    5. SEGUIMIENTO:
       - Frecuencia óptima de re-evaluación
       - Indicadores clave a monitorear
       - Criterios para ajustar el tratamiento
    
    Proporciona un análisis longitudinal profesional basado en la evolución observada.
    """
    
    return prompt


def get_severity_level(score):
    """
    Determina el nivel de severidad basado en el puntaje PHQ-9
    """
    if score >= 0 and score <= 4:
        return "Mínimo"
    elif score >= 5 and score <= 9:
        return "Leve"
    elif score >= 10 and score <= 14:
        return "Moderado"
    elif score >= 15 and score <= 19:
        return "Moderadamente severo"
    elif score >= 20 and score <= 27:
        return "Severo"
    else:
        return "Desconocido"
