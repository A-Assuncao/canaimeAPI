"""
Ponto de entrada para deploy na Vercel
"""
import importlib.util
import os
import sys
from pathlib import Path

# Adiciona o diretório principal ao sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importa a aplicação FastAPI
from canaimeapi.app import app

# Exporta a aplicação para a Vercel
app = app 