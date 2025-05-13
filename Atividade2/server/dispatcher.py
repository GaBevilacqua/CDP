from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import time
import os
from common.auth import validate_token
from common.protocol import ProtocolMode
import logging
import hashlib
from common.auth import load_users, generate_auth_token

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
        users = load_users(self.users_file)
        for username, password in users.items():
            expected_token = generate_auth_token(username, password)
            if expected_token == auth_token:
                return username
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
        parsed_path = urlparse(self.path)
        endpoint = parsed_path.path
        params = parse_qs(parsed_path.query)
        auth_token = params.get('auth_token', [''])[0]
        
        username = self._authenticate(auth_token)
        if not username:
            return
            
        try:
            if endpoint == '/get_file_content':
                content = self.file_handler.read_content()
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'content': content
                }).encode())
                
            elif endpoint == '/check_master_version':
                version_info = self.file_handler.get_version_info()  # Agora funciona
                self._set_headers()
                self.wfile.write(json.dumps({
                    'status': 'success',
                    'version_info': version_info
                }).encode())
                
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({
                    'status': 'error',
                    'message': 'Endpoint não encontrado'
                }).encode())
                
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': str(e)
            }).encode())
            logging.error(f"Erro interno: {str(e)}")

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