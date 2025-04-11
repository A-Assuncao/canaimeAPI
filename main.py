"""
Ponto de entrada para execução local da aplicação
"""
import asyncio
import os
import sys
import uvicorn
from pathlib import Path

from dotenv import load_dotenv
from canaimeapi.app import app

# Configuração de codificação para o sistema
# Força UTF-8 para entrada/saída padrão
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Certifica-se de que os logs usam UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

def main():
    """Função principal para iniciar a aplicação localmente"""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configura o host e porta para o servidor
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    
    # Inicia o servidor
    print(f"Iniciando a API no endereço http://{host}:{port}")
    uvicorn.run(
        "canaimeapi.app:app",
        host=host,
        port=port,
        reload=True,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "use_colors": True,
                }
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "INFO"},
                "canaime_scraper": {"handlers": ["default"], "level": "INFO"},
                "fastapi": {"handlers": ["default"], "level": "INFO"},
            },
        }
    )


if __name__ == "__main__":
    main()
