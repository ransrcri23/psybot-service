"""
Step definitions para las funcionalidades de valoraciones PHQ-9
"""

import json
from behave import given, when, then, step
import requests
import uuid


@given('que tengo acceso al endpoint de valoraciones')
def step_acceso_endpoint_valoraciones(context):
    """Verificar acceso al endpoint de valoraciones"""
    context.valoraciones_url = f"{context.base_url}/api/assessments/"


@given('que existe un paciente de prueba para las valoraciones')
def step_paciente_prueba_valoraciones(context):
    """Usar paciente de prueba existente para valoraciones"""
    # Usar el ID del paciente creado manualmente
    context.patient_id = "73092b95-9129-48f7-a0af-d01b806bb572"
    
    # Verificar que el paciente existe
    response = context.session.get(f"{context.base_url}/api/pacientes/{context.patient_id}/")
    assert response.status_code == 200, f"El paciente no existe: {response.status_code}"


@given('que tengo los datos de una nueva valoración PHQ-9')
def step_datos_nueva_valoracion(context):
    """Preparar datos de una nueva valoración PHQ-9"""
    row = context.table[0]
    context.assessment_data = {
        "patient_id": context.patient_id,
        "responses": [int(row[f"respuesta{i+1}"]) for i in range(9)]
    }


@given('que tengo los datos de una valoración con {estado}')
def step_datos_valoracion_estado(context, estado):
    """Preparar datos específicos de valoración según el escenario"""
    row = context.table[0]
    context.assessment_data = {}
    
    if "sin paciente_id" in estado:
        context.assessment_data["responses"] = [int(row[f"respuesta{i+1}"]) for i in range(9)]
    elif "respuestas insuficientes" in estado:
        context.assessment_data = {
            "patient_id": context.patient_id,
            "responses": [int(row[f"respuesta{i+1}"]) for i in range(len(row))]
        }
    elif "respuestas inválidas" in estado:
        context.assessment_data = {
            "patient_id": context.patient_id,
            "responses": [int(row[f"respuesta{i+1}"]) for i in range(9)]
        }


@when('envío una solicitud POST para crear la valoración')
def step_post_crear_valoracion(context):
    """Enviar solicitud POST para crear una nueva valoración"""
    context.response = context.session.post(context.valoraciones_url, json=context.assessment_data)
    context.status_code = context.response.status_code
    context.response_data = context.response.json() if context.response.content else {}


@then('la valoración se crea exitosamente')
def step_valoracion_creada_exitosamente(context):
    """Verificar que la valoración se creó exitosamente"""
    assert context.status_code == 201
    assert 'id' in context.response_data
    context.created_assessment_id = context.response_data['id']


@then('el total_score se calcula correctamente como {score}')
def step_verificar_calculo_total_score(context, score):
    """Verificar que el total_score de la valoración es correcto"""
    assert context.response_data['total_score'] == int(score)


@then('la creación de la valoración falla')
def step_creacion_valoracion_falla(context):
    """Verificar que la creación de la valoración falló"""
    assert context.status_code == 400


@given('que tengo una valoración PHQ-9 creada previamente con ID conocido')
def step_valoracion_creada_previamente(context):
    """Crea y asegura que existe una valoración para pruebas de análisis"""
    context.execute_steps('''
        Dado que tengo los datos de una nueva valoración PHQ-9:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
    ''')




@then('el análisis se genera exitosamente')
def step_analisis_generado_exitosamente(context):
    """Verificar que el análisis individual se generó exitosamente"""
    assert context.status_code == 200
    assert 'clinical_analysis' in context.response_data




@then('el análisis de tendencias se genera exitosamente')
def step_analisis_tendencias_generado_exitosamente(context):
    """Verificar que el análisis de tendencias se generó exitosamente"""
    assert context.status_code == 200
    assert 'trend_analysis' in context.response_data


# ================== STEPS ADICIONALES IMPLEMENTADOS ==================

@then('la respuesta contiene los datos de la valoración creada')
def step_verificar_datos_valoracion_creada(context):
    """Verificar que la respuesta contiene los datos de la valoración"""
    assert 'patient_id' in context.response_data
    assert 'responses' in context.response_data
    assert 'total_score' in context.response_data
    assert 'date_created' in context.response_data


@then('la valoración tiene un ID único asignado')
def step_verificar_id_unico_valoracion(context):
    """Verificar que la valoración tiene un ID único"""
    assert 'id' in context.response_data
    assert context.response_data['id'] is not None
    try:
        uuid.UUID(context.response_data['id'])
    except ValueError:
        raise AssertionError(f"El ID no es un UUID válido: {context.response_data['id']}")


@then('la respuesta contiene un mensaje de error sobre 9 respuestas requeridas')
def step_verificar_error_9_respuestas(context):
    """Verificar mensaje de error sobre 9 respuestas requeridas"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['9', 'nine', 'nueve', 'exactamente']), \
        f"No se encontró mensaje sobre 9 respuestas en: {context.response_data}"


@then('la respuesta contiene un mensaje de error sobre valores válidos')
def step_verificar_error_valores_validos(context):
    """Verificar mensaje de error sobre valores válidos"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['valid', 'válido', 'range', 'rango', '0', '3']), \
        f"No se encontró mensaje sobre valores válidos en: {context.response_data}"


@given('que tengo los datos de una valoración sin paciente_id')
def step_datos_valoracion_sin_paciente_id(context):
    """Preparar datos de valoración sin paciente_id"""
    row = context.table[0]
    context.assessment_data = {
        "responses": [int(row[f"respuesta{i+1}"]) for i in range(9)]
    }


@then('la respuesta contiene un mensaje de error sobre patient_id requerido')
def step_verificar_error_patient_id_requerido(context):
    """Verificar mensaje de error sobre patient_id requerido"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['patient_id', 'patient', 'paciente', 'required', 'requerido']), \
        f"No se encontró mensaje sobre patient_id requerido en: {context.response_data}"


@then('la respuesta contiene información del paciente')
def step_verificar_informacion_paciente(context):
    """Verificar que la respuesta contiene información del paciente"""
    assert 'patient_info' in context.response_data
    patient_info = context.response_data['patient_info']
    assert 'nombre' in patient_info
    assert 'edad' in patient_info or 'identificacion' in patient_info


@then('la respuesta contiene información de la valoración')
def step_verificar_informacion_valoracion(context):
    """Verificar que la respuesta contiene información de la valoración"""
    assert 'assessment_info' in context.response_data
    assessment_info = context.response_data['assessment_info']
    assert 'total_score' in assessment_info
    assert 'responses' in assessment_info
    assert 'severity_level' in assessment_info


@then('la respuesta contiene un análisis clínico generado por Gemini')
def step_verificar_analisis_clinico_gemini(context):
    """Verificar que contiene análisis clínico de Gemini"""
    assert 'clinical_analysis' in context.response_data
    analysis = context.response_data['clinical_analysis']
    assert len(analysis) > 50  # Verificar que el análisis tiene contenido sustancial


@then('el análisis incluye interpretación clínica')
def step_verificar_interpretacion_clinica(context):
    """Verificar que el análisis incluye interpretación clínica"""
    analysis = context.response_data.get('clinical_analysis', '').lower()
    assert any(keyword in analysis for keyword in ['interpretación', 'interpretacion', 'análisis', 'analisis', 'clínico', 'clinico']), \
        "El análisis no incluye interpretación clínica"


@then('el análisis incluye recomendaciones terapéuticas')
def step_verificar_recomendaciones_terapeuticas(context):
    """Verificar que el análisis incluye recomendaciones terapéuticas"""
    analysis = context.response_data.get('clinical_analysis', '').lower()
    assert any(keyword in analysis for keyword in ['recomendación', 'recomendacion', 'terapéutica', 'terapeutica', 'tratamiento']), \
        "El análisis no incluye recomendaciones terapéuticas"


@given('que tengo un ID de valoración inexistente')
def step_id_valoracion_inexistente(context):
    """Preparar un ID de valoración inexistente"""
    context.nonexistent_assessment_id = str(uuid.uuid4())


@then('el análisis falla')
def step_analisis_falla(context):
    """Verificar que el análisis falló"""
    assert context.status_code in [400, 404]


@then('la respuesta contiene un mensaje de error sobre valoración inexistente')
def step_verificar_error_valoracion_inexistente(context):
    """Verificar mensaje de error sobre valoración inexistente"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['not found', 'no encontr', 'inexistente', 'exist']), \
        f"No se encontró mensaje sobre valoración inexistente en: {context.response_data}"


@given('que no proporciono un assessment_id')
def step_sin_assessment_id(context):
    """No proporcionar assessment_id"""
    context.no_assessment_id = True


@then('la respuesta contiene un mensaje de error sobre assessment_id requerido')
def step_verificar_error_assessment_id_requerido(context):
    """Verificar mensaje de error sobre assessment_id requerido"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['assessment_id', 'assessment', 'required', 'requerido']), \
        f"No se encontró mensaje sobre assessment_id requerido en: {context.response_data}"


@given('que tengo múltiples valoraciones PHQ-9 para el mismo paciente')
def step_multiples_valoraciones_mismo_paciente(context):
    """Crear múltiples valoraciones para el mismo paciente"""
    # Crear primera valoración
    context.execute_steps('''
        Dado que tengo los datos de una nueva valoración PHQ-9:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 2          | 2          | 2          | 2          | 2          | 2          | 2          | 2          | 2          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
    ''')
    
    # Crear segunda valoración
    context.execute_steps('''
        Dado que tengo los datos de una nueva valoración PHQ-9:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
    ''')


@then('la respuesta contiene el número de valoraciones analizadas')
def step_verificar_numero_valoraciones(context):
    """Verificar que contiene el número de valoraciones analizadas"""
    assert 'assessments_count' in context.response_data
    assert context.response_data['assessments_count'] >= 1


@then('la respuesta contiene datos de todas las valoraciones')
def step_verificar_datos_todas_valoraciones(context):
    """Verificar que contiene datos de todas las valoraciones"""
    assert 'assessments_data' in context.response_data
    assessments_data = context.response_data['assessments_data']
    assert len(assessments_data) >= 1
    for assessment in assessments_data:
        assert 'id' in assessment
        assert 'total_score' in assessment
        assert 'severity_level' in assessment


@then('la respuesta contiene un análisis de tendencias generado por Gemini')
def step_verificar_analisis_tendencias_gemini(context):
    """Verificar que contiene análisis de tendencias de Gemini"""
    assert 'trend_analysis' in context.response_data
    analysis = context.response_data['trend_analysis']
    assert len(analysis) > 50  # Verificar que el análisis tiene contenido sustancial


@then('el análisis incluye evolución temporal')
def step_verificar_evolucion_temporal(context):
    """Verificar que el análisis incluye evolución temporal"""
    analysis = context.response_data.get('trend_analysis', '').lower()
    assert any(keyword in analysis for keyword in ['evolución', 'evolucion', 'temporal', 'tiempo', 'tendencia']), \
        "El análisis no incluye evolución temporal"


@then('el análisis incluye interpretación de cambios')
def step_verificar_interpretacion_cambios(context):
    """Verificar que el análisis incluye interpretación de cambios"""
    analysis = context.response_data.get('trend_analysis', '').lower()
    assert any(keyword in analysis for keyword in ['cambio', 'mejora', 'empeoramiento', 'variación', 'variacion']), \
        "El análisis no incluye interpretación de cambios"


@given('que tengo un ID de paciente inexistente')
def step_id_paciente_inexistente(context):
    """Preparar un ID de paciente inexistente"""
    context.nonexistent_patient_id = str(uuid.uuid4())


@then('el análisis de tendencias falla')
def step_analisis_tendencias_falla(context):
    """Verificar que el análisis de tendencias falló"""
    assert context.status_code in [400, 404]


@then('la respuesta contiene un mensaje de error sobre paciente inexistente')
def step_verificar_error_paciente_inexistente(context):
    """Verificar mensaje de error sobre paciente inexistente"""
    response_text = json.dumps(context.response_data).lower()
    assert any(keyword in response_text for keyword in ['not found', 'no encontr', 'inexistente', 'paciente']), \
        f"No se encontró mensaje sobre paciente inexistente en: {context.response_data}"


@given('que no proporciono un patient_id')
def step_sin_patient_id(context):
    """No proporcionar patient_id"""
    context.no_patient_id = True


@given('que tengo una sola valoración PHQ-9 para un paciente')
def step_una_sola_valoracion(context):
    """Crear una sola valoración para un paciente"""
    context.execute_steps('''
        Dado que tengo los datos de una nueva valoración PHQ-9:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          | 1          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
    ''')


@then('la respuesta indica que hay 1 valoración analizada')
def step_verificar_una_valoracion_analizada(context):
    """Verificar que indica 1 valoración analizada"""
    assert context.response_data['assessments_count'] == 1


@then('el análisis incluye recomendaciones para seguimiento futuro')
def step_verificar_recomendaciones_seguimiento(context):
    """Verificar que incluye recomendaciones para seguimiento futuro"""
    analysis = context.response_data.get('trend_analysis', '').lower()
    assert any(keyword in analysis for keyword in ['seguimiento', 'futuro', 'próxima', 'proxima', 'continuar']), \
        "El análisis no incluye recomendaciones para seguimiento futuro"


# ================== CORRECCIONES PARA ANÁLISIS SIN PARÁMETROS ==================

@when('envío una solicitud POST para analizar la valoración individual')
def step_post_analizar_valoracion_corregido(context):
    """Enviar solicitud POST para análisis individual con Gemini (versión corregida)"""
    analysis_url = f"{context.base_url}/api/assessments/analyze/"
    
    if hasattr(context, 'no_assessment_id'):
        # Enviar sin assessment_id
        context.response = context.session.post(analysis_url, json={})
    elif hasattr(context, 'nonexistent_assessment_id'):
        # Enviar con ID inexistente
        context.response = context.session.post(analysis_url, json={"assessment_id": context.nonexistent_assessment_id})
    else:
        # Enviar con ID válido
        context.response = context.session.post(analysis_url, json={"assessment_id": context.created_assessment_id})
    
    context.status_code = context.response.status_code
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = {"error": "No JSON response"}


@when('envío una solicitud POST para analizar las tendencias')
def step_post_analizar_tendencias_corregido(context):
    """Enviar solicitud POST para análisis de tendencias con Gemini (versión corregida)"""
    trends_url = f"{context.base_url}/api/assessments/trends/"
    
    if hasattr(context, 'no_patient_id'):
        # Enviar sin patient_id
        context.response = context.session.post(trends_url, json={})
    elif hasattr(context, 'nonexistent_patient_id'):
        # Enviar con ID inexistente
        context.response = context.session.post(trends_url, json={"patient_id": context.nonexistent_patient_id})
    else:
        # Enviar con ID válido
        context.response = context.session.post(trends_url, json={"patient_id": context.patient_id})
    
    context.status_code = context.response.status_code
    try:
        context.response_data = context.response.json()
    except:
        context.response_data = {"error": "No JSON response"}

