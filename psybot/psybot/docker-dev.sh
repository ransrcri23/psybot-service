#!/bin/bash
# Script para facilitar el desarrollo con Docker
# Uso: ./docker-dev.sh [comando]

if [ $# -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "          PsyBot Docker Development"
    echo "=========================================="
    echo ""
    echo "Comandos disponibles:"
    echo "   start     - Iniciar servicios Docker"
    echo "   stop      - Detener servicios Docker"
    echo "   restart   - Reiniciar servicios Docker"
    echo "   build     - Construir y iniciar con rebuild"
    echo "   logs      - Ver logs del backend"
    echo "   shell     - Acceder al shell del backend"
    echo "   migrate   - Ejecutar migraciones Django"
    echo "   status    - Ver estado de los servicios"
    echo "   test      - Ejecutar pruebas BDD"
    echo "   clean     - Limpiar contenedores y volúmenes"
    echo ""
    echo "Ejemplo: ./docker-dev.sh start"
    echo ""
    exit 0
fi

case $1 in
    start)
        echo "⚡ Iniciando servicios Docker..."
        docker-compose up -d
        echo "✅ Servicios iniciados"
        echo "🌐 Interfaz web: http://localhost:8000"
        echo "📚 API docs: http://localhost:8000/api/schema/swagger-ui/"
        ;;
    stop)
        echo "⏹️ Deteniendo servicios Docker..."
        docker-compose down
        echo "✅ Servicios detenidos"
        ;;
    restart)
        echo "🔄 Reiniciando servicios Docker..."
        docker-compose down
        docker-compose up -d
        echo "✅ Servicios reiniciados"
        ;;
    build)
        echo "🏗️ Construyendo y iniciando servicios..."
        docker-compose up --build -d
        echo "✅ Servicios construidos y iniciados"
        ;;
    logs)
        echo "📋 Viendo logs del backend..."
        docker-compose logs -f backend
        ;;
    shell)
        echo "🐚 Accediendo al shell del backend..."
        docker-compose exec backend /bin/bash
        ;;
    migrate)
        echo "🔄 Ejecutando migraciones Django..."
        docker-compose exec backend python manage.py migrate
        echo "✅ Migraciones completadas"
        ;;
    status)
        echo "📊 Estado de los servicios:"
        docker-compose ps
        ;;
    test)
        echo "🧪 Ejecutando pruebas BDD..."
        docker-compose exec backend behave
        ;;
    clean)
        echo "🧹 Limpiando contenedores y volúmenes..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Limpieza completada"
        ;;
    *)
        echo "❌ Comando no reconocido: $1"
        echo "Use './docker-dev.sh' para ver comandos disponibles"
        exit 1
        ;;
esac
