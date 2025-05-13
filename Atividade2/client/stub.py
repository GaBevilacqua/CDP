"""
Implementação do Stub RMI para comunicação com o servidor.
"""

import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from interface.remote_interface import RemoteFileSyncInterface
from common.protocol import ProtocolMode
import logging

class FileSyncStub(RemoteFileSyncInterface):
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url.rstrip('/')
        self.auth_token = auth_token
        logging.info(f"Stub conectado a {self.server_url}")
        logging.debug(f"Token sendo usado: {auth_token}")

    def _make_request(self, endpoint: str, method: str = 'GET', data: dict = None):
        """Método interno para requisições HTTP."""
        url = f"{self.server_url}{endpoint}"
        try:
            if method == 'GET':
                url = f"{url}?auth_token={self.auth_token}"
                request = Request(url)
            else:
                if data is None:
                    data = {}
                data['auth_token'] = self.auth_token
                request = Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={'Content-Type': 'application/json'},
                    method=method
                )
            
            with urlopen(request) as response:
                return json.loads(response.read().decode())
                
        except HTTPError as e:
            logging.error(f"Erro HTTP {e.code}: {e.reason}")
            raise
        except URLError as e:
            logging.error(f"Falha na conexão: {str(e)}")
            raise

    def get_file_content(self) -> str:
        response = self._make_request('/get_file_content')
        return response.get('content', '')

    def check_master_version(self) -> dict:
        return self._make_request('/check_master_version').get('version_info', {})

    def update_file_content(self, content: str, protocol_mode: str = 'R') -> dict:
        if not ProtocolMode.has_value(protocol_mode):
            raise ValueError(f"Modo de protocolo inválido: {protocol_mode}")
        
        response = self._make_request(
            '/update_file_content',
            method='POST',
            data={'content': content, 'protocol_mode': protocol_mode}
        )
        
        if ProtocolMode(protocol_mode).requires_ack():
            self._send_acknowledgment(response.get('sync_id'), protocol_mode)
            
        return response

    def acknowledge_sync(self, sync_id: str) -> bool:
        response = self._make_request(
            '/acknowledge_sync',
            method='POST',
            data={'sync_id': sync_id}
        )
        return response.get('status') == 'success'

    def _send_acknowledgment(self, sync_id: str, protocol_mode: str):
        if not sync_id:
            return
            
        if ProtocolMode(protocol_mode) == ProtocolMode.REQUEST_RESPONSE:
            if self.acknowledge_sync(sync_id):
                logging.info(f"ACK RR enviado para {sync_id}")
                
        elif ProtocolMode(protocol_mode) == ProtocolMode.ASYNC_ACK:
            import threading
            threading.Timer(2.0, self._send_async_ack, args=(sync_id,)).start()
            logging.info(f"ACK RRA agendado para {sync_id}")

    def _send_async_ack(self, sync_id: str):
        try:
            if self.acknowledge_sync(sync_id):
                logging.info(f"ACK RRA enviado para {sync_id}")
        except Exception as e:
            logging.error(f"Falha no ACK assíncrono: {str(e)}")