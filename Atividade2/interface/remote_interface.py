from abc import ABC, abstractmethod
from common.protocol import ProtocolMode
from typing import Dict, Optional
from typing import Optional

class RemoteFileSyncInterface(ABC):
    
    @abstractmethod
    def get_file_content(self, auth_token: str) -> str:
        """
        Obtém o conteúdo atual do arquivo master do servidor.
        """
        pass
    
    @abstractmethod
    def check_master_version(self, auth_token: str) -> Dict[str, str]:
        """
        Verifica a versão atual do arquivo master, retornando metadados úteis
        para detecção de mudanças.
        """
        pass
    
    @abstractmethod
    def update_file_content(self, auth_token: str, content: str, protocol_mode: str) -> Dict[str, str]:
        """
        Atualiza o conteúdo do arquivo master no servidor.
        """
        pass
    
    @abstractmethod
    def acknowledge_sync(self, auth_token: str, sync_id: str) -> bool:
        """
        Envia um acknowledgment para o servidor (usado nos modos RR e RRA).
        
        Args:
            auth_token: Token de autenticação gerado a partir de usuário/senha
            sync_id: ID da sincronização a ser confirmada
            
        Returns:
            bool: True se o acknowledgment foi registrado com sucesso
            
        Raises:
            PermissionError: Se o token de autenticação for inválido
            ConnectionError: Se ocorrer um erro de comunicação
        """
        pass