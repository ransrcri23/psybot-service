# Reporte de Pruebas Allure - PsyBot Service

## Resumen del Reporte

- **Total de Escenarios**: 21
- **Escenarios Exitosos**: 15 (71.4%)
- **Escenarios Fallidos**: 6 (28.6%)
- **Fecha de Generación**: 11/7/2025

## Cómo Ver el Reporte

### Opción 1: Usar Allure (Recomendado)
Si tienes Allure instalado en tu sistema:
```bash
allure open allure-report
```
Este comando abrirá automáticamente el reporte en tu navegador predeterminado.

### Opción 2: Usar Python HTTP Server
Si tienes Python instalado:
```bash
python -m http.server 8080 --directory allure-report
```
Después de ejecutar el comando, abre tu navegador y ve a: http://localhost:8080

### Opción 3: Usar Node.js HTTP Server
Si tienes Node.js instalado:
```bash
npx http-server allure-report -p 8080
```
Después de ejecutar el comando, abre tu navegador y ve a: http://localhost:8080

### Opción 4: Script Automático (Windows)
Ejecuta el archivo `open-report.bat` incluido en el paquete y selecciona una de las opciones disponibles.

## Archivos Incluidos

- `allure-report/` - Carpeta con el reporte HTML completo
- `allure-report-psybot.zip` - Archivo comprimido con todo el reporte
- `open-report.bat` - Script para abrir el reporte fácilmente (Windows)
- `REPORTE-ALLURE.md` - Este archivo de instrucciones

## Contenido del Reporte

El reporte de Allure incluye las siguientes secciones:

- **Dashboard**: Resumen general con métricas y gráficos de las pruebas
- **Suites**: Organización de pruebas por funcionalidad
- **Behaviors**: Agrupación por features de BDD (Behavior Driven Development)
- **Timeline**: Cronología de ejecución de pruebas
- **Categories**: Clasificación de fallas por tipo
- **Packages**: Estructura de archivos de pruebas

## Áreas Evaluadas

- **Creación de Pacientes**: Casos exitosos y validaciones (EXITOSO)
- **Autenticación**: Login y manejo de tokens (EXITOSO)
- **Validaciones de Campos**: Campos requeridos y formatos (EXITOSO)
- **Validación de Fechas**: Pendiente mejorar validación de fechas futuras (PENDIENTE)
- **Manejo de Errores**: Algunos casos edge pendientes (PENDIENTE)

## Para Desarrolladores

### Regenerar el Reporte
Para generar un nuevo reporte con resultados actualizados:
```bash
# Ejecutar pruebas con formato Allure
behave --format allure_behave.formatter:AllureFormatter -o allure-results

# Generar reporte HTML
allure generate allure-results --output allure-report --clean
```

### Abrir Reporte en Desarrollo
Para ver el reporte directamente durante el desarrollo:
```bash
allure serve allure-results
```
Este comando genera y sirve el reporte en tiempo real.

## Requisitos

Para ver el reporte necesitas al menos una de las siguientes herramientas instaladas:
- Allure Framework (recomendado)
- Python 3.x
- Node.js
- Cualquier servidor HTTP local

## Contacto

Para preguntas sobre el reporte o las pruebas, contacta al equipo de QA.

---
*Reporte generado automáticamente con Allure Framework*
