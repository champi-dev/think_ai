#!/bin/bash
# 🧠 Think AI - Script de inicio rápido
# Ejecuta todo el sistema con un solo comando

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧠 Think AI - Sistema de IA Superinteligente${NC}"
echo -e "${BLUE}===========================================${NC}\n"

# Función para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ Error: $1 no está instalado${NC}"
        return 1
    fi
    return 0
}

# Verificar requisitos
echo -e "${YELLOW}📋 Verificando requisitos...${NC}"
check_command python3 || check_command python || { echo -e "${RED}Python no encontrado!${NC}"; exit 1; }
check_command pip || { echo -e "${RED}pip no encontrado!${NC}"; exit 1; }

# Detectar comando de Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo -e "${GREEN}✓ Requisitos verificados${NC}\n"

# Crear y activar entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}🔧 Creando entorno virtual...${NC}"
    $PYTHON_CMD -m venv venv
fi

# Activar entorno virtual
echo -e "${YELLOW}🔌 Activando entorno virtual...${NC}"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || {
    echo -e "${RED}❌ No se pudo activar el entorno virtual${NC}"
    exit 1
}

# Instalar dependencias si no están instaladas
if ! pip show think-ai-consciousness &> /dev/null; then
    echo -e "${YELLOW}📦 Instalando Think AI...${NC}"
    pip install -e . --quiet
    echo -e "${GREEN}✓ Think AI instalado${NC}\n"
fi

# Inicializar servicios y configuración
echo -e "${YELLOW}🚀 Inicializando servicios del sistema...${NC}"

# Crear directorios necesarios para almacenamiento
mkdir -p storage/chromadb storage/qdrant storage/faiss storage/local data/cache data/logs data/models
echo -e "${GREEN}✓ Directorios de almacenamiento creados${NC}"

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Creando archivo de configuración...${NC}"
    cat > .env << 'EOF'
# Think AI Configuration
DEBUG=false
LOG_LEVEL=INFO
STORAGE_TYPE=local
VECTOR_DB_TYPE=chromadb
CACHE_DIR=data/cache
LOG_DIR=data/logs
MODEL_DIR=data/models
CHROMADB_PATH=storage/chromadb
QDRANT_PATH=storage/qdrant
FAISS_PATH=storage/faiss
API_HOST=0.0.0.0
API_PORT=8080
WEBAPP_PORT=3000
EOF
    echo -e "${GREEN}✓ Configuración creada${NC}\n"
else
    # Cargar variables de entorno existentes
    source .env
fi

# Verificar e instalar dependencias de webapp si existe
if [ -d "webapp" ] && [ -f "webapp/package.json" ]; then
    if [ ! -d "webapp/node_modules" ]; then
        echo -e "${YELLOW}📦 Instalando dependencias de webapp...${NC}"
        cd webapp
        npm install --silent
        cd ..
        echo -e "${GREEN}✓ Dependencias de webapp instaladas${NC}"
    fi
fi

# Inicializar bases de datos vectoriales
echo -e "${YELLOW}🗄️  Inicializando bases de datos vectoriales...${NC}"
$PYTHON_CMD -c "
import os
import sys

# Intentar importar y configurar ChromaDB
try:
    import chromadb
    client = chromadb.PersistentClient(path='storage/chromadb')
    print('✓ ChromaDB inicializado')
except Exception as e:
    print(f'⚠️  ChromaDB no disponible: {e}')

# Intentar importar y configurar Qdrant
try:
    from qdrant_client import QdrantClient
    # Solo intentar crear el cliente, no conectar
    print('✓ Qdrant disponible')
except Exception as e:
    print(f'⚠️  Qdrant no disponible: {e}')

print('✓ Inicialización de servicios completada')
" 2>/dev/null || echo -e "${YELLOW}⚠️  Algunas bases de datos no están disponibles, usando fallback${NC}"

# Pre-cargar el modelo de lenguaje si está disponible
if [ -f "scripts/preload_model.py" ]; then
    echo -e "\n${YELLOW}🧠 Pre-cargando modelo de lenguaje para inicio rápido...${NC}"
    echo -e "${YELLOW}Esto puede tomar un momento la primera vez...${NC}"
    $PYTHON_CMD scripts/preload_model.py 2>&1 | while IFS= read -r line; do
        if [[ "$line" == *"Loading checkpoint shards:"* ]]; then
            echo -e "${BLUE}$line${NC}"
        elif [[ "$line" == *"✅"* ]]; then
            echo -e "${GREEN}$line${NC}"
        elif [[ "$line" == *"❌"* ]]; then
            echo -e "${RED}$line${NC}"
        elif [[ "$line" == *"⚡"* ]] || [[ "$line" == *"🔥"* ]]; then
            echo -e "${YELLOW}$line${NC}"
        else
            echo "$line"
        fi
    done
    echo ""
fi

echo -e "${GREEN}✅ Sistema inicializado y listo para usar${NC}\n"

# Menú de opciones
echo -e "${BLUE}¿Qué quieres ejecutar?${NC}"
echo "1) 💬 Chat Simple O(1) (sin API keys)"
echo "2) 🧠 Sistema Completo (CLI Full)"
echo "3) 🌐 API Server + Webapp"
echo "4) 🚀 Todo el Sistema (Process Manager)"
echo "5) 📊 Demo de Rendimiento"
echo "6) 🤖 CLI Principal (think-ai)"
echo "7) 🧠 Pre-cargar Modelo (acelera futuros inicios)"
echo -e "8) ❌ Salir\n"

read -p "Selecciona una opción (1-8): " choice

case $choice in
    1)
        echo -e "\n${GREEN}▶️  Iniciando Chat Simple O(1)...${NC}"
        echo -e "${YELLOW}Tip: Escribe 'help' para ver comandos disponibles${NC}\n"
        $PYTHON_CMD think_ai_simple_chat.py
        ;;
    2)
        echo -e "\n${GREEN}▶️  Iniciando Sistema Completo CLI...${NC}"
        $PYTHON_CMD think_ai_full_cli.py
        ;;
    3)
        echo -e "\n${GREEN}▶️  Iniciando API Server + Webapp...${NC}"
        echo -e "${YELLOW}API: http://localhost:8080${NC}"
        echo -e "${YELLOW}Web: http://localhost:3000${NC}\n"
        
        # Iniciar API en background
        $PYTHON_CMD railway_server.py &
        API_PID=$!
        
        # Esperar un poco
        sleep 3
        
        # Verificar si hay webapp
        if [ -d "webapp" ] && [ -f "webapp/package.json" ]; then
            echo -e "${YELLOW}📦 Instalando dependencias de webapp...${NC}"
            cd webapp
            npm install --silent
            echo -e "${GREEN}▶️  Iniciando webapp...${NC}"
            npm run dev &
            WEBAPP_PID=$!
            cd ..
        else
            echo -e "${YELLOW}⚠️  Webapp no encontrada, solo API disponible${NC}"
        fi
        
        echo -e "\n${GREEN}✅ Sistema iniciado!${NC}"
        echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}\n"
        
        # Esperar hasta Ctrl+C
        trap "kill $API_PID $WEBAPP_PID 2>/dev/null; exit" INT
        wait
        ;;
    4)
        echo -e "\n${GREEN}▶️  Iniciando TODO el sistema...${NC}"
        $PYTHON_CMD process_manager.py
        ;;
    5)
        echo -e "\n${GREEN}▶️  Ejecutando Demo de Rendimiento O(1)...${NC}"
        $PYTHON_CMD think_ai_1000_iterations_cpu.py
        ;;
    6)
        echo -e "\n${GREEN}▶️  Iniciando CLI Principal...${NC}"
        echo -e "${YELLOW}Usa /help para ver comandos disponibles${NC}\n"
        think-ai || $PYTHON_CMD -m think_ai.cli.main
        ;;
    7)
        echo -e "\n${GREEN}▶️  Pre-cargando modelo de lenguaje...${NC}"
        echo -e "${YELLOW}Esto optimizará los futuros inicios del sistema${NC}\n"
        $PYTHON_CMD scripts/preload_model.py
        ;;
    8)
        echo -e "\n${GREEN}👋 ¡Hasta luego!${NC}"
        exit 0
        ;;
    *)
        echo -e "\n${RED}❌ Opción inválida${NC}"
        exit 1
        ;;
esac

# Desactivar entorno virtual al salir
deactivate 2>/dev/null || true