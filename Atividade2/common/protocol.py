# common/protocol.py
"""
Definição dos protocolos de comunicação e sincronização para o sistema RMI.

Contém:
- ProtocolMode: Enumeração dos modos de operação (R, RR, RRA)
- SyncProtocol: Classe auxiliar para operações de sincronização
"""

from enum import Enum, auto
import logging
from typing import Optional, Dict, Any

class ProtocolMode(Enum):
    """
    Enumeração dos modos de comunicação suportados pelo sistema.
    
    Valores:
        SIMPLE_REQUEST ('R'): Requisição simples sem confirmação
        REQUEST_RESPONSE ('RR'): Requisição com confirmação síncrona
        ASYNC_ACK ('RRA'): Requisição com confirmação assíncrona
    """
    SIMPLE_REQUEST = 'R'
    REQUEST_RESPONSE = 'RR'
    ASYNC_ACK = 'RRA'

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Verifica se um valor é um modo válido."""
        return value in cls._value2member_map_

    def get_description(self) -> str:
        """Retorna descrição amigável do modo."""
        return {
            self.SIMPLE_REQUEST: "Requisição Simples",
            self.REQUEST_RESPONSE: "Requisição-Resposta",
            self.ASYNC_ACK: "Confirmação Assíncrona"
        }.get(self, "Modo Desconhecido")

class SyncProtocol:
    """
    Classe auxiliar para operações de sincronização.
    Implementa padrões comuns para todos os modos de operação.
    """
    
    @staticmethod
    def validate_mode(mode: str) -> ProtocolMode:
        """Valida e converte string para ProtocolMode."""
        if not ProtocolMode.has_value(mode):
            raise ValueError(f"Modo de protocolo inválido: {mode}")
        return ProtocolMode(mode)

    @staticmethod
    def requires_acknowledgment(mode: ProtocolMode) -> bool:
        """Verifica se o modo requer confirmação."""
        return mode in [ProtocolMode.REQUEST_RESPONSE, ProtocolMode.ASYNC_ACK]

    @staticmethod
    def prepare_request(content: str, mode: ProtocolMode) -> Dict[str, Any]:
        """
        Prepara um dicionário padrão para requisições de sincronização.
        
        Args:
            content: Conteúdo a ser sincronizado
            mode: Modo de protocolo
            
        Returns:
            Dicionário padronizado para a requisição
        """
        return {
            "content": content,
            "protocol_mode": mode.value,
            "timestamp": SyncProtocol.current_timestamp()
        }

    @staticmethod
    def current_timestamp() -> str:
        """Retorna timestamp no formato ISO8601."""
        from datetime import datetime
        return datetime.now().isoformat()

    @staticmethod
    def log_operation(mode: ProtocolMode, operation: str, success: bool = True):
        """Log padronizado para operações de sincronização."""
        status = "SUCESSO" if success else "FALHA"
        logging.info(f"[{status}] {mode.get_description()} - {operation}")