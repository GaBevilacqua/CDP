#!/usr/bin/env python3
"""
Ponto de entrada principal do cliente RMI (versão mínima modificada).
"""

import argparse
import logging
from .stub import FileSyncStub
from .sync_monitor import SyncMonitor
from common.auth import generate_auth_token

def configure_logging():
    """Configuração básica de logging (inalterada)."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('client.log')
        ]
    )

def parse_arguments():
    """Parser de argumentos (inalterado)."""
    parser = argparse.ArgumentParser(description='Cliente de sincronização RMI')
    parser.add_argument('--host', default='localhost', help='Endereço do servidor')
    parser.add_argument('--port', type=int, default=8000, help='Porta do servidor')
    parser.add_argument('--username', required=True, help='Usuário para autenticação')
    parser.add_argument('--password', required=True, help='Senha para autenticação')
    parser.add_argument('--mode', choices=['R', 'RR', 'RRA'], default='R',
                      help='Modo de protocolo (R, RR, RRA)')
    parser.add_argument('--interval', type=int, default=5,
                      help='Intervalo de verificação em segundos')
    return parser.parse_args()

def main():
    """Função principal com alterações mínimas."""
    configure_logging()
    args = parse_arguments()

    try:
        # Modificação 1: Adicionado log do usuário (sem alterar lógica)
        logging.debug(f"Tentando autenticar como: {args.username}")
        
        auth_token = generate_auth_token(args.username, args.password)
        stub = FileSyncStub(
            server_url=f"http://{args.host}:{args.port}",
            auth_token=auth_token
        )
        
        # Modificação 2: Adicionado teste de conexão rápida
        try:
            stub.check_master_version()
        except Exception as e:
            logging.error(f"Falha na conexão inicial: {str(e)}")
            return  # Sai silenciosamente como antes
        
        monitor = SyncMonitor(
            stub=stub,
            protocol_mode=args.mode,
            interval=args.interval
        )

        logging.info(f"Cliente iniciado (Modo: {args.mode})")
        monitor.start()

    except KeyboardInterrupt:
        logging.info("Cliente encerrado pelo usuário")
    except Exception as e:
        logging.error(f"Erro: {str(e)}")  # Mensagem mantida simples

        

    

if __name__ == '__main__':
    main()