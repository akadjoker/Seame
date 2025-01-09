#!/bin/bash

# Nome do ambiente virtual
ENV_NAME="code"


# Função para verificar erros e parar o script
function check_error {
    if [ $? -ne 0 ]; then
        echo "Erro ao executar: $1"
        exit 1
    fi
}

# Criar o ambiente virtual se não existir
if [ ! -d "$ENV_NAME" ]; then
    echo "Criando o ambiente virtual..."
    python3 -m venv $ENV_NAME
    check_error "Criar ambiente virtual"
    echo "Ambiente virtual criado com sucesso."
fi

# Ativar o ambiente virtual
echo "Ativando o ambiente virtual..."
source $ENV_NAME/bin/activate
check_error "Ativar ambiente virtual"


# Desativar o ambiente virtual
deactivate
echo "Ambiente virtual desativado."
