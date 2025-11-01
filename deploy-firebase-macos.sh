#!/bin/bash
# Script para automatizar el despliegue de una Firebase Function en macOS
# que utiliza un paquete personalizado "musicinfo" gestionado con Poetry

set -e  # Salir si hay errores

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Directorios
ROOT_DIR="$(pwd)"
MUSICINFO_DIR="$ROOT_DIR/musicinfo"
FUNCTIONS_DIR="$ROOT_DIR/functions"
DIST_DIR="$ROOT_DIR/dist"
TEMP_DIR="$ROOT_DIR/temp"

clear
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║      MUSICINFO FIREBASE DEPLOY TOOL        ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Iniciando proceso de despliegue..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -d "$MUSICINFO_DIR" ]; then
    echo -e "${RED}${BOLD}[ERROR]${NC} No se encuentra el directorio musicinfo."
    echo -e "${YELLOW}Este script debe ejecutarse desde el directorio raíz del proyecto.${NC}"
    exit 1
fi

if [ ! -d "$FUNCTIONS_DIR" ]; then
    echo -e "${RED}${BOLD}[ERROR]${NC} No se encuentra el directorio functions."
    echo -e "${YELLOW}Este script debe ejecutarse desde el directorio raíz del proyecto.${NC}"
    exit 1
fi

# Crear directorio temporal si no existe
mkdir -p "$TEMP_DIR"

# Paso 1: Generar el paquete musicinfo usando Poetry
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║         GENERANDO PAQUETE MUSICINFO        ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Generando paquete musicinfo con Poetry..."
cd "$MUSICINFO_DIR"

# Verificar que Poetry está instalado
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}${BOLD}[ERROR]${NC} Poetry no está instalado. Por favor, instálalo primero."
    echo -e "${YELLOW}Puedes instalarlo con: curl -sSL https://install.python-poetry.org | python3 -${NC}"
    exit 1
fi

# Limpiar dist anterior para evitar confusiones
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
fi
mkdir -p "$DIST_DIR"

# Construir el paquete
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Ejecutando poetry build..."
poetry build

# Volver al directorio raíz
cd "$ROOT_DIR"

# Obtener la lista de archivos en el directorio dist
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Verificando archivos generados en dist:"
ls -lh "$DIST_DIR"

# Buscar archivos wheel en el directorio dist
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Buscando archivos wheel..."
WHEEL_FILE=$(ls "$DIST_DIR"/*.whl 2>/dev/null | head -n 1)

if [ -z "$WHEEL_FILE" ]; then
    echo -e "${RED}${BOLD}[ERROR]${NC} No se encontraron archivos wheel en el directorio dist."
    exit 1
fi

WHEEL_FILENAME=$(basename "$WHEEL_FILE")
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Archivo wheel encontrado: $WHEEL_FILENAME"

# Copiar el archivo wheel al directorio temporal y también al directorio functions
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Copiando el archivo wheel..."
cp "$WHEEL_FILE" "$TEMP_DIR/"
cp "$WHEEL_FILE" "$FUNCTIONS_DIR/"

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Archivo wheel copiado a functions/$WHEEL_FILENAME"

# Paso 2: Preparar Firebase Function
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║       PREPARANDO FIREBASE FUNCTIONS        ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Preparando Firebase Function..."
cd "$FUNCTIONS_DIR"

# Copiar el archivo .env de la raíz al directorio functions
if [ -f "$ROOT_DIR/.env" ]; then
    echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Copiando archivo .env al directorio functions..."
    cp "$ROOT_DIR/.env" "$FUNCTIONS_DIR/.env"
    echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Archivo .env copiado correctamente."
else
    echo -e "${YELLOW}${BOLD}[WARNING]${NC} No se encontró archivo .env en el directorio raíz."
fi

# Verificar si existe requirements.txt y hacer backup
if [ -f "requirements.txt" ]; then
    cp requirements.txt requirements.txt.bak
    echo -e "${YELLOW}${BOLD}[WARNING]${NC} Se ha creado una copia de seguridad del archivo requirements.txt como requirements.txt.bak"
fi

# Crear o actualizar requirements.txt
if [ -f "requirements.txt" ]; then
    # Guardar contenido actual sin líneas de musicinfo
    grep -vi "musicinfo" requirements.txt > "$TEMP_DIR/temp_req.txt" || true
    cp "$TEMP_DIR/temp_req.txt" requirements.txt
fi

# Agregar la nueva versión de musicinfo al requirements.txt (usando la copia local)
echo "$WHEEL_FILENAME" >> requirements.txt
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Se ha actualizado requirements.txt con la nueva versión de musicinfo"

# Mostrar el contenido actualizado de requirements.txt
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Contenido de requirements.txt:"
cat requirements.txt

# Crear/actualizar entorno virtual
echo ""
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Preparando entorno virtual..."

# Eliminar venv anterior si existe
if [ -d "venv" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Eliminando entorno virtual anterior..."
    rm -rf venv
fi

# Crear nuevo entorno virtual
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Creando entorno virtual con Python..."
python3 -m venv venv

# Activar entorno e instalar dependencias
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Instalando dependencias en el entorno virtual..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt
deactivate

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Entorno virtual configurado correctamente."

# Paso 3: Desplegar Firebase Function
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║         DESPLEGANDO A FIREBASE             ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Desplegando Firebase Function..."

# Verificar si Firebase CLI está instalado
if ! command -v firebase &> /dev/null; then
    echo -e "${RED}${BOLD}[ERROR]${NC} Firebase CLI no está instalado. Por favor, instálalo primero."
    echo -e "${YELLOW}Puedes instalarlo con: npm install -g firebase-tools${NC}"
    exit 1
fi

# Desplegar la función
firebase deploy --only functions

# Limpieza
echo ""
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Limpiando archivos temporales..."
if [ -f "requirements.txt.bak" ]; then
    mv requirements.txt.bak requirements.txt
    echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Restaurado el archivo requirements.txt original"
fi

echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║          DESPLIEGUE COMPLETADO             ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} ¡Despliegue completado con éxito!"
echo -e "${BLUE}[INFO]${NC} El directorio temporal '$TEMP_DIR' contiene el paquete generado."
echo -e "${BLUE}[INFO]${NC} Fecha y hora del despliegue: $(date '+%Y-%m-%d %H:%M:%S')"

echo ""
echo -e "${MAGENTA}Gracias por usar el script de despliegue automático.${NC}"
cd "$ROOT_DIR"