from abc import ABC, abstractmethod
from common.protocol import ProtocolMode
from typing import Dict, Optional
from typing import Optional

class RemoteFileSyncInterface(ABC):
    
    @abstractmethod
    def get_file_content(self, auth_token: str) -> str:
        pass
    
    @abstractmethod
    def check_master_version(self, auth_token: str) -> Dict[str, str]:
        pass
    
    @abstractmethod
    def update_file_content(self, auth_token: str, content: str, protocol_mode: str) -> Dict[str, str]:
        pass
    
    @abstractmethod
    def acknowledge_sync(self, auth_token: str, sync_id: str) -> bool:
        pass