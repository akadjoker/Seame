#!/bin/bash

# Caminho para o ambiente virtual
VENV_PATH="/home/djoker/code"

# Caminho para o script Python
SCRIPT_PATH="/home/djoker/dev/oled_ip.py"

python3 -m venv $VENV_PATH

source "$VENV_PATH/bin/activate"
python "$SCRIPT_PATH"

# Desativar o ambiente virtual (opcional)
#deactivate



python3 -m venv /home/djoker/code
source  code/bin/activate
