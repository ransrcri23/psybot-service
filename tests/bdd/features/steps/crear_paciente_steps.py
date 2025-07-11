"""
Step definitions para los escenarios de crear paciente
"""

import json
import uuid
from datetime import datetime, date
from behave import given, when, then, step
import requests
import allure


@given('que el servicio PsyBot está disponible')
def step_servicio_disponible(context):
    """Verificar que el servicio esté disponible"""
    with allure.step("Verificar disponibilidad del servicio PsyBot"):
        try:
            response = context.session.get(f"{context.base_url}/api/pacientes/")
            assert response.status_code in [200, 404], f"Servicio no disponible. Status: {response.status_code}"
            allure.attach(f"Servicio disponible - Status: {response.status_code}", name="Estado del servicio")
        except requests.exceptions.ConnectionError:
            raise AssertionError("No se puede conectar al servicio PsyBot. Asegúrate de que esté ejecutándose.")


@given('que tengo acceso al endpoint de pacientes')
def step_acceso_endpoint_pacientes(context):
    """Verificar acceso al endpoint de pacientes"""
    with allure.step("Verificar acceso al endpoint de pacientes"):
        context.pacientes_url = f"{context.base_url}/api/pacientes/"
        allure.attach(context.pacientes_url, name="URL del endpoint")


@given('que tengo los datos de un nuevo paciente')
def step_datos_nuevo_paciente(context):
    """Preparar datos de un nuevo paciente desde la tabla"""
    with allure.step("Preparar datos del nuevo paciente"):
        row = context.table[0]
        # Generar identificación única para evitar conflictos
        unique_id = f"{row['identificacion']}-{uuid.uuid4().hex[:8]}"
        context.patient_data = {
            "nombre": row['nombre'],
            "apellido": row['apellido'],
            "identificacion": unique_id,
            "fecha_nacimiento": row['fecha_nacimiento']
        }
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos del paciente", attachment_type=allure.attachment_type.JSON)


@given('que tengo los datos de un paciente sin {campo}')
def step_datos_paciente_sin_campo(context, campo):
    """Preparar datos de paciente sin un campo específico"""
    with allure.step(f"Preparar datos del paciente sin {campo}"):
        row = context.table[0]
        context.patient_data = {}
        
        # Mapear nombres de campos
        campo_mapping = {
            'nombre': 'nombre',
            'apellido': 'apellido',
            'identificación': 'identificacion'
        }
        
        # Agregar todos los campos disponibles excepto el que falta
        for key in row.headings:
            if key != campo_mapping.get(campo, campo):
                context.patient_data[key] = row[key]
        
        allure.attach(json.dumps(context.patient_data, indent=2), name=f"Datos sin {campo}", attachment_type=allure.attachment_type.JSON)


@given('que tengo los datos de un paciente con fecha de nacimiento inválida')
def step_datos_paciente_fecha_invalida(context):
    """Preparar datos con fecha de nacimiento en el futuro"""
    with allure.step("Preparar datos con fecha de nacimiento inválida"):
        row = context.table[0]
        context.patient_data = {
            "nombre": row['nombre'],
            "apellido": row['apellido'],
            "identificacion": row['identificacion'],
            "fecha_nacimiento": row['fecha_nacimiento']  # Fecha en el futuro
        }
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos con fecha inválida", attachment_type=allure.attachment_type.JSON)


@given('que tengo los datos de un paciente con nombres largos')
def step_datos_paciente_nombres_largos(context):
    """Preparar datos con nombres muy largos"""
    with allure.step("Preparar datos con nombres largos"):
        row = context.table[0]
        unique_id = f"{row['identificacion']}-{uuid.uuid4().hex[:8]}"
        context.patient_data = {
            "nombre": row['nombre'],
            "apellido": row['apellido'],
            "identificacion": unique_id,
            "fecha_nacimiento": row['fecha_nacimiento']
        }
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos con nombres largos", attachment_type=allure.attachment_type.JSON)


@given('que tengo los datos de un paciente mayor de edad')
def step_datos_paciente_mayor_edad(context):
    """Preparar datos de paciente mayor de edad"""
    with allure.step("Preparar datos de paciente mayor de edad"):
        row = context.table[0]
        unique_id = f"{row['identificacion']}-{uuid.uuid4().hex[:8]}"
        context.patient_data = {
            "nombre": row['nombre'],
            "apellido": row['apellido'],
            "identificacion": unique_id,
            "fecha_nacimiento": row['fecha_nacimiento']
        }
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos de paciente mayor", attachment_type=allure.attachment_type.JSON)


@given('que existe un paciente con identificación "{identificacion}"')
def step_crear_paciente_existente(context, identificacion):
    """Crear un paciente con la identificación especificada"""
    with allure.step(f"Crear paciente existente con identificación {identificacion}"):
        existing_patient = {
            "nombre": "Paciente",
            "apellido": "Existente",
            "identificacion": identificacion,
            "fecha_nacimiento": "1990-01-01"
        }
        
        response = context.session.post(
            context.pacientes_url,
            json=existing_patient,
            headers=context.headers
        )
        
        if response.status_code == 201:
            patient_id = response.json().get('id')
            if not hasattr(context, 'created_in_scenario'):
                context.created_in_scenario = []
            context.created_in_scenario.append(patient_id)
            context.created_patients.append(patient_id)
            allure.attach(f"Paciente creado con ID: {patient_id}", name="Paciente existente creado")


@given('que tengo los datos de un nuevo paciente con la misma identificación')
def step_datos_paciente_identificacion_duplicada(context):
    """Preparar datos con identificación duplicada"""
    with allure.step("Preparar datos con identificación duplicada"):
        row = context.table[0]
        context.patient_data = {
            "nombre": row['nombre'],
            "apellido": row['apellido'],
            "identificacion": row['identificacion'],
            "fecha_nacimiento": row['fecha_nacimiento']
        }
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos con ID duplicado", attachment_type=allure.attachment_type.JSON)


@when('envío una solicitud POST para crear el paciente')
def step_enviar_post_crear_paciente(context):
    """Enviar solicitud POST para crear paciente"""
    with allure.step("Enviar solicitud POST para crear paciente"):
        allure.attach(context.pacientes_url, name="URL de destino")
        allure.attach(json.dumps(context.patient_data, indent=2), name="Datos enviados", attachment_type=allure.attachment_type.JSON)
        
        context.response = context.session.post(
            context.pacientes_url,
            json=context.patient_data,
            headers=context.headers
        )
        
        context.status_code = context.response.status_code
        
        try:
            context.response_data = context.response.json()
        except json.JSONDecodeError:
            context.response_data = {"error": "Respuesta no es JSON válido", "text": context.response.text}
        
        allure.attach(f"Status Code: {context.status_code}", name="Código de respuesta")
        allure.attach(json.dumps(context.response_data, indent=2), name="Respuesta recibida", attachment_type=allure.attachment_type.JSON)


@then('el paciente se crea exitosamente')
def step_paciente_creado_exitosamente(context):
    """Verificar que el paciente se creó exitosamente"""
    with allure.step("Verificar creación exitosa del paciente"):
        assert context.status_code == 201, f"Se esperaba status 201, pero se recibió {context.status_code}"
        assert context.response_data is not None, "No se recibió respuesta"
        
        # Guardar ID del paciente creado para limpieza
        if 'id' in context.response_data:
            patient_id = context.response_data['id']
            if not hasattr(context, 'created_in_scenario'):
                context.created_in_scenario = []
            context.created_in_scenario.append(patient_id)
            context.created_patients.append(patient_id)
            allure.attach(f"Paciente creado con ID: {patient_id}", name="ID del paciente creado")


@then('la creación del paciente falla')
def step_creacion_paciente_falla(context):
    """Verificar que la creación del paciente falló"""
    with allure.step("Verificar que la creación falló"):
        assert context.status_code != 201, f"Se esperaba un error, pero se creó exitosamente con status {context.status_code}"
        allure.attach(f"Creación falló correctamente con status: {context.status_code}", name="Resultado esperado")


@then('recibo un código de respuesta {codigo:d}')
def step_verificar_codigo_respuesta(context, codigo):
    """Verificar el código de respuesta específico"""
    with allure.step(f"Verificar código de respuesta {codigo}"):
        assert context.status_code == codigo, f"Se esperaba status {codigo}, pero se recibió {context.status_code}"
        allure.attach(f"Código correcto: {context.status_code}", name="Verificación de status")


@then('la respuesta contiene los datos del paciente creado')
def step_verificar_datos_paciente_creado(context):
    """Verificar que la respuesta contiene los datos del paciente"""
    with allure.step("Verificar datos del paciente en la respuesta"):
        assert 'nombre' in context.response_data, "Falta el campo 'nombre' en la respuesta"
        assert 'apellido' in context.response_data, "Falta el campo 'apellido' en la respuesta"
        assert 'identificacion' in context.response_data, "Falta el campo 'identificacion' en la respuesta"
        assert 'fecha_nacimiento' in context.response_data, "Falta el campo 'fecha_nacimiento' en la respuesta"
        
        # Verificar que los datos coincidan
        assert context.response_data['nombre'] == context.patient_data['nombre'], "El nombre no coincide"
        assert context.response_data['apellido'] == context.patient_data['apellido'], "El apellido no coincide"
        assert context.response_data['identificacion'] == context.patient_data['identificacion'], "La identificación no coincide"
        
        allure.attach("Todos los datos del paciente están presentes y son correctos", name="Verificación de datos")


@then('el paciente tiene un ID único asignado')
def step_verificar_id_unico(context):
    """Verificar que el paciente tiene un ID único"""
    with allure.step("Verificar ID único del paciente"):
        assert 'id' in context.response_data, "Falta el campo 'id' en la respuesta"
        assert context.response_data['id'] is not None, "El ID no puede ser nulo"
        
        # Verificar que es un UUID válido
        try:
            uuid.UUID(context.response_data['id'])
            allure.attach(f"ID válido: {context.response_data['id']}", name="ID único verificado")
        except ValueError:
            raise AssertionError(f"El ID no es un UUID válido: {context.response_data['id']}")


@then('la fecha de creación está establecida')
def step_verificar_fecha_creacion(context):
    """Verificar que la fecha de creación está establecida"""
    with allure.step("Verificar fecha de creación"):
        assert 'fecha_creacion' in context.response_data, "Falta el campo 'fecha_creacion' en la respuesta"
        
        fecha_creacion = context.response_data['fecha_creacion']
        assert fecha_creacion is not None, "La fecha de creación no puede ser nula"
        
        # Verificar que es una fecha válida de hoy
        try:
            if isinstance(fecha_creacion, str):
                fecha_creacion = datetime.fromisoformat(fecha_creacion.replace('Z', '+00:00')).date()
            
            hoy = date.today()
            assert fecha_creacion == hoy, f"La fecha de creación {fecha_creacion} no es de hoy {hoy}"
            allure.attach(f"Fecha de creación correcta: {fecha_creacion}", name="Fecha de creación verificada")
        except (ValueError, TypeError) as e:
            raise AssertionError(f"Formato de fecha inválido: {fecha_creacion}. Error: {e}")


@then('la respuesta contiene un mensaje de error sobre el {campo} requerido')
def step_verificar_mensaje_error_campo(context, campo):
    """Verificar mensaje de error sobre campo requerido"""
    with allure.step(f"Verificar mensaje de error sobre {campo} requerido"):
        assert context.response_data is not None, "No se recibió respuesta"
        
        # El mensaje puede estar en diferentes formatos dependiendo del serializer
        response_text = json.dumps(context.response_data).lower()
        campo_lower = campo.lower()
        
        # Verificar que el mensaje menciona el campo faltante
        assert any(keyword in response_text for keyword in [campo_lower, 'required', 'requerido', 'obligatorio']), \
            f"No se encontró mensaje de error sobre {campo} en: {context.response_data}"
        
        allure.attach(f"Error sobre {campo} encontrado en la respuesta", name="Mensaje de error verificado")


@then('la respuesta contiene un mensaje de error sobre identificación duplicada')
def step_verificar_mensaje_error_duplicado(context):
    """Verificar mensaje de error sobre identificación duplicada"""
    with allure.step("Verificar mensaje de error sobre identificación duplicada"):
        assert context.response_data is not None, "No se recibió respuesta"
        
        response_text = json.dumps(context.response_data).lower()
        
        # Verificar que el mensaje menciona duplicado o unique
        assert any(keyword in response_text for keyword in ['duplicate', 'duplicado', 'unique', 'único', 'already exists', 'ya existe']), \
            f"No se encontró mensaje de error sobre duplicado en: {context.response_data}"
        
        allure.attach("Error sobre identificación duplicada encontrado", name="Mensaje de duplicado verificado")


@then('la respuesta contiene un mensaje de error sobre la fecha de nacimiento')
def step_verificar_mensaje_error_fecha(context):
    """Verificar mensaje de error sobre fecha de nacimiento"""
    with allure.step("Verificar mensaje de error sobre fecha de nacimiento"):
        assert context.response_data is not None, "No se recibió respuesta"
        
        response_text = json.dumps(context.response_data).lower()
        
        # Verificar que el mensaje menciona la fecha
        assert any(keyword in response_text for keyword in ['fecha', 'date', 'birth', 'nacimiento', 'future', 'futuro']), \
            f"No se encontró mensaje de error sobre fecha en: {context.response_data}"
        
        allure.attach("Error sobre fecha de nacimiento encontrado", name="Mensaje de fecha verificado")


@then('la respuesta contiene los datos del paciente con nombres largos')
def step_verificar_datos_nombres_largos(context):
    """Verificar que los nombres largos se guardaron correctamente"""
    with allure.step("Verificar datos con nombres largos"):
        assert context.response_data['nombre'] == context.patient_data['nombre'], "El nombre largo no se guardó correctamente"
        assert context.response_data['apellido'] == context.patient_data['apellido'], "El apellido largo no se guardó correctamente"
        
        allure.attach(f"Nombre: {context.response_data['nombre']}", name="Nombre largo verificado")
        allure.attach(f"Apellido: {context.response_data['apellido']}", name="Apellido largo verificado")


@then('el paciente tiene más de {edad:d} años')
def step_verificar_edad_paciente(context, edad):
    """Verificar la edad del paciente"""
    with allure.step(f"Verificar que el paciente tiene más de {edad} años"):
        fecha_nacimiento = datetime.strptime(context.patient_data['fecha_nacimiento'], '%Y-%m-%d').date()
        hoy = date.today()
        edad_calculada = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        assert edad_calculada > edad, f"El paciente tiene {edad_calculada} años, no más de {edad}"
        allure.attach(f"Edad calculada: {edad_calculada} años", name="Edad verificada")


@then('la respuesta contiene un mensaje de error sobre la identificación requerida')
def step_verificar_error_identificacion_requerida(context):
    """Verificar que la respuesta contiene un mensaje de error sobre la identificación requerida"""
    with allure.step("Verificar mensaje de error sobre identificación requerida"):
        assert context.response_data is not None, "No se recibió respuesta"
        
        response_text = json.dumps(context.response_data).lower()
        assert any(keyword in response_text for keyword in ['identificacion', 'identification', 'required', 'requerida', 'this field']), \
            f"No se encontró mensaje de error sobre identificación requerida en: {context.response_data}"
        
        allure.attach("Error sobre identificación requerida encontrado", name="Mensaje de identificación verificado")
