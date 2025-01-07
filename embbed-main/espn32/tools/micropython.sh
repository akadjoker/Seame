#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Verifica se é root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Por favor, execute como root (sudo)${NC}"
    exit 1
fi

# Verifica se o firmware existe
FIRMWARE="ESP32_GENERIC-20241129-v1.24.1.bin"
if [ ! -f "$FIRMWARE" ]; then
    echo -e "${RED}Firmware $FIRMWARE não encontrado no diretório atual${NC}"
    exit 1
fi

# Função para verificar se um comando existe
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${BLUE}Instalando $1...${NC}"
        apt-get install -y $1
    fi
}

echo -e "${GREEN}Iniciando instalação do MicroPython para ESP32...${NC}"

# Instala dependências necessárias
apt-get update
check_command python3
check_command python3-pip

# Instala esptool se necessário
if ! command -v esptool.py &> /dev/null; then
    echo -e "${BLUE}Instalando esptool...${NC}"
    pip3 install esptool
fi

# Identifica a porta ESP32
PORT=$(ls /dev/ttyUSB* 2>/dev/null | head -n 1)
if [ -z "$PORT" ]; then
    echo -e "${RED}ESP32 não encontrada. Verifique a conexão USB.${NC}"
    exit 1
fi

echo -e "${GREEN}ESP32 encontrada em: $PORT${NC}"

# Adiciona usuário ao grupo dialout
current_user=$(who am i | awk '{print $1}')
usermod -a -G dialout $current_user
echo -e "${BLUE}Usuário $current_user adicionado ao grupo dialout${NC}"

# Apaga flash
echo -e "${BLUE}Apagando flash da ESP32...${NC}"
esptool.py --port $PORT erase_flash

# Instala MicroPython
echo -e "${BLUE}Instalando MicroPython...${NC}"
esptool.py --chip esp32 --port $PORT --baud 460800 write_flash -z 0x1000 $FIRMWARE

echo -e "${GREEN}Instalação concluída!${NC}"
echo -e "${BLUE}Recomendamos usar Thonny IDE para programar: sudo apt install thonny${NC}"
echo -e "${GREEN}Você precisa fazer logout e login novamente para as permissões terem efeito${NC}"
