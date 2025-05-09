# common/__init__.py
"""
Pacote com componentes compartilhados entre cliente e servidor.
"""

from .auth import generate_auth_token, validate_token, load_users
from .protocol import ProtocolMode

__all__ = ['generate_auth_token', 'validate_token', 'load_users', 'ProtocolMode']