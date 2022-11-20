[![Linkedin Badge](https://img.shields.io/badge/-Kauan%20Carvalho-6633cc?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/kauan-carvalho/)](https://www.linkedin.com/in/kauan-carvalho/)

### Aplicação que utiliza DHT (Distributed Hash Table) junto a arquitetura P2P (Peer-to-Peer)

O intuito da aplicação é simplesmente o armazenamento de *arquivos MP3*, onde como critério, o arquivo deve ser de certa forma _fragmentado_ e distribuido pelos nós, utilizando o conceito de tabelas hash distribuídas, dessa forma, os nós da rede devem ser capazes de buscar ou definir certos regsitros.

#### Como funciona?

Basicamente, qualquer arquivo é um _punhado_ de bytes, sabendo disso, e com o intuito de não perder a qualidade da música, a nossa aplicação pega um dado arquivo, no caso estamos falando explicitamente de _.mp3_, e _encoda_ em base64, que tem como finalidade transferência de dados, geralmente binários, com isso, geramos um outro texto que preserva os _bits vazios_. Com o arquivo encodado, fragmentamos em *N* porções de *7500* caractéres (tamanho definido do valor armazenado pelo time), e para cada fragmento geramos uma certa chave na tabela com o auxiliar de um caractére especial (_#_), e quando tentamos buscar uma certa chave, simplesmente o que acontece que a aplicação pega todos os fragmentos, os ordena, e junta voltando ao _base64_ original, e dessa forma podemos decodar no arquivo de volta.

#### Versões de softwares utilizados:

| Ruby  | Python3 |
| :---: | :-----: |
| 3.1.1 |  3.8.0  |

#### Clonando o repositório:

        $ git clone git@github.com:KauanCarvalho/project-aed2.git

#### Rodando a aplicação com docker-compose:

1. Rodando um node (por padrão, subimos o primeiro node na porta 8468):

        $ python node.py

2. Subindo um segundo node na rede para replicação (por padrão, subimos o primeiro node na porta 8469):

        $ python node.py --ip 0.0.0.0 --port 8468

3. Podemos guardar qualquer música na DHT utilizando o caminho relativo (no repositório tem alguns trechos de música), ex:

        $ ruby main.rb define key-waka-waka musicas/waka_waka.mp3

4. Definindo uma segunda música na DHT:

        $ ruby main.rb define key-evidences musicas/evidencias.mp3

5. Recuperando a primeira música:

        $ ruby main.rb busca key-waka-waka

6. Recuperando a segunda música:

        $ ruby main.rb busca key-evidences

Note que ambas se encotram agora na _subpasta 'recuperadas'_. 

Foram colocados os devidos *logs*, inclusive para elucidar o que está acontecendo, exemplo ao subir a aplicação adequadamente:

```bash
python node.py

2022-11-20 04:39:37,329 - kademlia.network - INFO - Node 336784226009406177743853723780522151250921774459 listening on 0.0.0.0:8468
2022-11-20 04:39:37,330 - kademlia.network - DEBUG - Refreshing routing table
```

```bash
python node.py --ip 0.0.0.0 --port 8468

2022-11-20 04:40:02,053 - kademlia.network - INFO - Node 940821304010392210305745554557882791345975334792 listening on 0.0.0.0:8469
2022-11-20 04:40:02,054 - kademlia.network - DEBUG - Refreshing routing table
2022-11-20 04:40:02,054 - kademlia.network - DEBUG - Attempting to bootstrap node with 1 initial contacts
2022-11-20 04:40:02,057 - kademlia.crawling - INFO - creating spider with peers: [[336784226009406177743853723780522151250921774459, '0.0.0.0', 8468]]
2022-11-20 04:40:02,057 - kademlia.crawling - INFO - crawling network with nearest: ([336784226009406177743853723780522151250921774459, '0.0.0.0', 8468],)
2022-11-20 04:40:02,058 - kademlia.protocol - INFO - got successful response from 0.0.0.0:8468
2022-11-20 04:40:02,058 - kademlia.protocol - INFO - never seen 0.0.0.0:8468 before, adding to router
```

Repare na replicação da informação.
```bash
ruby main.rb define key-waka-waka musicas/waka_waka.mp3

2022-11-20 04:40:57,438 - kademlia.protocol - INFO - got successful response from 0.0.0.0:8468
2022-11-20 04:40:57,438 - kademlia.crawling - INFO - crawling network with nearest: ([336784226009406177743853723780522151250921774459, '0.0.0.0', 8468], [940821304010392210305745554557882791345975334792, '127.0.0.1', 8469])
2022-11-20 04:40:57,439 - kademlia.protocol - INFO - got successful response from 127.0.0.1:8469
2022-11-20 04:40:57,439 - kademlia.protocol - INFO - never seen 127.0.0.1:8469 before, adding to router
2022-11-20 04:40:57,440 - kademlia.network - INFO - setting 'key-waka-waka#9' = '+xBk44ABKyVYhjxAAhsBqtDDGAAErFlmGYQAAFOE64MMEAH19SoKYg/wbCi1PZb3zynXqr6OK1d3DW4ut7FOSj/0A/YofYyXXfRZ911/+l2DBBwu+xDi0j29lRRsQNPuAlkqV5H//v/7EmTIDzCsEdsHNEAADyELKOGAAQKISWgHpEEAMIRsFAGIKM0BBCjECLjwiZ6e1O39X8mf5cY3ljOJLS/Vb9XbRJ+eMFgWd6HoJGEjow33d/mKyhpYQyogDoJo/+3/ZqhJKTjrxAAEDv/7EGTIAzCjCFoh5RiQDCEK4AgiJgKUI2AMGGRANYZsFAMIGJ2DDFFwVcvkXIraBYKggSDQwIkQGzp0AcBHg31gMzwwZ2o92r+K1bWrptmA3HQocYQIqskRlAwhD0jizo7lFadHs/9X//sSZMiP8KoIWAMNMJAOgYrgAMIKAjQhZAxAwAA7g2vAEyQQv//AHPLcgs1n8gFEZ27Mag50Sj8f0GrTrff+AABfHeTIlyuIVKDEo4I0yb2kKka5rrdtr4ExBDjmAKiKBsBkj/Bx9lXv//sQZMiP8JUFWQIPSBAOoLrwFSYEAmQpaAewQoA6gqwAIKQIAh1wChaLle18mqz23LW7XbIIAAABdgIbuMM08VzHk7P7//jCR/Cp7+OkID1WYCeqCOp9VWlktu0TChg8qjwRFEZybD//+xJkyQ+QkQVbgetgAAyAqvAEyQQCOBVwBRjAQDcFLFQTCFAf///WcJJZZWws1q4fUMXx1e7pyRqcT1P16f3anf7+lq1JqsLIE4ZFAD1HZyHA1MrMG4tRZJZbZwFEwaSDEJJVUB2d1oL/+xBkzA+wfAVdAOMwEAyhCwAAwgQBpBFyAwkiACyELFQgiGAkCwJgBi8BlKOzn9X9VRZJbaLGAAAAMSSd9xR0jvgJ5/w+HqFBaTbxLknrUG0FZLQjnW/ADigVwpiyE0cfnlVfEfb/O//7EmTTjzBrBdsBKAigDsCLEABDAAJcF2oGJAKAMYHtFAEADyjCA3X3mctc8E0H2qyS/+v+hZGEJI0MAAdU6BuzhXOZNbE5xV3T6FYQADuOGlvNEwrPt+v//8ZJIyCsI/2B4bgVMn+frf/7EGTYAzB4BFsARhAQDkDLaADCAQHcEXqBDEBgPAOsQAGMAPjzJDNFGTI+s5rt2HdSO4FniXqfXZuCXGqiYGEyIJXZcXjZu9J1qi6zraQ6lWhHXhmxmWX4zagICagIkhEDXWd/rdwa//sSZNwD8HkEXyBDEBgNgOsgAEMAAVgBiICESWA5h6xAAwgIUBARJCI8o9wVxL8jlkxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//sQZOOB8D0AY6AiAAoO4OsQAGcAArAxkYGEajAzhCyAARgQVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/+xJk6QPwwgpe6GEYkA7hewAcxSYCeDN6gYREQDyEbAAEjBhVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/+xBk5oEwjyNbACATEg6hW2QAwgkCFBWLgAxAcDkELEADCABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/7EmTogfCzDmJoCRBcDaFLAADFCAKMG2qgCGAAPIUsQAMUIFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/7EGTnAACtCt1lDEAID4BbNaMAAAUId2wYxAAAZISsQwwgAFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//sSZNWP8IAHUYcMAAANAFmg4YABAAABpAAAACAAADSAAAAEVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV' on network
2022-11-20 04:40:57,440 - kademlia.crawling - INFO - creating spider with peers: [[940821304010392210305745554557882791345975334792, '127.0.0.1', 8469], [336784226009406177743853723780522151250921774459, '127.0.0.1', 8468]]
2022-11-20 04:40:57,440 - kademlia.crawling - INFO - crawling network with nearest: ([940821304010392210305745554557882791345975334792, '127.0.0.1', 8469], [336784226009406177743853723780522151250921774459, '127.0.0.1', 8468])
2022-11-20 04:40:57,440 - kademlia.protocol - INFO - got successful response from 127.0.0.1:8469
2022-11-20 04:40:57,441 - kademlia.protocol - INFO - got successful response from 127.0.0.1:8468
2022-11-20 04:40:57,441 - kademlia.network - INFO - setting 'c4c059698e3d0e0f06001339a4d30e1537c33e24' on ['127.0.0.1:8469', '127.0.0.1:8468']
```

```bash
ruby main.rb busca key-waka-waka

2022-11-20 04:42:51,538 - kademlia.network - INFO - Looking up key key-waka-waka#10
2022-11-20 04:42:51,538 - kademlia.crawling - INFO - creating spider with peers: [[940821304010392210305745554557882791345975334792, '127.0.0.1', 8469], [336784226009406177743853723780522151250921774459, '127.0.0.1', 8468]]
2022-11-20 04:42:51,539 - kademlia.crawling - INFO - crawling network with nearest: ([940821304010392210305745554557882791345975334792, '127.0.0.1', 8469], [336784226009406177743853723780522151250921774459, '127.0.0.1', 8468])
2022-11-20 04:42:51,539 - kademlia.protocol - INFO - got successful response from 127.0.0.1:8469
2022-11-20 04:42:51,540 - kademlia.protocol - INFO - got successful response from 127.0.0.1:8468
```

#### Vídeo explicativo da aplicação
[Youtube](https://youtu.be/Njw0JNsyzKI)

## License
[MIT](https://choosealicense.com/licenses/mit/)
