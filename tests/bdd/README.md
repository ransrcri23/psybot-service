# Pruebas BDD para PsyBot

Este directorio contiene las pruebas de Behavior Driven Development (BDD) para el sistema PsyBot, utilizando behave y Allure para reportes.

## Estructura del Proyecto

```
tests/bdd/
├── features/
│   ├── crear_paciente.feature      # Escenarios para crear pacientes
│   ├── environment.py              # Configuración del entorno
│   └── steps/
│       └── crear_paciente_steps.py # Implementación de los steps
├── reports/                        # Reportes generados
│   ├── allure-results/            # Resultados raw de Allure
│   ├── allure-report/             # Reporte HTML de Allure
│   └── junit/                     # Reportes JUnit
├── behave.ini                     # Configuración de behave
└── README.md                      # Esta documentación
```

## Instalación de Dependencias

1. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

2. Instalar Allure CLI (opcional, para reportes HTML):

### Windows (con Scoop):
```powershell
scoop install allure
```

### macOS (con Homebrew):
```bash
brew install allure
```

### Manual:
Descargar desde: https://github.com/allure-framework/allure2/releases

## Ejecución de Pruebas

### Método 1: Usando el script Python

```bash
# Ejecutar todas las pruebas
python run_bdd_tests.py

# Ejecutar solo pruebas con tag específico
python run_bdd_tests.py --tags @smoke

# Ejecutar feature específico
python run_bdd_tests.py --feature crear_paciente.feature

# Ejecutar sin generar reporte Allure
python run_bdd_tests.py --no-report

# Ejecutar y abrir reporte automáticamente
python run_bdd_tests.py --open
```

### Método 2: Usando behave directamente

```bash
# Ejecutar todas las pruebas
behave tests/bdd/features/

# Ejecutar con tags específicos
behave tests/bdd/features/ --tags @crear_paciente

# Ejecutar feature específico
behave tests/bdd/features/crear_paciente.feature

# Ejecutar con formato específico
behave tests/bdd/features/ --format allure_behave.formatter:AllureFormatter --outdir tests/bdd/reports/allure-results
```

## Tags Disponibles

- `@pacientes` - Pruebas relacionadas con gestión de pacientes
- `@api` - Pruebas de API
- `@smoke` - Pruebas críticas de funcionalidad básica
- `@crear_paciente` - Pruebas específicas de creación de pacientes
- `@validacion` - Pruebas de validación de datos
- `@happy_path` - Escenarios de casos exitosos
- `@edge_cases` - Casos límite

## Escenarios Implementados

### Crear Paciente
- **Crear un paciente con datos válidos** - Escenario exitoso básico
- **Intentar crear un paciente sin nombre** - Validación de campo requerido
- **Intentar crear un paciente sin apellido** - Validación de campo requerido
- **Intentar crear un paciente sin identificación** - Validación de campo requerido
- **Intentar crear un paciente con identificación duplicada** - Validación de unicidad
- **Intentar crear un paciente con fecha de nacimiento inválida** - Validación de fecha
- **Crear un paciente con nombre y apellido largos** - Caso límite de longitud
- **Crear un paciente mayor de edad** - Caso límite de edad

## Reportes

### Allure Reports
Los reportes de Allure proporcionan:
- Vista general de resultados de pruebas
- Detalles de cada escenario ejecutado
- Capturas de pantalla y logs
- Gráficos de tendencias
- Métricas de cobertura

Para generar y ver el reporte:
```bash
allure generate tests/bdd/reports/allure-results --output tests/bdd/reports/allure-report --clean
allure open tests/bdd/reports/allure-report
```

### JUnit Reports
Los reportes JUnit son útiles para integración con CI/CD:
- Ubicación: `tests/bdd/reports/junit/`
- Formato estándar XML
- Compatible con Jenkins, GitLab CI, etc.

## Configuración del Entorno

### Variables de Entorno
El archivo `environment.py` configura:
- URL base del servicio: `http://localhost:8000`
- Headers por defecto
- Sesión de requests
- Limpieza automática de datos de prueba

### Requisitos Previos
- Servicio PsyBot ejecutándose en `http://localhost:8000`
- Base de datos MongoDB disponible
- Acceso a todos los endpoints de la API

## Escritura de Nuevas Pruebas

### 1. Crear un nuevo archivo .feature
```gherkin
# language: es
@nueva_funcionalidad @api
Característica: Nueva Funcionalidad
    Como usuario
    Quiero hacer algo
    Para obtener un beneficio

    Escenario: Hacer algo exitosamente
        Dado que tengo los datos necesarios
        Cuando ejecuto la acción
        Entonces obtengo el resultado esperado
```

### 2. Implementar los steps
```python
@given('que tengo los datos necesarios')
def step_datos_necesarios(context):
    # Implementación del step
    pass

@when('ejecuto la acción')
def step_ejecutar_accion(context):
    # Implementación del step
    pass

@then('obtengo el resultado esperado')
def step_resultado_esperado(context):
    # Implementación del step
    pass
```

### 3. Agregar tags apropiados
- Usar tags descriptivos
- Agrupar por funcionalidad
- Incluir nivel de criticidad

## Buenas Prácticas

1. **Nomenclatura Clara**: Usar nombres descriptivos en escenarios y steps
2. **Datos de Prueba**: Limpiar datos automáticamente después de cada escenario
3. **Assertions Específicas**: Verificar comportamientos específicos, no solo códigos de estado
4. **Reutilización**: Crear steps reutilizables para acciones comunes
5. **Documentación**: Mantener documentación actualizada

## Solución de Problemas

### Servicio no disponible
```
AssertionError: No se puede conectar al servicio PsyBot
```
**Solución**: Verificar que el servicio esté ejecutándose en `http://localhost:8000`

### Error de dependencias
```
ModuleNotFoundError: No module named 'behave'
```
**Solución**: Instalar dependencias con `pip install -r requirements.txt`

### Error de Allure
```
FileNotFoundError: allure
```
**Solución**: Instalar Allure CLI según las instrucciones de instalación

### Datos de prueba persistentes
Si los datos de prueba no se limpian automáticamente, verificar:
- Configuración en `environment.py`
- Implementación del método `cleanup_patient`
- Permisos de eliminación en la API
