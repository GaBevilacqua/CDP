# CDP

## Exercício 1

### Base
Comunicação Difusa Seletiva (Multicast), 1 host manda para vários destinatários (n), nesse caso usamos UDP.
Para a serialização dos dados utilizamos XML, podemos usar as bibliotecas(xml.etree.ElementTree)

### Arquitetura do Programa Produtos

Configuração do socket (UDP,IP, Port, TTL) -> Ciração XML -> Serialização -> Envio

### Arquitetura Consumidor
COnfiguração do socket -> Recepção -> Desserialização ou usar biblioteca







python server/server_main.py
python -m client.client_main --username admin --password admin123 --mode RR


