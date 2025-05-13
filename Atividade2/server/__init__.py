# server/__init__.py
"""
Pacote do servidor do sistema de sincronização de arquivos RMI.
"""

from .server_main import run_server
from .dispatcher import RequestDispatcher
from .file_handler import FileHandler

__all__ = ['run_server', 'RequestDispatcher', 'FileHandler']