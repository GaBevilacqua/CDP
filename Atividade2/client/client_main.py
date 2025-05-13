import argparse
import logging
from .stub import FileSyncStub
from .sync_monitor import SyncMonitor
from common.auth import generate_auth_token

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('client.log')
        ]
    )

def parse_arguments():
    parser = argparse.ArgumentParser(description='Cliente de sincronização RMI')
    parser.add_argument('--host', default='localhost', help='Endereço do servidor')
    parser.add_argument('--port', type=int, default=8000, help='Porta do servidor')
    parser.add_argument('--username', required=True, help='Usuário para autenticação')
    parser.add_argument('--password', required=True, help='Senha para autenticação')
    parser.add_argument('--mode', choices=['R', 'RR', 'RRA'], default='R',
                      help='Modo de protocolo (R, RR, RRA)')
    parser.add_argument('--interval', type=int, default=5,
                      help='Intervalos')
    return parser.parse_args()

import threading

def main():
    configure_logging()
    args = parse_arguments()

    try:
        logging.debug(f"Autenticando como: {args.username}")
        
        auth_token = generate_auth_token(args.username, args.password)
        stub = FileSyncStub(
            server_url=f"http://{args.host}:{args.port}",
            auth_token=auth_token
        )

        try:
            stub.check_master_version()
        except Exception as e:
            logging.error(f"Falha na conexão inicial: {str(e)}")
            return

        monitor = SyncMonitor(
            stub=stub,
            protocol_mode=args.mode,
            interval=args.interval
        )

        logging.info(f"Cliente iniciado (Modo: {args.mode})")

        monitor_thread = threading.Thread(target=monitor.start, daemon=True)
        monitor_thread.start()

        print("\n___ Sistema de Sincronização ___")
        print(f"Usuário: {args.username} | Modo: {args.mode}\n")
        
        while True:
            print("\nOpções:")
            print("1. Atualizar master")
            print("2. Sair")
            choice = input("Escolha: ")
            
            if choice == '1':
                new_content = input("\nDigite o novo conteúdo: ")
                try:
                    response = stub.update_master(new_content)
                    print(f"\nSucesso: {response.get('message')}")
                except Exception as e:
                    print(f"\nErro: {str(e)}")
                    
            elif choice == '2':
                print("Encerrando...")
                break
            else:
                print("Opção inválida.")

    except KeyboardInterrupt:
        logging.info("Cliente encerrado pelo usuário.")
    except Exception as e:
        logging.error(f"Erro: {str(e)}")


if __name__ == '__main__':
    main()