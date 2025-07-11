# language: es
@pacientes @api @smoke
Característica: Gestión de Pacientes
    Como psicólogo clínico
    Quiero poder crear y gestionar pacientes en el sistema PsyBot
    Para poder realizar seguimiento de sus valoraciones PHQ-9

    Antecedentes:
        Dado que el servicio PsyBot está disponible
        Y que tengo acceso al endpoint de pacientes

    @crear_paciente @happy_path
    Escenario: Crear un paciente con datos válidos
        Dado que tengo los datos de un nuevo paciente:
            | nombre     | apellido | identificacion | fecha_nacimiento |
            | Juan       | Pérez    | 123456789      | 1990-05-15       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces el paciente se crea exitosamente
        Y recibo un código de respuesta 201
        Y la respuesta contiene los datos del paciente creado
        Y el paciente tiene un ID único asignado
        Y la fecha de creación está establecida

    @crear_paciente @validacion
    Escenario: Intentar crear un paciente sin nombre
        Dado que tengo los datos de un paciente sin nombre:
            | apellido | identificacion | fecha_nacimiento |
            | García   | 987654321      | 1985-03-20       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces la creación del paciente falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre el nombre requerido

    @crear_paciente @validacion
    Escenario: Intentar crear un paciente sin apellido
        Dado que tengo los datos de un paciente sin apellido:
            | nombre | identificacion | fecha_nacimiento |
            | María  | 456789123      | 1992-08-10       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces la creación del paciente falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre el apellido requerido

    @crear_paciente @validacion
    Escenario: Intentar crear un paciente sin identificación
        Dado que tengo los datos de un paciente sin identificación:
            | nombre | apellido | fecha_nacimiento |
            | Carlos | López    | 1988-12-05       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces la creación del paciente falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre la identificación requerida

    @crear_paciente @validacion
    Escenario: Intentar crear un paciente con identificación duplicada
        Dado que existe un paciente con identificación "555666777"
        Y que tengo los datos de un nuevo paciente con la misma identificación:
            | nombre | apellido | identificacion | fecha_nacimiento |
            | Pedro  | Martínez | 555666777      | 1995-01-25       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces la creación del paciente falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre identificación duplicada

    @crear_paciente @validacion
    Escenario: Intentar crear un paciente con fecha de nacimiento inválida
        Dado que tengo los datos de un paciente con fecha de nacimiento inválida:
            | nombre  | apellido  | identificacion | fecha_nacimiento |
            | Ana     | Rodríguez | 111222333      | 2025-12-31       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces la creación del paciente falla
        Y recibo un código de respuesta 400
        Y la respuesta contiene un mensaje de error sobre la fecha de nacimiento

    @crear_paciente @edge_cases
    Escenario: Crear un paciente con nombre y apellido largos
        Dado que tengo los datos de un paciente con nombres largos:
            | nombre                                              | apellido                                            | identificacion | fecha_nacimiento |
            | María Fernanda Alejandra Esperanza                  | González Rodríguez de la Torre y Mendoza           | 999888777      | 1987-06-18       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces el paciente se crea exitosamente
        Y recibo un código de respuesta 201
        Y la respuesta contiene los datos del paciente con nombres largos

    @crear_paciente @edge_cases
    Escenario: Crear un paciente mayor de edad
        Dado que tengo los datos de un paciente mayor de edad:
            | nombre    | apellido | identificacion | fecha_nacimiento |
            | Esperanza | Jiménez  | 777666555      | 1940-04-12       |
        Cuando envío una solicitud POST para crear el paciente
        Entonces el paciente se crea exitosamente
        Y recibo un código de respuesta 201
        Y el paciente tiene más de 80 años
