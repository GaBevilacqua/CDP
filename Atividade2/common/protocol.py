# common/protocol.py
"""
Definição dos modos de protocolo de comunicação suportados pelo sistema.
"""

from enum import Enum, auto
import logging

class ProtocolMode(Enum):
    """
    Enumeração dos modos de protocolo de comunicação suportados.
    
    Valores:
        SIMPLE_REQUEST ('R'): Requisição simples (request-only)
        REQUEST_RESPONSE ('RR'): Requisição-Resposta confirmada
        ASYNC_ACK ('RRA'): Requisição-Resposta com Acknowledgment assíncrono
    """
    SIMPLE_REQUEST = 'R'
    REQUEST_RESPONSE = 'RR'
    ASYNC_ACK = 'RRA'

    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        Verifica se um valor é um modo de protocolo válido.
        
        Args:
            value: Valor a ser verificado
            
        Returns:
            bool: True se o valor for válido, False caso contrário
        """
        return value in {item.value for item in cls}

    @classmethod
    def get_mode(cls, value: str) -> 'ProtocolMode':
        """
        Obtém o enum correspondente ao valor string.
        
        Args:
            value: Valor string ('R', 'RR' ou 'RRA')
            
        Returns:
            ProtocolMode: Enum correspondente
            
        Raises:
            ValueError: Se o valor não corresponder a nenhum modo válido
        """
        for mode in cls:
            if mode.value == value:
                return mode
        raise ValueError(f"Modo de protocolo inválido: {value}")

    def get_description(self) -> str:
        """
        Retorna uma descrição amigável do modo de protocolo.
        """
        descriptions = {
            self.SIMPLE_REQUEST: "Requisição simples (sem confirmação)",
            self.REQUEST_RESPONSE: "Requisição-Resposta confirmada",
            self.ASYNC_ACK: "Requisição-Resposta com Ack assíncrono"
        }
        return descriptions.get(self, "Modo de protocolo desconhecido")

    def requires_ack(self) -> bool:
        """
        Indica se este modo de protocolo requer acknowledgment.
        """
        return self in {ProtocolMode.REQUEST_RESPONSE, ProtocolMode.ASYNC_ACK}

    def is_async_ack(self) -> bool:
        """
        Indica se este modo de protocolo requer acknowledgment assíncrono.
        """
        return self == ProtocolMode.ASYNC_ACK