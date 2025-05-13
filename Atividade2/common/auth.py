import json
import hashlib
from typing import Dict, Optional
import os
import logging

def generate_auth_token(username: str, password: str) -> str:
    if not username or not password:
        raise ValueError("Username e password não podem ser vazios")
    
    # Cria um hash combinando username e password
    token = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
    logging.debug(f"Token gerado para usuário {username}")
    return token

def load_users(file_path: str) -> Dict[str, str]:
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

if __name__ == "__main__":
    print("Teste de token:", generate_auth_token("user", "pass"))