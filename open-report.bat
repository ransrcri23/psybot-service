@echo off
echo Abriendo reporte de pruebas Allure...
echo.
echo Opcion 1: Usar Allure serve (requiere Allure instalado)
echo allure open allure-report
echo.
echo Opcion 2: Usar servidor HTTP simple con Python
echo python -m http.server 8080 --directory allure-report
echo.
echo Opcion 3: Usar servidor HTTP simple con Node.js
echo npx http-server allure-report -p 8080
echo.
echo Seleccione una opcion:
echo 1) Allure serve
echo 2) Python HTTP server
echo 3) Node.js HTTP server
echo 4) Solo mostrar instrucciones
echo.
set /p choice="Ingrese su opcion (1-4): "

if "%choice%"=="1" (
    allure open allure-report
) else if "%choice%"=="2" (
    echo Iniciando servidor Python en http://localhost:8080
    python -m http.server 8080 --directory allure-report
) else if "%choice%"=="3" (
    echo Iniciando servidor Node.js en http://localhost:8080
    npx http-server allure-report -p 8080
) else (
    echo.
    echo === INSTRUCCIONES PARA VER EL REPORTE ===
    echo.
    echo 1. Si tienes Allure instalado:
    echo    allure open allure-report
    echo.
    echo 2. Si tienes Python instalado:
    echo    python -m http.server 8080 --directory allure-report
    echo    Luego abre: http://localhost:8080
    echo.
    echo 3. Si tienes Node.js instalado:
    echo    npx http-server allure-report -p 8080
    echo    Luego abre: http://localhost:8080
    echo.
    echo 4. Alternativamente, puedes usar cualquier servidor HTTP local
    echo    que apunte a la carpeta 'allure-report'
    echo.
)

pause
