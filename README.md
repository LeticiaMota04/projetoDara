# Dara-sockets

Implementação do jogo de tabuleiro **Dara** para **dois jogadores em rede**, com **sockets TCP** em Python. O **servidor** mantém e valida o estado do jogo; cada jogador usa um **cliente** com interface em **Pygame**. As mensagens são **JSON**, uma por linha (`\n`), conforme `shared/protocol.py`.

## Pré-requisitos

- **Python 3.10+** no cliente com Pygame (anotações de tipo `str | None`, etc.).
- **Pygame** apenas no cliente:

  ```bash
  pip install pygame
  ```

O servidor usa somente a biblioteca padrão.

## Pastas

| Pasta | Função |
|--------|--------|
| `server/` | `server.py` (TCP, threads) e `game_logic.py` (regras) |
| `client/` | `client_ui_pygame.py` (interface) |
| `shared/` | `protocol.py` (envio/recebimento de mensagens) |

## Como executar

Execute os comandos a partir da pasta **`dara-sockets`** (onde está este arquivo).

1. **Servidor** (antes de qualquer cliente):

   ```bash
   python server/server.py
   ```

   Escuta em **`0.0.0.0:5001`** (todas as interfaces). Ao iniciar, o terminal mostra **dicas de IP** e lembretes para VM/firewall.

2. **Clientes** — até dois. O endereço do servidor é opcional; sem argumento usa **`localhost`**.

   Mesma máquina que o servidor (dois terminais):

   ```bash
   python client/client_ui_pygame.py
   ```

   Outro computador ou máquina virtual (use o IP **do host que roda o servidor**):

   ```bash
   python client/client_ui_pygame.py 192.168.0.10
   ```

   **VirtualBox (NAT):** do Linux guest para o Windows host, em geral **`10.0.2.2`**:

   ```bash
   python client/client_ui_pygame.py 10.0.2.2
   ```

Se a conexão falhar de fora do host, no **Windows** crie uma regra de **Firewall** liberando **TCP 5001** (entrada).

Quando o **segundo** jogador conecta, a partida começa automaticamente.

## Documentação

Arquitetura, protocolo e detalhes por arquivo: **`explicacao.md`** no diretório **acima** de `dara-sockets`.
