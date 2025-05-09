# interface/__init__.py
"""
Pacote que contém a interface remota (IDL) do sistema de sincronização de arquivos.
"""

from .remote_interface import RemoteFileSyncInterface

__all__ = ['RemoteFileSyncInterface']