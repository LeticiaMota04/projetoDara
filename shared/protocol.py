import json

_recv_buffers: dict[int, bytes] = {}


def send_message(sock, data: dict) -> None:
    line = json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n"
    sock.sendall(line.encode("utf-8"))


def receive_message(sock):
    sid = id(sock)
    buf = _recv_buffers.get(sid, b"")

    while True:
        i = buf.find(b"\n")
        if i >= 0:
            raw_line = buf[:i]
            buf = buf[i + 1 :]
            _recv_buffers[sid] = buf
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            return json.loads(raw_line.decode("utf-8"))

        chunk = sock.recv(65536)
        if not chunk:
            _recv_buffers.pop(sid, None)
            return None
        buf += chunk
        _recv_buffers[sid] = buf
