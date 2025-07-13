"""
URLs para la interfaz web de PsyBot
"""

from django.urls import path
import web_interface

urlpatterns = [
    # Dashboard principal
    path('', web_interface.DashboardView.as_view(), name='dashboard'),
    
    # Gestión de pacientes
    path('pacientes/', web_interface.PacientesView.as_view(), name='pacientes'),
    
    # Gestión de valoraciones
    path('valoraciones/', web_interface.ValoracionesView.as_view(), name='valoraciones'),
    
    # Análisis
    path('analisis/', web_interface.AnalisisView.as_view(), name='analisis'),
    path('analisis/individual/', web_interface.AnalisisIndividualView.as_view(), name='analisis_individual'),
    path('analisis/tendencias/', web_interface.AnalisisTendenciasView.as_view(), name='analisis_tendencias'),
    
    # API para obtener valoraciones de un paciente
    path('api/valoraciones-paciente/<str:patient_id>/', web_interface.ValoracionesPacienteView.as_view(), name='valoraciones_paciente'),
]
