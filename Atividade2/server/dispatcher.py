
"""
Implementação do dispatcher/skeleton que trata as requisições HTTP.
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import time
import os
from common.auth import validate_token
from common.protocol import ProtocolMode
import logging
import hashlib

class RequestDispatcher(BaseHTTPRequestHandler):
    file_handler = None  # Será inicializado no server_main
    users_file = 'users.json'
    
    def _set_headers(self, status_code=200):
        """Configura os cabeçalhos básicos da resposta."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _parse_request_data(self):
        """Extrai dados da requisição (query params ou body)."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            return json.loads(self.rfile.read(content_length))
        return {}
    
    def _load_users(self) -> dict:
        """Carrega usuários do arquivo JSON com tratamento robusto de erros"""
        try:
            if not os.path.exists(self.users_file):
                logging.error(f"Arquivo {self.users_file} não encontrado")
                return {}

            with open(self.users_file, 'r') as f:
                users = json.load(f)
                if not isinstance(users, dict):
                    raise ValueError("Formato inválido de users.json")
                return users
                
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar {self.users_file}")
            return {}
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {str(e)}")
            return {}
   

    def _authenticate(self, auth_token: str) -> str:
        """Autenticação com tratamento completo de erros"""
        try:
            users = self._load_users()
            if not users:
                logging.error("Nenhum usuário cadastrado")
                return None
                
            for username, password in users.items():
                try:
                    expected_token = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
                    if expected_token == auth_token:
                        logging.info(f"Usuário autenticado: {username}")
                        return username
                except Exception as e:
                    logging.error(f"Erro ao verificar {username}: {str(e)}")
                    continue
                    
            logging.warning("Token não corresponde a nenhum usuário")
            return None
            
        except Exception as e:
            logging.error(f"Falha crítica na autenticação: {str(e)}")
            return None
        

    def _log_request(self, username: str, success: bool, message: str):
        """Registra uma tentativa de sincronização."""
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'username': username,
            'client_ip': self.client_address[0],
            'success': success,
            'message': message
        }
        
        # Escreve no arquivo de log
        with open('sync.log', 'a') as log_file:
            log_file.write(json.dumps(log_entry) + '\n')
        
        # Log no console
        status = "SUCCESS" if success else "FAILED"
        logging.info(f"[{status}] {username}@{self.client_address[0]}: {message}")
        
        def do_GET(self):
            if endpoint == '/check_master_version':
                version_info = self.file_handler.get_version_info()  # Agora deve funcionar
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'version_info': version_info
                }).encode())

    def do_POST(self):
        """Trata requisições POST."""
        parsed_path = urlparse(self.path)
        endpoint = parsed_path.path
        data = self._parse_request_data()
        auth_token = data.get('auth_token', '')
        
        # Autenticação
        username = self._authenticate(auth_token)
        if not username:
            return
        
        try:
            if endpoint == '/update_file_content':
                content = data.get('content', '')
                protocol_mode = data.get('protocol_mode', 'R')
                
                # Valida modo de protocolo
                if not ProtocolMode.has_value(protocol_mode):
                    raise ValueError("Modo de protocolo inválido")
                
                # Atualiza o arquivo
                self.file_handler.write_content(content)
                
                # Prepara resposta
                response = {
                    'status': 'success',
                    'message': 'Arquivo atualizado com sucesso',
                    'sync_id': str(int(time.time())),
                    'protocol_mode': protocol_mode
                }
                
                self._set_headers()
                self.wfile.write(json.dumps(response).encode())
                self._log_request(username, True, f"Arquivo atualizado (Modo: {protocol_mode})")
                
            elif endpoint == '/acknowledge_sync':
                sync_id = data.get('sync_id', '')
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'message': f'Acknowledgment recebido para sync_id {sync_id}'
                }).encode())
                self._log_request(username, True, f"Ack recebido para sync_id {sync_id}")
                
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'message': 'Endpoint não encontrado'
                }).encode())
                self._log_request(username, False, f"Endpoint POST não encontrado: {endpoint}")
                
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': str(e)
            }).encode())
            self._log_request(username, False, f"Erro interno (POST): {str(e)}")