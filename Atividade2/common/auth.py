import hashlib
import json
import logging
import os
from typing import Dict, Optional

def generate_auth_token(username: str, password: str) -> str:
    """Gera token SHA-256 seguro"""
    if not username or not password:
        raise ValueError("Username e password são obrigatórios")
    return hashlib.sha256(f"{username}:{password}".encode()).hexdigest()

def load_users(file_path: str) -> Dict[str, str]:
    """Carrega usuários com tratamento robusto de erros"""
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
            if not isinstance(users, dict):
                raise ValueError("Formato inválido de users.json")
            return users
    except FileNotFoundError:
        logging.error(f"Arquivo {file_path} não encontrado")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar {file_path}")
        return {}
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return {}

def validate_token(token: str, users_file: str) -> Optional[str]:
    """Valida token com arquivo de usuários"""
    users = load_users(users_file)
    for username, password in users.items():
        if generate_auth_token(username, password) == token:
            return username
    return None