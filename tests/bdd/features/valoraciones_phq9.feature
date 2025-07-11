# language: es
@valoraciones @api @smoke
Característica: Gestión de Valoraciones PHQ-9
    Como psicólogo clínico
    Quiero poder crear valoraciones PHQ-9 y analizarlas con Gemini AI
    Para realizar seguimiento del estado mental de mis pacientes

    Antecedentes:
        Dado que el servicio PsyBot está disponible
        Y que tengo acceso al endpoint de valoraciones
        Y que existe un paciente de prueba para las valoraciones

    @crear_valoracion @happy_path
    Escenario: Crear una valoración PHQ-9 con datos válidos
        Dado que tengo los datos de una nueva valoración PHQ-9:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 2          | 1          | 3          | 2          | 1          | 2          | 1          | 0          | 0          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
        Y recibo un código de respuesta 201
        Y la respuesta contiene los datos de la valoración creada
        Y la valoración tiene un ID único asignado
        Y el total_score se calcula correctamente como 12
        Y la fecha de creación está establecida

    @crear_valoracion @validacion
    Escenario: Intentar crear una valoración con respuestas insuficientes
        Dado que tengo los datos de una valoración con 7 respuestas:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 |
            | 2          | 1          | 3          | 2          | 1          | 2          | 1          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la creación de la valoración falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre 9 respuestas requeridas

    @crear_valoracion @validacion
    Escenario: Intentar crear una valoración con respuestas fuera de rango
        Dado que tengo los datos de una valoración con respuestas inválidas:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 2          | 1          | 3          | 5          | 1          | 2          | 1          | 0          | 0          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la creación de la valoración falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre valores válidos

    @crear_valoracion @validacion
    Escenario: Intentar crear una valoración sin paciente_id
        Dado que tengo los datos de una valoración sin paciente_id:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 2          | 1          | 3          | 2          | 1          | 2          | 1          | 0          | 0          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la creación de la valoración falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre patient_id requerido

    @crear_valoracion @edge_cases
    Escenario: Crear una valoración con puntaje máximo
        Dado que tengo los datos de una valoración con puntaje máximo:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 3          | 3          | 3          | 3          | 3          | 3          | 3          | 3          | 3          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
        Y recibo un código de respuesta 201
        Y el total_score se calcula correctamente como 27

    @crear_valoracion @edge_cases
    Escenario: Crear una valoración con puntaje mínimo
        Dado que tengo los datos de una valoración con puntaje mínimo:
            | respuesta1 | respuesta2 | respuesta3 | respuesta4 | respuesta5 | respuesta6 | respuesta7 | respuesta8 | respuesta9 |
            | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          | 0          |
        Cuando envío una solicitud POST para crear la valoración
        Entonces la valoración se crea exitosamente
        Y recibo un código de respuesta 201
        Y el total_score se calcula correctamente como 0

    @analisis_individual @gemini @happy_path
    Escenario: Analizar una valoración individual con Gemini AI
        Dado que tengo una valoración PHQ-9 creada previamente con ID conocido
        Cuando envío una solicitud POST para analizar la valoración individual
        Entonces el análisis se genera exitosamente
        Y recibo un código de respuesta 200
        Y la respuesta contiene información del paciente
        Y la respuesta contiene información de la valoración
        Y la respuesta contiene un análisis clínico generado por Gemini
        Y el análisis incluye interpretación clínica
        Y el análisis incluye recomendaciones terapéuticas

    @analisis_individual @validacion
    Escenario: Intentar analizar una valoración inexistente
        Dado que tengo un ID de valoración inexistente
        Cuando envío una solicitud POST para analizar la valoración individual
        Entonces el análisis falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre valoración inexistente

    @analisis_individual @validacion
    Escenario: Intentar analizar sin proporcionar assessment_id
        Dado que no proporciono un assessment_id
        Cuando envío una solicitud POST para analizar la valoración individual
        Entonces el análisis falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre assessment_id requerido

    @analisis_tendencias @gemini @happy_path
    Escenario: Analizar tendencias de múltiples valoraciones
        Dado que tengo múltiples valoraciones PHQ-9 para el mismo paciente
        Cuando envío una solicitud POST para analizar las tendencias
        Entonces el análisis de tendencias se genera exitosamente
        Y recibo un código de respuesta 200
        Y la respuesta contiene información del paciente
        Y la respuesta contiene el número de valoraciones analizadas
        Y la respuesta contiene datos de todas las valoraciones
        Y la respuesta contiene un análisis de tendencias generado por Gemini
        Y el análisis incluye evolución temporal
        Y el análisis incluye interpretación de cambios

    @analisis_tendencias @validacion
    Escenario: Intentar analizar tendencias de un paciente inexistente
        Dado que tengo un ID de paciente inexistente
        Cuando envío una solicitud POST para analizar las tendencias
        Entonces el análisis de tendencias falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre paciente inexistente

    @analisis_tendencias @validacion
    Escenario: Intentar analizar tendencias sin proporcionar patient_id
        Dado que no proporciono un patient_id
        Cuando envío una solicitud POST para analizar las tendencias
        Entonces el análisis de tendencias falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre patient_id requerido

    @analisis_tendencias @edge_cases
    Escenario: Analizar tendencias con una sola valoración
        Dado que tengo una sola valoración PHQ-9 para un paciente
        Cuando envío una solicitud POST para analizar las tendencias
        Entonces el análisis de tendencias se genera exitosamente
        Y recibo un código de respuesta 200
        Y la respuesta indica que hay 1 valoración analizada
        Y el análisis incluye recomendaciones para seguimiento futuro
