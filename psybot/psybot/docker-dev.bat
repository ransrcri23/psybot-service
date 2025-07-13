@echo off
REM Script para facilitar el desarrollo con Docker
REM Uso: docker-dev.bat [comando]

if "%1"=="" (
    echo.
    echo ==========================================
    echo          PsyBot Docker Development
    echo ==========================================
    echo.
    echo Comandos disponibles:
    echo   start     - Iniciar servicios Docker
    echo   stop      - Detener servicios Docker
    echo   restart   - Reiniciar servicios Docker
    echo   build     - Construir y iniciar con rebuild
    echo   logs      - Ver logs del backend
    echo   shell     - Acceder al shell del backend
    echo   migrate   - Ejecutar migraciones Django
    echo   status    - Ver estado de los servicios
    echo   test      - Ejecutar pruebas BDD
    echo   clean     - Limpiar contenedores y volúmenes
    echo.
    echo Ejemplo: docker-dev.bat start
    echo.
    goto :eof
)

if "%1"=="start" (
    echo ⚡ Iniciando servicios Docker...
    docker-compose up -d
    echo ✅ Servicios iniciados
    echo 🌐 Interfaz web: http://localhost:8000
    echo 📚 API docs: http://localhost:8000/api/schema/swagger-ui/
    goto :eof
)

if "%1"=="stop" (
    echo ⏹️ Deteniendo servicios Docker...
    docker-compose down
    echo ✅ Servicios detenidos
    goto :eof
)

if "%1"=="restart" (
    echo 🔄 Reiniciando servicios Docker...
    docker-compose down
    docker-compose up -d
    echo ✅ Servicios reiniciados
    goto :eof
)

if "%1"=="build" (
    echo 🏗️ Construyendo y iniciando servicios...
    docker-compose up --build -d
    echo ✅ Servicios construidos y iniciados
    goto :eof
)

if "%1"=="logs" (
    echo 📋 Viendo logs del backend...
    docker-compose logs -f backend
    goto :eof
)

if "%1"=="shell" (
    echo 🐚 Accediendo al shell del backend...
    docker-compose exec backend /bin/bash
    goto :eof
)

if "%1"=="migrate" (
    echo 🔄 Ejecutando migraciones Django...
    docker-compose exec backend python manage.py migrate
    echo ✅ Migraciones completadas
    goto :eof
)

if "%1"=="status" (
    echo 📊 Estado de los servicios:
    docker-compose ps
    goto :eof
)

if "%1"=="test" (
    echo 🧪 Ejecutando pruebas BDD...
    docker-compose exec backend behave
    goto :eof
)

if "%1"=="clean" (
    echo 🧹 Limpiando contenedores y volúmenes...
    docker-compose down -v
    docker system prune -f
    echo ✅ Limpieza completada
    goto :eof
)

echo ❌ Comando no reconocido: %1
echo Use 'docker-dev.bat' para ver comandos disponibles
