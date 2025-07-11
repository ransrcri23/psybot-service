"""
Utilidad para manejar la conexión y configuración de Gemini AI
"""

import google.generativeai as genai
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Cliente para interactuar con la API de Gemini AI
    """
    
    def __init__(self):
        """
        Inicializa el cliente de Gemini
        """
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.temperature = settings.GEMINI_TEMPERATURE
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        
        # Configurar la API key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            logger.error("GEMINI_API_KEY no está configurada")
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
    
    def generate_text(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Genera texto usando Gemini AI
        
        Args:
            prompt (str): El prompt para generar texto
            **kwargs: Parámetros adicionales para la generación
            
        Returns:
            Optional[str]: El texto generado o None si hay error
        """
        try:
            # Configurar parámetros de generación
            generation_config = {
                "temperature": kwargs.get("temperature", self.temperature),
                "max_output_tokens": kwargs.get("max_tokens", self.max_tokens),
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
            }
            
            # Generar respuesta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generando texto con Gemini: {e}")
            return None
    
    def generate_chat_response(self, message: str, context: Optional[str] = None) -> Optional[str]:
        """
        Genera una respuesta de chat usando Gemini AI
        
        Args:
            message (str): El mensaje del usuario
            context (Optional[str]): Contexto adicional para la conversación
            
        Returns:
            Optional[str]: La respuesta generada o None si hay error
        """
        try:
            # Construir el prompt con contexto si se proporciona
            if context:
                prompt = f"Contexto: {context}\n\nUsuario: {message}\n\nAsistente:"
            else:
                prompt = f"Usuario: {message}\n\nAsistente:"
            
            return self.generate_text(prompt)
            
        except Exception as e:
            logger.error(f"Error generando respuesta de chat: {e}")
            return None
    
    def is_configured(self) -> bool:
        """
        Verifica si el cliente está correctamente configurado
        
        Returns:
            bool: True si está configurado, False en caso contrario
        """
        return bool(self.api_key and self.model)


# Instancia global del cliente
gemini_client = GeminiClient()
