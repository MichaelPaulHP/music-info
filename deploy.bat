@echo off
REM Script para automatizar el despliegue de una Firebase Function en Windows
REM que utiliza un paquete personalizado "musicinfo" gestionado con Poetry

setlocal enabledelayedexpansion

REM Colores para los mensajes (funciona en Windows 10 y superior)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "BOLD=[1m"
set "NC=[0m"

REM Directorios
set "ROOT_DIR=%cd%"
set "MUSICINFO_DIR=%ROOT_DIR%\musicinfo"
set "FUNCTIONS_DIR=%ROOT_DIR%\functions"
set "DIST_DIR=%ROOT_DIR%\dist"
set "TEMP_DIR=%ROOT_DIR%\temp"

cls
echo %CYAN%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %CYAN%%BOLD%║      MUSICINFO FIREBASE DEPLOY TOOL        ║%NC%
echo %CYAN%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.

echo %GREEN%%BOLD%[DEPLOY]%NC% Iniciando proceso de despliegue...
echo.

REM Verificar que estamos en el directorio correcto
if not exist "%MUSICINFO_DIR%" (
    echo %RED%%BOLD%[ERROR]%NC% No se encuentra el directorio musicinfo.
    echo %YELLOW%Este script debe ejecutarse desde el directorio raíz del proyecto.%NC%
    goto :error
)

if not exist "%FUNCTIONS_DIR%" (
    echo %RED%%BOLD%[ERROR]%NC% No se encuentra el directorio functions.
    echo %YELLOW%Este script debe ejecutarse desde el directorio raíz del proyecto.%NC%
    goto :error
)

REM Crear directorio temporal si no existe
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Paso 1: Generar el paquete musicinfo usando Poetry
echo.
echo %CYAN%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %CYAN%%BOLD%║         GENERANDO PAQUETE MUSICINFO        ║%NC%
echo %CYAN%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.

echo %GREEN%%BOLD%[DEPLOY]%NC% Generando paquete musicinfo con Poetry...
cd "%MUSICINFO_DIR%"

REM Verificar que Poetry está instalado
where poetry >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo %RED%%BOLD%[ERROR]%NC% Poetry no está instalado. Por favor, instálalo primero.
    goto :error
)

REM Limpiar dist anterior para evitar confusiones
if exist "%DIST_DIR%" rd /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

REM Construir el paquete
echo %GREEN%%BOLD%[DEPLOY]%NC% Ejecutando poetry build...
poetry build

REM Volver al directorio raíz
cd "%ROOT_DIR%"

REM Obtener la lista de archivos en el directorio dist
echo %GREEN%%BOLD%[DEPLOY]%NC% Verificando archivos generados en dist:
dir "%DIST_DIR%"

REM Buscar archivos wheel en el directorio dist
echo %GREEN%%BOLD%[DEPLOY]%NC% Buscando archivos wheel...
dir /b "%DIST_DIR%\*.whl" > "%TEMP_DIR%\wheel_files.txt"

REM Leer el primer archivo de la lista
set "WHEEL_FILE="
for /f "delims=" %%i in (%TEMP_DIR%\wheel_files.txt) do (
    if "!WHEEL_FILE!"=="" set "WHEEL_FILE=%%i"
)

if "!WHEEL_FILE!"=="" (
    echo %RED%%BOLD%[ERROR]%NC% No se encontraron archivos wheel en el directorio dist.
    goto :error
)

echo %GREEN%%BOLD%[DEPLOY]%NC% Archivo wheel encontrado: !WHEEL_FILE!

REM Copiar el archivo wheel al directorio temporal y también al directorio functions
echo %GREEN%%BOLD%[DEPLOY]%NC% Copiando el archivo wheel...
copy "%DIST_DIR%\!WHEEL_FILE!" "%TEMP_DIR%\"
copy "%DIST_DIR%\!WHEEL_FILE!" "%FUNCTIONS_DIR%\"
if %ERRORLEVEL% neq 0 (
    echo %RED%%BOLD%[ERROR]%NC% Error al copiar el archivo wheel.
    goto :error
)

echo %GREEN%%BOLD%[DEPLOY]%NC% Archivo wheel copiado a functions/!WHEEL_FILE!

REM Paso 2: Preparar Firebase Function
echo.
echo %CYAN%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %CYAN%%BOLD%║       PREPARANDO FIREBASE FUNCTIONS        ║%NC%
echo %CYAN%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.

echo %GREEN%%BOLD%[DEPLOY]%NC% Preparando Firebase Function...
cd "%FUNCTIONS_DIR%"

REM Copiar el archivo .env de la raíz al directorio functions
if exist "%ROOT_DIR%\.env" (
    echo %GREEN%%BOLD%[DEPLOY]%NC% Copiando archivo .env al directorio functions...
    copy "%ROOT_DIR%\.env" "%FUNCTIONS_DIR%\.env" >nul
    echo %GREEN%%BOLD%[DEPLOY]%NC% Archivo .env copiado correctamente.
) else (
    echo %YELLOW%%BOLD%[WARNING]%NC% No se encontró archivo .env en el directorio raíz.
)

REM Verificar si existe requirements.txt y hacer backup
if exist "requirements.txt" (
    copy requirements.txt requirements.txt.bak >nul
    echo %YELLOW%%BOLD%[WARNING]%NC% Se ha creado una copia de seguridad del archivo requirements.txt como requirements.txt.bak
)

REM Crear o actualizar requirements.txt
if exist "requirements.txt" (
    REM Guardar contenido actual en archivo temporal sin líneas de musicinfo
    type nul > "%TEMP_DIR%\temp_req.txt"
    for /f "tokens=*" %%a in (requirements.txt) do (
        echo %%a | findstr /i "musicinfo" >nul
        if errorlevel 1 (
            echo %%a>> "%TEMP_DIR%\temp_req.txt"
        )
    )

    REM Copiar el contenido actualizado de vuelta a requirements.txt
    copy "%TEMP_DIR%\temp_req.txt" requirements.txt >nul
)

REM Agregar la nueva versión de musicinfo al requirements.txt (usando la copia local)
echo !WHEEL_FILE!>> requirements.txt
echo %GREEN%%BOLD%[DEPLOY]%NC% Se ha actualizado requirements.txt con la nueva versión de musicinfo

REM Mostrar el contenido actualizado de requirements.txt
echo %GREEN%%BOLD%[DEPLOY]%NC% Contenido de requirements.txt:
type requirements.txt

REM Paso 3: Desplegar Firebase Function
echo.
echo %CYAN%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %CYAN%%BOLD%║         DESPLEGANDO A FIREBASE             ║%NC%
echo %CYAN%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.

echo %GREEN%%BOLD%[DEPLOY]%NC% Desplegando Firebase Function...

REM Verificar si Firebase CLI está instalado
where firebase >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo %RED%%BOLD%[ERROR]%NC% Firebase CLI no está instalado. Por favor, instálalo primero.
    goto :error
)

REM Desplegar la función
firebase deploy --only functions
if %ERRORLEVEL% neq 0 (
    echo %RED%%BOLD%[ERROR]%NC% Error al desplegar Firebase Functions
    goto :error
)

REM Limpieza
echo.
echo %GREEN%%BOLD%[DEPLOY]%NC% Limpiando archivos temporales...
if exist "requirements.txt.bak" (
    move /y requirements.txt.bak requirements.txt >nul
    echo %GREEN%%BOLD%[DEPLOY]%NC% Restaurado el archivo requirements.txt original
)

echo.
echo %CYAN%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %CYAN%%BOLD%║          DESPLIEGUE COMPLETADO             ║%NC%
echo %CYAN%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.
echo %GREEN%%BOLD%[DEPLOY]%NC% ¡Despliegue completado con éxito!
echo %BLUE%[INFO]%NC% El directorio temporal '%TEMP_DIR%' contiene el paquete generado.
echo %BLUE%[INFO]%NC% Fecha y hora del despliegue: %date% %time%

goto :end

:error
echo.
echo %RED%%BOLD%╔════════════════════════════════════════════╗%NC%
echo %RED%%BOLD%║            ERROR DE DESPLIEGUE             ║%NC%
echo %RED%%BOLD%╚════════════════════════════════════════════╝%NC%
echo.
echo %RED%%BOLD%[ERROR]%NC% El proceso de despliegue ha fallado.
cd "%ROOT_DIR%"
exit /b 1

:end
echo.
echo %MAGENTA%Gracias por usar el script de despliegue automático.%NC%
cd "%ROOT_DIR%"
exit /b 0