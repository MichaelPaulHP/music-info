
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

# Leer versión del pyproject.toml
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Leyendo versión del proyecto..."
if [ -f "$ROOT_DIR/pyproject.toml" ]; then
    PROJECT_VERSION=$(grep '^version = ' "$ROOT_DIR/pyproject.toml" | sed 's/version = "\(.*\)"/\1/')
    echo -e "${BLUE}[INFO]${NC} Versión del proyecto: ${BOLD}v$PROJECT_VERSION${NC}"
else
    echo -e "${YELLOW}${BOLD}[WARNING]${NC} No se encontró pyproject.toml, no se podrá generar el mensaje de commit automático."
    PROJECT_VERSION=""
fi

# Paso 1: Verificar variables de entorno
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║      VERIFICANDO VARIABLES DE ENTORNO      ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

if [ -f "$ROOT_DIR/.env" ] && [ -f "$FUNCTIONS_DIR/.env" ]; then
    echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Comparando archivos .env..."

    # Extraer nombres de variables (líneas que no son comentarios ni vacías)
    ROOT_VARS=$(grep -v '^#' "$ROOT_DIR/.env" | grep -v '^$' | cut -d'=' -f1 | sort)
    FUNCTIONS_VARS=$(grep -v '^#' "$FUNCTIONS_DIR/.env" | grep -v '^$' | cut -d'=' -f1 | sort)

    # Comparar variables
    DIFF_VARS=$(comm -3 <(echo "$ROOT_VARS") <(echo "$FUNCTIONS_VARS") 2>/dev/null || true)

    if [ -n "$DIFF_VARS" ]; then
        echo -e "${YELLOW}${BOLD}[WARNING]${NC} Se detectaron diferencias en las variables de entorno:"
        echo ""

        # Variables en root pero no en functions
        ONLY_ROOT=$(comm -23 <(echo "$ROOT_VARS") <(echo "$FUNCTIONS_VARS") 2>/dev/null || true)
        if [ -n "$ONLY_ROOT" ]; then
            echo -e "${YELLOW}Variables en ROOT/.env pero NO en functions/.env:${NC}"
            echo "$ONLY_ROOT" | while read var; do echo "  - $var"; done
            echo ""
        fi

        # Variables en functions pero no en root
        ONLY_FUNCTIONS=$(comm -13 <(echo "$ROOT_VARS") <(echo "$FUNCTIONS_VARS") 2>/dev/null || true)
        if [ -n "$ONLY_FUNCTIONS" ]; then
            echo -e "${YELLOW}Variables en functions/.env pero NO en ROOT/.env:${NC}"
            echo "$ONLY_FUNCTIONS" | while read var; do echo "  - $var"; done
            echo ""
        fi

        echo -e "${YELLOW}${BOLD}[WARNING]${NC} Por favor, revisa que las variables de entorno sean correctas."
        read -p "$(echo -e ${YELLOW}¿Deseas continuar con el despliegue? \(y/n\): ${NC})" -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[YySs]$ ]]; then
            echo -e "${RED}[ABORT]${NC} Despliegue cancelado por el usuario."
            exit 0
        fi
    else
        echo -e "${GREEN}${BOLD}[OK]${NC} Los archivos .env tienen las mismas variables."
    fi
elif [ ! -f "$ROOT_DIR/.env" ]; then
    echo -e "${YELLOW}${BOLD}[WARNING]${NC} No se encontró archivo .env en el directorio raíz."
elif [ ! -f "$FUNCTIONS_DIR/.env" ]; then
    echo -e "${YELLOW}${BOLD}[WARNING]${NC} No se encontró archivo .env en el directorio functions."
fi

# Paso 2: Generar el paquete musicinfo usando Poetry
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

# Copiar el archivo wheel al directorio functions
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Copiando el archivo wheel..."
cp "$WHEEL_FILE" "$FUNCTIONS_DIR/"
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Archivo wheel copiado a functions/$WHEEL_FILENAME"

# Paso 3: Preparar Firebase Function
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║       PREPARANDO FIREBASE FUNCTIONS        ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Preparando Firebase Function..."
cd "$FUNCTIONS_DIR"

# Actualizar requirements.txt con el nuevo archivo wheel
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} Actualizando requirements.txt..."
echo "firebase_functions~=0.1.0" > requirements.txt
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

# Paso 4: Desplegar Firebase Function
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

echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║          DESPLIEGUE COMPLETADO             ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}${BOLD}[DEPLOY]${NC} ¡Despliegue completado con éxito!"
echo -e "${BLUE}[INFO]${NC} Fecha y hora del despliegue: $(date '+%Y-%m-%d %H:%M:%S')"

# Paso 5: Opción de hacer commit
echo ""
echo -e "${CYAN}${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║             CONTROL DE VERSIONES           ║${NC}"
echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

cd "$ROOT_DIR"

# Verificar si hay cambios en Git
if command -v git &> /dev/null && [ -d ".git" ]; then
    echo -e "${BLUE}[INFO]${NC} Estado actual del repositorio:"
    echo ""
    git status --short
    echo ""

    # Verificar si hay cambios
    if [ -n "$(git status --porcelain)" ]; then
        read -p "$(echo -e ${YELLOW}¿Deseas hacer commit de los cambios? \(y/n\): ${NC})" -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[YySs]$ ]]; then
            # Agregar todos los archivos modificados
            git add -A

            # Mostrar qué se va a commitear
            echo ""
            echo -e "${BLUE}[INFO]${NC} Archivos que se incluirán en el commit:"
            git diff --cached --name-status
            echo ""

            # Mensaje de commit por defecto
            if [ -n "$PROJECT_VERSION" ]; then
                DEFAULT_MSG="chore: deploy v$PROJECT_VERSION to firebase"
            else
                DEFAULT_MSG="chore: deploy to firebase"
            fi

            echo -e "${BLUE}[INFO]${NC} Mensaje por defecto: ${BOLD}$DEFAULT_MSG${NC}"
            read -p "$(echo -e ${YELLOW}Presiona Enter para usar el mensaje por defecto o escribe uno personalizado: ${NC})" COMMIT_MSG

            if [ -z "$COMMIT_MSG" ]; then
                COMMIT_MSG="$DEFAULT_MSG"
            fi

            # Hacer el commit
            git commit -m "$COMMIT_MSG"
            echo ""
            echo -e "${GREEN}${BOLD}[SUCCESS]${NC} Commit realizado exitosamente."
            echo ""

            # Preguntar si desea hacer push
            read -p "$(echo -e ${YELLOW}¿Deseas hacer push al repositorio remoto? \(y/n\): ${NC})" -n 1 -r
            echo ""

            if [[ $REPLY =~ ^[YySs]$ ]]; then
                git push
                echo ""
                echo -e "${GREEN}${BOLD}[SUCCESS]${NC} Push realizado exitosamente."
            else
                echo -e "${BLUE}[INFO]${NC} Los cambios están en commit local. Usa 'git push' cuando estés listo."
            fi
        else
            echo -e "${BLUE}[INFO]${NC} No se realizó el commit. Los cambios siguen sin versionar."
        fi
    else
        echo -e "${BLUE}[INFO]${NC} No hay cambios para commitear."
    fi
else
    echo -e "${YELLOW}[WARNING]${NC} Git no está disponible o no es un repositorio Git."
fi

echo ""
echo -e "${MAGENTA}Gracias por usar el script de despliegue automático.${NC}"