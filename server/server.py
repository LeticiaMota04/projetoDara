import socket
import sys
import threading
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
_server_dir = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
if str(_server_dir) not in sys.path:
    sys.path.insert(0, str(_server_dir))

from shared.protocol import send_message, receive_message
from game_logic import DaraGame, PLAYER1, PLAYER2

HOST = "0.0.0.0"
PORT = 5001
MAX_PLAYERS = 2

players = []
lock = threading.Lock()
game_lock = threading.Lock()

game = DaraGame()


# -------------------------------
# UTIL
# -------------------------------

def game_state_message():
    return {
        "type": "game_state",
        "data": {
            "turn": game.current_turn,
            "phase": game.phase,
            "must_capture": game.must_capture,
            "captures": [game.captures[PLAYER1], game.captures[PLAYER2]],
        }
    }


def broadcast(message):
    for player in players:
        send_message(player, message)


def send_to_player(player_conn, message):
    send_message(player_conn, message)


# -------------------------------
# GAME CONTROL
# -------------------------------

def start_game():
    print("Iniciando partida!")
    with game_lock:
        game.reset()
        for i, player in enumerate(players):
            player_id = i + 1

            send_to_player(player, {
                "type": "start_game",
                "data": {"player": player_id}
            })

        broadcast(game_state_message())


def handle_message(conn, player_id, message):

    msg_type = message["type"]
    data = message.get("data", {})

    print(f"[PLAYER {player_id}] {msg_type} -> {data}")

    if game.game_over_winner is not None:
        if msg_type == "restart_game":
            game.reset()
            broadcast({
                "type": "update_board",
                "data": {"board": game.get_board()}
            })
            broadcast(game_state_message())
            broadcast({"type": "match_reset", "data": {}})
            return
        if msg_type == "chat":
            broadcast({
                "type": "chat",
                "data": {
                    "player": player_id,
                    "message": data["message"]
                }
            })
            return
        return

    if msg_type == "restart_game":
        return

    # -------------------------------
    # PLACE PIECE
    # -------------------------------
    if msg_type == "place_piece":

        success = game.place_piece(
            data["row"],
            data["col"],
            player_id
        )

        if success:
            broadcast({
                "type": "update_board",
                "data": {"board": game.get_board()}
            })

            broadcast(game_state_message())

    # -------------------------------
    # MOVE PIECE
    # -------------------------------
    elif msg_type == "move_piece":

        success = game.move_piece(
            data["from"][0],
            data["from"][1],
            data["to"][0],
            data["to"][1],
            player_id
        )

        if success:

            broadcast({
                "type": "update_board",
                "data": {"board": game.get_board()}
            })

            broadcast(game_state_message())

    # -------------------------------
    # CAPTURE PIECE
    # -------------------------------
    elif msg_type == "capture_piece":

        success = game.capture_piece(
            data["row"],
            data["col"],
            player_id
        )

        if success:

            broadcast({
                "type": "update_board",
                "data": {"board": game.get_board()}
            })

            winner = game.check_game_over()

            if winner:
                game.game_over_winner = winner
                broadcast({
                    "type": "game_over",
                    "data": {"winner": winner}
                })
            else:
                broadcast(game_state_message())

    # -------------------------------
    # CHAT
    # -------------------------------
    elif msg_type == "chat":

        broadcast({
            "type": "chat",
            "data": {
                "player": player_id,
                "message": data["message"]
            }
        })

    # -------------------------------
    # RESIGN
    # -------------------------------
    elif msg_type == "resign":

        winner = PLAYER2 if player_id == PLAYER1 else PLAYER1
        game.game_over_winner = winner
        broadcast({
            "type": "game_over",
            "data": {"winner": winner}
        })


# -------------------------------
# CLIENT HANDLER
# -------------------------------

def handle_client(conn, addr, player_id):

    print(f"Jogador {player_id} conectado: {addr}")

    try:
        while True:

            message = receive_message(conn)

            if not message:
                break

            with game_lock:
                handle_message(conn, player_id, message)

    except Exception as e:
        print(f"Erro com jogador {player_id}: {e}")

    finally:
        print(f"Jogador {player_id} desconectado")
        conn.close()

        with lock:
            if conn in players:
                players.remove(conn)


# -------------------------------
# SERVER START
# -------------------------------

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)

    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:

        conn, addr = server.accept()

        with lock:
            if len(players) >= MAX_PLAYERS:
                send_message(conn, {"type": "error", "data": {"message": "Sala cheia"}})
                conn.close()
                continue

            players.append(conn)
            player_id = len(players)

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, player_id)
        )

        thread.start()

        if len(players) == 2:
            start_game()


if __name__ == "__main__":
    start_server()
