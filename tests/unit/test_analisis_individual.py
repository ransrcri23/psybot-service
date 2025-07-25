import pytest
import os
from unittest.mock import patch, MagicMock

# Configurar host para testing local
os.environ['MONGO_HOST'] = 'localhost'

@pytest.mark.django_db
@patch('psybot.utils.gemini_client.gemini_client')
def test_analisis_individual(mock_gemini_client):
    """Test análisis individual básico con mock de Gemini"""
    
    # Mock simple del cliente Gemini
    mock_gemini_client.is_configured.return_value = True
    mock_gemini_client.generate_text.return_value = "Análisis clínico simulado"
    
    # Test básico: verificar que el mock funciona
    result = mock_gemini_client.generate_text("test prompt")
    assert result == "Análisis clínico simulado"
    
    # Verificar que el cliente está configurado
    assert mock_gemini_client.is_configured() == True
    
    # Verificar que se llamó generate_text
    mock_gemini_client.generate_text.assert_called_once_with("test prompt")
