# common/auth.py
"""
Módulo de autenticação compartilhado entre cliente e servidor.

Implementa a geração e validação de tokens de autenticação baseados em usuário e senha.
"""

import json
import hashlib
from typing import Dict, Optional
import os
import logging

def generate_auth_token(username: str, password: str) -> str:
    """
    Gera um token de autenticação baseado em usuário e senha.
    
    Args:
        username: Nome de usuário
        password: Senha do usuário
        
    Returns:
        str: Token SHA-256 no formato hexadecimal
    """
    if not username or not password:
        raise ValueError("Username e password não podem ser vazios")
    
    # Cria um hash combinando username e password
    token = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
    logging.debug(f"Token gerado para usuário {username}")
    return token

def load_users(file_path: str) -> Dict[str, str]:
    """
    Carrega usuários autorizados de um arquivo JSON.
    
    Args:
        file_path: Caminho para o arquivo JSON com usuários e senhas
        
    Returns:
        Dict[str, str]: Dicionário com usuários (chave) e senhas (valor)
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o arquivo não for um JSON válido
    """
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
            if not isinstance(users, dict):
                raise ValueError("Formato inválido do arquivo de usuários")
            return users
    except FileNotFoundError:
        logging.warning(f"Arquivo de usuários não encontrado: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao decodificar arquivo de usuários: {str(e)}")
        raise

def validate_token(token: str, users_file: str) -> Optional[str]:
    """
    Valida um token contra a lista de usuários autorizados.
    
    Args:
        token: Token a ser validado
        users_file: Caminho para o arquivo JSON com usuários autorizados
        
    Returns:
        Optional[str]: Nome do usuário se o token for válido, None caso contrário
    """
    if not token:
        return None
    
    users = load_users(users_file)
    if not users:
        return None
    
    # Verifica se o token corresponde a algum usuário/senha
    for username, password in users.items():
        if generate_auth_token(username, password) == token:
            logging.debug(f"Token válido para usuário {username}")
            return username
    
    logging.warning("Token de autenticação inválido")
    return None