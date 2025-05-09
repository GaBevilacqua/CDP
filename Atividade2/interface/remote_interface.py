# interface/remote_interface.py
"""
Módulo que define a interface remota (IDL) para o sistema de sincronização de arquivos.

Esta interface especifica todos os métodos que devem ser implementados tanto pelo servidor
quanto pelo stub do cliente, seguindo o padrão RMI (Remote Method Invocation).

A interface serve como um contrato entre cliente e servidor, garantindo que ambos
implementem os mesmos métodos com a mesma assinatura.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

class RemoteFileSyncInterface(ABC):
    """
    Interface abstrata que define os métodos remotos disponíveis no servidor.
    Todos os métodos devem ser implementados tanto pelo servidor quanto pelo stub do cliente.
    """
    
    @abstractmethod
    def get_file_content(self, auth_token: str) -> str:
        """
        Obtém o conteúdo atual do arquivo master do servidor.
        
        Args:
            auth_token: Token de autenticação gerado a partir de usuário/senha
            
        Returns:
            str: Conteúdo completo do arquivo master
            
        Raises:
            PermissionError: Se o token de autenticação for inválido
            ConnectionError: Se ocorrer um erro de comunicação
        """
        pass
    
    @abstractmethod
    def check_master_version(self, auth_token: str) -> Dict[str, str]:
        """
        Verifica a versão atual do arquivo master, retornando metadados úteis
        para detecção de mudanças.
        
        Args:
            auth_token: Token de autenticação gerado a partir de usuário/senha
            
        Returns:
            Dict[str, str]: Dicionário contendo:
                - 'content_hash': Hash SHA-256 do conteúdo do arquivo
                - 'last_modified': Timestamp da última modificação
                - 'size': Tamanho do arquivo em bytes
                
        Raises:
            PermissionError: Se o token de autenticação for inválido
            ConnectionError: Se ocorrer um erro de comunicação
        """
        pass
    
    @abstractmethod
    def update_file_content(self, auth_token: str, content: str, protocol_mode: str) -> Dict[str, str]:
        """
        Atualiza o conteúdo do arquivo master no servidor.
        
        Args:
            auth_token: Token de autenticação gerado a partir de usuário/senha
            content: Novo conteúdo para o arquivo
            protocol_mode: Modo de protocolo ('R', 'RR' ou 'RRA')
            
        Returns:
            Dict[str, str]: Dicionário contendo:
                - 'status': 'success' ou 'error'
                - 'message': Mensagem descritiva
                - 'sync_id': ID único da sincronização (para modos RR e RRA)
                
        Raises:
            PermissionError: Se o token de autenticação for inválido
            ValueError: Se o modo de protocolo for inválido
            ConnectionError: Se ocorrer um erro de comunicação
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