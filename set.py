# Importando as bibliotecas 'BASES' a serem utilizadas.

# Melhora os logs.
import logging
# Utilitário para programação concorrente.
import asyncio
# Utilitário para lidar com IO e comandos de saídas.
import sys
# Abstração maior de um nó.
from kademlia.network import Server

# Constantes a serem utilizadas.
NODE_3_PORT=8470

# Caso os parâmetros informados não atenda o que necessário, saí com 'SIGTERM' 1.
if len(sys.argv) != 4:
    print("Usage: python set.py <bootstrap port> <key> <value>")
    sys.exit(1)

# Configura o 'logger'.
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run():
    server = Server()
    await server.listen(NODE_3_PORT)
    await server.bootstrap([("0.0.0.0", int(sys.argv[1]))])
    await server.set(sys.argv[2], sys.argv[3])
    server.stop()

asyncio.run(run())
