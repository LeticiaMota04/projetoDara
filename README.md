# Dara-sockets

Implementação do jogo de tabuleiro **Dara** em modo **dois jogadores em rede**, usando **sockets TCP** em Python. Há um **servidor** que valida o estado do jogo e até **dois clientes** com interface gráfica (**Pygame**). A comunicação entre cliente e servidor é feita com mensagens em **JSON**, uma por linha (ver `shared/protocol.py`).

## Como executar

1. **Instalar dependências** (na pasta do projeto):

   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar o servidor** (deve rodar antes dos clientes):

   ```bash
   python server/server.py
   ```

   O servidor escuta em todas as interfaces (`0.0.0.0`) na porta **5001**.

3. **Iniciar dois clientes** (dois terminais ou duas máquinas na mesma rede; se for outro computador, altere `HOST` em `client/client_ui_pygame.py` para o IP da máquina do servidor):

   ```bash
   python client/client_ui_pygame.py
   ```

Quando o **segundo** jogador conecta, a partida começa automaticamente.
