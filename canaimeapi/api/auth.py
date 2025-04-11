"""
Módulo de autenticação para a API do Canaimé
"""
import os
import secrets
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Configurações de autenticação
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "admin")

# Sistema de autenticação básica HTTP
security = HTTPBasic()


def verificar_credenciais(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    """
    Verifica as credenciais de autenticação HTTP Basic
    
    Args:
        credentials: Credenciais HTTP Basic fornecidas na requisição
        
    Returns:
        str: Nome de usuário autenticado
        
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    is_username_ok = secrets.compare_digest(credentials.username, API_USERNAME)
    is_password_ok = secrets.compare_digest(credentials.password, API_PASSWORD)
    
    if not (is_username_ok and is_password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username 