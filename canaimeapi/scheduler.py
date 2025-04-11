"""
Módulo de agendamento de tarefas para atualização periódica dos dados
"""
import asyncio
import logging
from datetime import datetime
from typing import Callable, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("canaime_scheduler")


class TaskScheduler:
    """Classe responsável por agendar a execução periódica de tarefas"""
    
    def __init__(self):
        """Inicializa o agendador de tarefas"""
        self.scheduler = AsyncIOScheduler()
        self.running = False
        
    async def start(self):
        """Inicia o agendador de tarefas"""
        if not self.running:
            self.scheduler.start()
            self.running = True
            logger.info("Agendador de tarefas iniciado")
            
    async def stop(self):
        """Para o agendador de tarefas"""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            logger.info("Agendador de tarefas parado")
            
    def add_periodic_task(
        self,
        task: Callable,
        interval_minutes: int = 60,
        id: str = None,
        start_immediately: bool = True,
    ):
        """
        Adiciona uma tarefa periódica ao agendador
        
        Args:
            task: Função a ser executada periodicamente
            interval_minutes: Intervalo em minutos entre as execuções
            id: Identificador da tarefa (opcional)
            start_immediately: Se True, executa a tarefa imediatamente
        """
        trigger = IntervalTrigger(minutes=interval_minutes)
        job_id = id or f"task_{datetime.now().timestamp()}"
        
        self.scheduler.add_job(
            task,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
        )
        
        logger.info(
            f"Tarefa '{job_id}' agendada para execução a cada {interval_minutes} minutos"
        )
        
        # Executa a tarefa imediatamente, se solicitado
        if start_immediately:
            asyncio.create_task(task())
            logger.info(f"Execução imediata da tarefa '{job_id}' iniciada")


# Instância única do agendador para ser usada em toda a aplicação
scheduler = TaskScheduler() 