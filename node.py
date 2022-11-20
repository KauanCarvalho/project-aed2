# Importando as bibliotecas 'BASES' a serem utilizadas.

# Ajuda a parsear os parâmetros.
import argparse
# Melhora os logs.
import logging
# Utilitário para programação concorrente.
import asyncio
# Abstração maior de um nó.
from kademlia.network import Server

# Constantes a serem utilizadas.
NODE_1_PORT=8468
NODE_2_PORT=8469

# Configura o 'logger'.
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# Instância o servidor.
server = Server()


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Argumentos opcionais.
    parser.add_argument("--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("--port", help="port number of existing node", type=int, default=None)

    return parser.parse_args()


def connect_to_bootstrap_node(args):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    # Sobe o segundo nó, e conecta a rede do primeiro nó.
    loop.run_until_complete(server.listen(NODE_2_PORT))
    bootstrap_node = (args.ip, int(args.port))
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def create_bootstrap_node():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    # Sobe o primeiro nó e cria a rede.
    loop.run_until_complete(server.listen(NODE_1_PORT))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def main():
    args = parse_arguments()

    if args.ip and args.port:
        connect_to_bootstrap_node(args)
    else:
        create_bootstrap_node()


if __name__ == "__main__":
    main()
