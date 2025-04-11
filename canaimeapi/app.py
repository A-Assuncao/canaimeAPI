"""
Aplicação principal da API do Canaimé
"""
import asyncio
import logging
import os
import sys
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from canaimeapi.api.router import router
from canaimeapi.scheduler import scheduler
from canaimeapi.scraper.crawler import atualizar_dados

# Configuração de codificação para o sistema
# Força UTF-8 para entrada/saída padrão
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Certifica-se de que os logs usam UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding='utf-8',  # Especifica UTF-8 para os logs
)
logger = logging.getLogger("canaime_app")

# Criação da aplicação FastAPI
app = FastAPI(
    title="Canaimé API",
    description="API para obter dados do sistema Canaimé",
    version="0.1.0",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adiciona rotas da API
app.include_router(router, prefix="/api/v1", tags=["Canaimé"])


@app.get("/", tags=["Root"])
async def read_root() -> Dict:
    """
    Endpoint raiz da API
    
    Returns:
        Dict: Informações básicas sobre a API
    """
    return {
        "app": "Canaimé API",
        "versao": "0.1.0",
        "documentacao": "/docs",
    }


@app.on_event("startup")
async def startup_event():
    """
    Evento chamado na inicialização da aplicação
    Configura o agendador de tarefas
    """
    logger.info("Inicializando a aplicação Canaimé API")
    
    # Configura e inicia o agendador de tarefas
    await scheduler.start()
    
    # Configura a tarefa periódica de atualização dos dados
    interval_minutes = int(os.getenv("ATUALIZAR_INTERVALO_MINUTOS", "60"))
    scheduler.add_periodic_task(
        atualizar_dados,
        interval_minutes=interval_minutes,
        id="atualizar_dados",
        start_immediately=True,
    )
    
    logger.info(f"Agendador configurado para atualizar dados a cada {interval_minutes} minutos")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento chamado no encerramento da aplicação
    Para o agendador de tarefas
    """
    logger.info("Encerrando a aplicação Canaimé API")
    await scheduler.stop() 