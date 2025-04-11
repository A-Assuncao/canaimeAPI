#!/bin/bash

# Script para configurar a aplicação na Vercel
echo "Iniciando a configuração do ambiente..."

# Configurando ambiente
export PLAYWRIGHT_BROWSERS_PATH=0

# Instalando dependências Python
pip install -r requirements.txt

# Instalando apenas o navegador Chromium do Playwright com argumentos de otimização
python -m playwright install chromium --with-deps
echo "Instalação do Chromium concluída!"

echo "Instalação concluída com sucesso!"

# EOF 