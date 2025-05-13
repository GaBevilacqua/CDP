import os
import hashlib
import time
import logging
from typing import Optional

class SyncMonitor:
    def __init__(self, stub, protocol_mode: str = 'R', interval: int = 5):
        self.stub = stub
        self.protocol_mode = protocol_mode
        self.interval = interval
        self.running = False
        self.slave_file = os.path.join(os.path.dirname(__file__), 'slave.txt')
        self.slave_file = 'slave.txt'
        self._init_file()
        self.last_hash = self._calculate_file_hash()

    def _init_file(self):
        if not os.path.exists(self.slave_file):
            with open(self.slave_file, 'w') as f:
                f.write('')
            logging.info(f"Arquivo {self.slave_file} criado")

    def _calculate_file_hash(self) -> Optional[str]:
        try:
            with open(self.slave_file, 'r') as f:
                return hashlib.sha256(f.read().encode()).hexdigest()
        except IOError as e:
            logging.error(f"Erro ao ler arquivo: {str(e)}")
            return None

    def _sync(self):
        try:
            server_version = self.stub.check_master_version()
            if not server_version:  # Novo
                logging.error("Resposta vazia do servidor")
                return
                
            if server_version.get('content_hash') != self.last_hash:
                content = self.stub.get_file_content()
                if not content:  # Novo
                    logging.error("Conteúdo vazio recebido do servidor")
                    return
                    
                with open(self.slave_file, 'w') as f:
                    f.write(content)
                self.last_hash = self._calculate_file_hash()
        except Exception as e:
            logging.error(f"Erro na sincronização: {str(e)}")

    def _get_local_last_modified(self) -> float:
        return os.path.getmtime(self.slave_file) if os.path.exists(self.slave_file) else 0

    def _sync_local_changes(self):
        current_hash = self._calculate_file_hash()
        if current_hash != self.last_hash:
            try:
                with open(self.slave_file, 'r') as f:
                    content = f.read()
                response = self.stub.update_master(content)
                logging.info(f"Local changes synced to master: {response.get('message')}")
                self.last_hash = current_hash
            except Exception as e:
                logging.error(f"Failed to sync local changes: {str(e)}")

    def start(self):
        self.running = True
        logging.info(f"Monitor started (Interval: {self.interval}s)")
        
        try:
            while self.running:
                self._sync()  
                self._sync_local_changes() 
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        logging.info("Monitor encerrado")

    def manual_sync(self, content: str):
        try:
            response = self.stub.update_file_content(content, self.protocol_mode)
            with open(self.slave_file, 'w') as f:
                f.write(content)
            self.last_hash = self._calculate_file_hash()
            logging.info(f"Sincronização manual: {response.get('message')}")
        except Exception as e:
            logging.error(f"Erro na sincronização manual: {str(e)}")
            raise