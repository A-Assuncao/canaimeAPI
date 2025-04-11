"""
Definição das rotas da API do Canaimé
"""
import json
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from canaimeapi.api.auth import verificar_credenciais
from canaimeapi.scraper.crawler import scraper

# Criação do router
router = APIRouter()


@router.get("/dados", response_model=List[Dict])
async def get_dados(username: str = Depends(verificar_credenciais)):
    """
    Endpoint para obter os dados dos presos
    
    Args:
        username: Nome do usuário autenticado (injetado pela dependência)
        
    Returns:
        List[Dict]: Lista de presos com suas informações
        
    Raises:
        HTTPException: Se não houver dados disponíveis
    """
    if scraper.dados_presos is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dados não disponíveis. Aguarde a primeira atualização.",
        )
    
    return json.loads(scraper.dados_json)


@router.get("/status")
async def get_status(username: str = Depends(verificar_credenciais)):
    """
    Endpoint para verificar o status do serviço
    
    Args:
        username: Nome do usuário autenticado (injetado pela dependência)
        
    Returns:
        Dict: Status do serviço com informações sobre a última atualização
    """
    return {
        "status": "online",
        "ultima_atualizacao": scraper.ultima_atualizacao,
        "registros": len(scraper.dados_presos) if scraper.dados_presos is not None else 0,
        "timestamp": datetime.now().isoformat(),
    } 