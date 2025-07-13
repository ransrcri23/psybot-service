"""
Servicios para análisis con Gemini AI
"""

import os
import google.generativeai as genai
from django.conf import settings
from .models import PHQ9Assessment
from pacientes.models import Paciente


class GeminiAnalysisService:
    """Servicio para análisis de valoraciones PHQ-9 usando Gemini AI"""
    
    def __init__(self):
        """Inicializar el servicio de Gemini"""
        try:
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.available = True
            else:
                self.available = False
        except Exception:
            self.available = False
    
    def analyze_single_assessment(self, assessment_id):
        """
        Analizar una valoración PHQ-9 individual
        
        Args:
            assessment_id (str): ID de la valoración
            
        Returns:
            str: Análisis clínico generado por Gemini
        """
        if not self.available:
            return "Servicio de análisis no disponible. Configure la API de Gemini."
        
        try:
            # Obtener la valoración
            assessment = PHQ9Assessment.objects.get(id=assessment_id)
            paciente = Paciente.objects.get(id=assessment.patient_id)
            
            # Crear prompt para Gemini
            prompt = f"""
            Como psicólogo clínico experto, analiza la siguiente valoración PHQ-9:
            
            Paciente: {paciente.nombre} {paciente.apellido}
            Fecha de nacimiento: {paciente.fecha_nacimiento}
            Fecha de valoración: {assessment.date_created.strftime('%d/%m/%Y')}
            
            Respuestas PHQ-9: {assessment.responses}
            Puntuación total: {assessment.total_score}/27
            
            Proporciona un análisis clínico detallado que incluya:
            1. Interpretación de la severidad de la depresión
            2. Análisis de síntomas específicos más relevantes
            3. Recomendaciones clínicas
            4. Sugerencias de seguimiento
            
            Responde en español y de manera profesional.
            """
            
            # Generar análisis
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error al generar análisis: {str(e)}"
    
    def analyze_trends(self, patient_id):
        """
        Analizar tendencias de múltiples valoraciones de un paciente
        
        Args:
            patient_id (str): ID del paciente
            
        Returns:
            str: Análisis de tendencias generado por Gemini
        """
        if not self.available:
            return "Servicio de análisis no disponible. Configure la API de Gemini."
        
        try:
            # Obtener paciente y valoraciones
            paciente = Paciente.objects.get(id=patient_id)
            valoraciones = PHQ9Assessment.objects.filter(patient_id=patient_id).order_by('date_created')
            
            if not valoraciones:
                return "No hay valoraciones para este paciente."
            
            # Preparar datos para el análisis
            datos_valoraciones = []
            for val in valoraciones:
                datos_valoraciones.append({
                    'fecha': val.date_created.strftime('%d/%m/%Y'),
                    'puntuacion': val.total_score,
                    'respuestas': val.responses
                })
            
            # Crear prompt para análisis de tendencias
            prompt = f"""
            Como psicólogo clínico experto, analiza las siguientes valoraciones PHQ-9 secuenciales:
            
            Paciente: {paciente.nombre} {paciente.apellido}
            Fecha de nacimiento: {paciente.fecha_nacimiento}
            Número de valoraciones: {len(datos_valoraciones)}
            
            Datos de valoraciones:
            """
            
            for i, datos in enumerate(datos_valoraciones, 1):
                prompt += f"""
            Valoración {i} ({datos['fecha']}):
            - Puntuación total: {datos['puntuacion']}/27
            - Respuestas: {datos['respuestas']}
            """
            
            prompt += """
            
            Proporciona un análisis de tendencias que incluya:
            1. Evolución temporal de la severidad de la depresión
            2. Patrones identificados en los síntomas
            3. Interpretación de la progresión del paciente
            4. Recomendaciones para tratamiento futuro
            5. Indicadores de mejora o empeoramiento
            
            Responde en español y de manera profesional.
            """
            
            # Generar análisis
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error al generar análisis de tendencias: {str(e)}"
