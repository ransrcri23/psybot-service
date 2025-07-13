"""
Vistas para la interfaz web de PsyBot
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from datetime import datetime, date
from pacientes.models import Paciente
from valoraciones.models import PHQ9Assessment
from valoraciones.services import GeminiAnalysisService


class DashboardView(View):
    """Vista principal del dashboard"""
    
    def get(self, request):
        # Obtener estadísticas básicas
        total_pacientes = Paciente.objects.count()
        total_valoraciones = PHQ9Assessment.objects.count()
        
        context = {
            'total_pacientes': total_pacientes,
            'total_valoraciones': total_valoraciones,
        }
        return render(request, 'dashboard.html', context)


class PacientesView(View):
    """Vista para gestión de pacientes"""
    
    def get(self, request):
        # Obtener lista de pacientes (sin paginación por ahora para simplificar)
        pacientes = Paciente.objects.order_by('-fecha_creacion')
        
        context = {
            'pacientes': pacientes,
        }
        return render(request, 'pacientes.html', context)
    
    def post(self, request):
        # Crear nuevo paciente
        try:
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            identificacion = request.POST.get('identificacion')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            
            # Validar campos requeridos
            if not all([nombre, apellido, identificacion, fecha_nacimiento]):
                messages.error(request, 'Todos los campos son requeridos.')
                return redirect('pacientes')
            
            # Crear paciente
            paciente = Paciente(
                nombre=nombre,
                apellido=apellido,
                identificacion=identificacion,
                fecha_nacimiento=fecha_nacimiento
            )
            paciente.save()
            
            messages.success(request, f'Paciente {nombre} {apellido} creado exitosamente.')
            return redirect('pacientes')
            
        except Exception as e:
            messages.error(request, f'Error al crear paciente: {str(e)}')
            return redirect('pacientes')


class ValoracionesView(View):
    """Vista para gestión de valoraciones"""
    
    def get(self, request):
        # Obtener lista de valoraciones (sin paginación por ahora para simplificar)
        valoraciones_raw = PHQ9Assessment.objects.order_by('-date_created')
        
        # Enriquecer valoraciones con información del paciente
        valoraciones_enriched = []
        for valoracion in valoraciones_raw:
            try:
                paciente = Paciente.objects.get(id=valoracion.patient_id)
                valoracion_data = {
                    'id': valoracion.id,
                    'patient_id': valoracion.patient_id,
                    'total_score': valoracion.total_score,
                    'date_created': valoracion.date_created,
                    'responses': valoracion.responses,
                    'paciente_nombre': f"{paciente.nombre} {paciente.apellido}",
                    'paciente_identificacion': paciente.identificacion
                }
                valoraciones_enriched.append(valoracion_data)
            except Paciente.DoesNotExist:
                # Si el paciente no existe, mostramos la valoración con datos básicos
                valoracion_data = {
                    'id': valoracion.id,
                    'patient_id': valoracion.patient_id,
                    'total_score': valoracion.total_score,
                    'date_created': valoracion.date_created,
                    'responses': valoracion.responses,
                    'paciente_nombre': 'Paciente no encontrado',
                    'paciente_identificacion': 'N/A'
                }
                valoraciones_enriched.append(valoracion_data)
        
        # Obtener lista de pacientes para el formulario
        pacientes = Paciente.objects.order_by('nombre')
        
        context = {
            'valoraciones': valoraciones_enriched,
            'pacientes': pacientes,
        }
        return render(request, 'valoraciones.html', context)
    
    def post(self, request):
        # Crear nueva valoración
        try:
            patient_id = request.POST.get('patient_id')
            
            # Obtener las 9 respuestas PHQ-9
            respuestas = []
            for i in range(1, 10):
                respuesta = request.POST.get(f'respuesta_{i}')
                if respuesta is None:
                    messages.error(request, f'Falta la respuesta {i}.')
                    return redirect('valoraciones')
                respuestas.append(int(respuesta))
            
            # Validar paciente
            if not patient_id:
                messages.error(request, 'Debe seleccionar un paciente.')
                return redirect('valoraciones')
            
            try:
                paciente = Paciente.objects.get(id=patient_id)
            except Paciente.DoesNotExist:
                messages.error(request, 'Paciente no encontrado.')
                return redirect('valoraciones')
            
            # Crear valoración
            valoracion = PHQ9Assessment(
                patient_id=patient_id,
                responses=respuestas
            )
            valoracion.save()
            
            messages.success(request, f'Valoración PHQ-9 creada exitosamente para {paciente.nombre} {paciente.apellido}.')
            return redirect('valoraciones')
            
        except Exception as e:
            messages.error(request, f'Error al crear valoración: {str(e)}')
            return redirect('valoraciones')


class AnalisisView(View):
    """Vista para análisis de valoraciones"""
    
    def get(self, request):
        # Obtener lista de pacientes que tienen valoraciones
        # MongoEngine no soporta values_list con flat=True, usamos una aproximación diferente
        valoraciones_ids = [v.patient_id for v in PHQ9Assessment.objects.only('patient_id')]
        pacientes_con_valoraciones = Paciente.objects.filter(
            id__in=list(set(valoraciones_ids))
        ).order_by('nombre')
        
        context = {
            'pacientes': pacientes_con_valoraciones,
        }
        return render(request, 'analisis.html', context)


class AnalisisIndividualView(View):
    """Vista para análisis individual de una valoración"""
    
    def post(self, request):
        try:
            valoracion_id = request.POST.get('valoracion_id')
            
            if not valoracion_id:
                return JsonResponse({'error': 'ID de valoración requerido'}, status=400)
            
            # Obtener valoración
            try:
                valoracion = PHQ9Assessment.objects.get(id=valoracion_id)
                paciente = Paciente.objects.get(id=valoracion.patient_id)
            except PHQ9Assessment.DoesNotExist:
                return JsonResponse({'error': 'Valoración no encontrada'}, status=404)
            except Paciente.DoesNotExist:
                return JsonResponse({'error': 'Paciente no encontrado'}, status=404)
            
            # Generar análisis con Gemini
            service = GeminiAnalysisService()
            analisis = service.analyze_single_assessment(str(valoracion.id))
            
            return JsonResponse({
                'success': True,
                'paciente': f'{paciente.nombre} {paciente.apellido}',
                'valoracion': {
                    'id': str(valoracion.id),
                    'fecha': valoracion.date_created.strftime('%d/%m/%Y'),
                    'total_score': valoracion.total_score,
                    'responses': valoracion.responses
                },
                'analisis': analisis
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AnalisisTendenciasView(View):
    """Vista para análisis de tendencias de un paciente"""
    
    def post(self, request):
        try:
            patient_id = request.POST.get('patient_id')
            
            if not patient_id:
                return JsonResponse({'error': 'ID de paciente requerido'}, status=400)
            
            # Obtener paciente
            try:
                paciente = Paciente.objects.get(id=patient_id)
            except Paciente.DoesNotExist:
                return JsonResponse({'error': 'Paciente no encontrado'}, status=404)
            
            # Obtener valoraciones del paciente
            valoraciones = PHQ9Assessment.objects.filter(patient_id=patient_id).order_by('date_created')
            
            if not valoraciones.count():
                return JsonResponse({'error': 'No hay valoraciones para este paciente'}, status=400)
            
            # Generar análisis de tendencias con Gemini
            service = GeminiAnalysisService()
            analisis = service.analyze_trends(patient_id)
            
            return JsonResponse({
                'success': True,
                'paciente': f'{paciente.nombre} {paciente.apellido}',
                'total_valoraciones': valoraciones.count(),
                'analisis': analisis
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ValoracionesPacienteView(View):
    """Vista para obtener valoraciones de un paciente específico"""
    
    def get(self, request, patient_id):
        try:
            # Obtener valoraciones del paciente
            valoraciones = PHQ9Assessment.objects.filter(patient_id=patient_id).order_by('-date_created')
            
            data = []
            for valoracion in valoraciones:
                data.append({
                    'id': str(valoracion.id),
                    'fecha': valoracion.date_created.strftime('%d/%m/%Y'),
                    'total_score': valoracion.total_score,
                    'responses': valoracion.responses
                })
            
            return JsonResponse({'valoraciones': data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
