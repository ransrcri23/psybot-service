"""
Vista de prueba para verificar la configuración de Gemini AI
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from psybot.utils.gemini_client import gemini_client
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def test_gemini_configuration(request):
    """
    Endpoint para probar la configuración de Gemini AI
    """
    try:
        # Verificar si el cliente está configurado
        if not gemini_client.is_configured():
            return Response({
                'status': 'error',
                'message': 'Gemini AI no está configurado correctamente'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Realizar una prueba simple
        test_prompt = "Hola, ¿puedes confirmar que estás funcionando correctamente?"
        response = gemini_client.generate_text(test_prompt)
        
        if response:
            return Response({
                'status': 'success',
                'message': 'Gemini AI está configurado correctamente',
                'test_response': response
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Error al generar respuesta con Gemini AI'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error en test de configuración de Gemini: {e}")
        return Response({
            'status': 'error',
            'message': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def test_gemini_chat(request):
    """
    Endpoint para probar el chat con Gemini AI
    """
    try:
        message = request.data.get('message', '')
        context = request.data.get('context', '')
        
        if not message:
            return Response({
                'status': 'error',
                'message': 'El campo "message" es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generar respuesta de chat
        response = gemini_client.generate_chat_response(message, context)
        
        if response:
            return Response({
                'status': 'success',
                'message': 'Respuesta generada exitosamente',
                'response': response
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Error al generar respuesta de chat'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error en test de chat con Gemini: {e}")
        return Response({
            'status': 'error',
            'message': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
