# Análisis PHQ-9 con Gemini AI

Esta documentación describe las funcionalidades de análisis de valoraciones PHQ-9 utilizando Gemini AI, diseñadas específicamente para psicólogos clínicos.

## Funcionalidades Disponibles

### 1. Análisis Individual de Valoración PHQ-9

**Endpoint:** `POST /api/assessments/analyze/`

Genera un análisis clínico detallado de una valoración PHQ-9 específica.

#### Parámetros de entrada:
```json
{
  "assessment_id": "uuid-de-la-valoracion"
}
```

#### Respuesta:
```json
{
  "status": "success",
  "patient_info": {
    "nombre": "Juan Pérez",
    "edad": 30,
    "identificacion": "12345678"
  },
  "assessment_info": {
    "total_score": 15,
    "responses": [2, 1, 3, 2, 1, 2, 2, 1, 0],
    "date_created": "2024-01-15T10:30:00Z",
    "severity_level": "Moderadamente severo"
  },
  "clinical_analysis": "Análisis detallado generado por Gemini AI..."
}
```

### 2. Análisis de Tendencias (Múltiples Valoraciones)

**Endpoint:** `POST /api/assessments/trends/`

Analiza la evolución del paciente basándose en múltiples valoraciones PHQ-9 a lo largo del tiempo.

#### Parámetros de entrada:
```json
{
  "patient_id": "uuid-del-paciente"
}
```

#### Respuesta:
```json
{
  "status": "success",
  "patient_info": {
    "nombre": "Juan Pérez",
    "identificacion": "12345678"
  },
  "assessments_count": 3,
  "assessments_data": [
    {
      "id": "uuid-1",
      "total_score": 18,
      "date_created": "2024-01-01T10:00:00Z",
      "severity_level": "Moderadamente severo"
    },
    {
      "id": "uuid-2",
      "total_score": 12,
      "date_created": "2024-01-15T10:00:00Z",
      "severity_level": "Moderado"
    },
    {
      "id": "uuid-3",
      "total_score": 8,
      "date_created": "2024-02-01T10:00:00Z",
      "severity_level": "Leve"
    }
  ],
  "trend_analysis": "Análisis de tendencias generado por Gemini AI..."
}
```

## Tipos de Análisis Proporcionados

### Análisis Individual
El análisis individual incluye:

1. **Interpretación Clínica:**
   - Análisis detallado del estado depresivo actual
   - Identificación de síntomas predominantes
   - Patrones de severidad por dominio sintomático

2. **Áreas de Atención Prioritaria:**
   - Síntomas que requieren intervención inmediata
   - Factores de riesgo identificados
   - Elementos protectores presentes

3. **Recomendaciones Terapéuticas:**
   - Modalidades de tratamiento sugeridas
   - Frecuencia de sesiones recomendada
   - Consideraciones para derivación a psiquiatría

4. **Seguimiento y Monitoreo:**
   - Indicadores a vigilar en próximas sesiones
   - Frecuencia de re-evaluación sugerida
   - Señales de alerta para intervención de crisis

5. **Consideraciones Adicionales:**
   - Aspectos psicoeducativos relevantes
   - Recursos de apoyo recomendados
   - Estrategias de autocuidado apropiadas

### Análisis de Tendencias
El análisis de tendencias incluye:

1. **Análisis de Tendencias:**
   - Patrón de evolución (mejora, empeoramiento, estabilidad)
   - Velocidad de cambio observada
   - Fluctuaciones significativas identificadas

2. **Interpretación Clínica:**
   - Posible respuesta al tratamiento actual
   - Identificación de períodos críticos
   - Factores que pueden influir en los cambios

3. **Pronóstico:**
   - Expectativas realistas de evolución
   - Factores que favorecen o dificultan la recuperación
   - Tiempo estimado para objetivos terapéuticos

4. **Ajustes Terapéuticos Recomendados:**
   - Modificaciones en el plan de tratamiento
   - Intensidad de intervención sugerida
   - Modalidades adicionales a considerar

5. **Seguimiento:**
   - Frecuencia óptima de re-evaluación
   - Indicadores clave a monitorear
   - Criterios para ajustar el tratamiento

## Escalas de Severidad PHQ-9

| Puntaje | Nivel de Severidad |
|---------|-------------------|
| 0-4     | Mínimo            |
| 5-9     | Leve              |
| 10-14   | Moderado          |
| 15-19   | Moderadamente severo |
| 20-27   | Severo            |

## Preguntas PHQ-9 Analizadas

1. Poco interés o placer en hacer cosas
2. Sentirse decaído(a), deprimido(a) o sin esperanza
3. Dificultad para conciliar el sueño, o despertarse frecuentemente
4. Sentirse cansado(a) o con poca energía
5. Poco apetito o comer en exceso
6. Sentirse mal acerca de sí mismo(a) o sentir que es un fracaso
7. Dificultad para concentrarse en actividades
8. Moverse o hablar tan lento que otras personas lo han notado
9. Pensamientos de lastimarse o que estaría mejor muerto(a)

## Ejemplos de Uso

### Análisis Individual
```bash
curl -X POST http://localhost:8000/api/assessments/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "assessment_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Análisis de Tendencias
```bash
curl -X POST http://localhost:8000/api/assessments/trends/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

## Consideraciones Importantes

1. **Confidencialidad:** Toda la información del paciente se maneja con estricta confidencialidad
2. **Uso Profesional:** Las recomendaciones están dirigidas exclusivamente a psicólogos clínicos
3. **Complemento al Juicio Clínico:** Los análisis de IA complementan, no reemplazan, el juicio clínico profesional
4. **Frecuencia de Uso:** Se recomienda usar estas herramientas como parte de la evaluación rutinaria del paciente

## Manejo de Errores

### Errores Comunes

- **404 Not Found:** Valoración o paciente no encontrado
- **400 Bad Request:** Parámetros faltantes o incorrectos
- **500 Internal Server Error:** Error en el procesamiento con Gemini AI

### Ejemplo de Respuesta de Error
```json
{
  "status": "error",
  "message": "La valoración PHQ-9 especificada no existe"
}
```

## Soporte Técnico

Para problemas técnicos o consultas sobre la implementación, contactar al equipo de desarrollo con los detalles específicos del error y el contexto de uso.
