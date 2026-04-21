import socket
import threading
import time
import webbrowser
from dataclasses import dataclass, field

from flask import Flask, flash, redirect, render_template, request, url_for

from des_socket_utils import HEADER_SIZE, build_packet, decrypt_des_cbc, encrypt_des_cbc, parse_header, recv_exact


@dataclass
class AppState:
    lock: threading.Lock = field(default_factory=threading.Lock)
    receiver_running: bool = False
    receiver_status: str = "Sẵn sàng nhận và giải mã bản tin."
    receiver_host: str = "127.0.0.1"
    receiver_port: int = 6000
    receiver_timeout: float = 60.0
    receiver_error: str = ""
    last_sender_status: str = "Chưa gửi bản tin nào."
    last_sender_error: str = ""
    last_message: str = ""
    last_key_hex: str = ""
    last_iv_hex: str = ""
    last_ciphertext_hex: str = ""
    last_plaintext: str = ""
    last_peer: str = ""
    manual_decrypt_status: str = "Chưa thực hiện giải mã thủ công."
    manual_decrypt_error: str = ""
    manual_decrypt_plaintext: str = ""

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "receiver_running": self.receiver_running,
                "receiver_status": self.receiver_status,
                "receiver_host": self.receiver_host,
                "receiver_port": self.receiver_port,
                "receiver_timeout": self.receiver_timeout,
                "receiver_error": self.receiver_error,
                "last_sender_status": self.last_sender_status,
                "last_sender_error": self.last_sender_error,
                "last_message": self.last_message,
                "last_key_hex": self.last_key_hex,
                "last_iv_hex": self.last_iv_hex,
                "last_ciphertext_hex": self.last_ciphertext_hex,
                "last_plaintext": self.last_plaintext,
                "last_peer": self.last_peer,
                "manual_decrypt_status": self.manual_decrypt_status,
                "manual_decrypt_error": self.manual_decrypt_error,
                "manual_decrypt_plaintext": self.manual_decrypt_plaintext,
            }


state = AppState()


def ensure_receiver_started(host: str, port: int, timeout: float) -> bool:
    with state.lock:
        if state.receiver_running:
            return False
        state.receiver_running = True
        state.receiver_host = host
        state.receiver_port = port
        state.receiver_timeout = timeout
        state.receiver_status = f"Đang lắng nghe {host}:{port}..."
        state.receiver_error = ""
        state.last_plaintext = ""
        state.last_peer = ""

    thread = threading.Thread(
        target=run_receiver_once,
        args=(host, port, timeout),
        daemon=True,
    )
    thread.start()
    return True


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "fit4012-des-socket-demo"

    @app.get("/")
    def index():
        return render_template("index.html", state=state.snapshot())

    @app.post("/sender/send")
    def send_message():
        host = request.form.get("host", "127.0.0.1").strip() or "127.0.0.1"
        port = int(request.form.get("port", "6000"))
        message = request.form.get("message", "").strip()

        if not message:
            with state.lock:
                state.last_sender_error = "Bạn cần nhập bản tin trước khi gửi."
                state.last_sender_status = "Gửi thất bại."
            flash("Bạn cần nhập bản tin trước khi gửi.", "error")
            return redirect(url_for("index"))

        with state.lock:
            receiver_running = state.receiver_running
            receiver_host = state.receiver_host
            receiver_port = state.receiver_port
            receiver_timeout = state.receiver_timeout

        if not receiver_running and host == receiver_host and port == receiver_port:
            ensure_receiver_started(host, port, receiver_timeout)
            time.sleep(0.25)

        try:
            key, iv, cipher_bytes = encrypt_des_cbc(message.encode("utf-8"))
            packet = build_packet(key, iv, cipher_bytes)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                client.sendall(packet)
        except OSError as exc:
            with state.lock:
                state.last_sender_error = str(exc)
                state.last_sender_status = "Gửi thất bại."
                state.last_message = message
            flash(f"Gửi thất bại: {exc}", "error")
            return redirect(url_for("index"))

        with state.lock:
            state.last_sender_error = ""
            state.last_sender_status = f"Đã gửi bản mã tới {host}:{port}."
            state.last_message = message
            state.last_key_hex = key.hex()
            state.last_iv_hex = iv.hex()
            state.last_ciphertext_hex = cipher_bytes.hex()

        flash("Gửi bản tin thành công.", "success")
        return redirect(url_for("index"))

    @app.post("/decrypt")
    def decrypt_message():
        key_hex = request.form.get("key_hex", "").strip()
        iv_hex = request.form.get("iv_hex", "").strip()
        ciphertext_hex = request.form.get("ciphertext_hex", "").strip()

        if not key_hex or not iv_hex or not ciphertext_hex:
            flash("Cần nhập đủ key, IV và ciphertext để giải mã.", "error")
            return redirect(url_for("index"))

        try:
            key = bytes.fromhex(key_hex)
            iv = bytes.fromhex(iv_hex)
            ciphertext = bytes.fromhex(ciphertext_hex)
            plaintext = decrypt_des_cbc(key, iv, ciphertext).decode("utf-8", errors="ignore")
        except ValueError as exc:
            with state.lock:
                state.manual_decrypt_status = "Giải mã thất bại."
                state.manual_decrypt_error = str(exc)
                state.manual_decrypt_plaintext = ""
            flash(f"Giải mã thất bại: {exc}", "error")
            return redirect(url_for("index"))

        with state.lock:
            state.manual_decrypt_status = "Giải mã thủ công thành công."
            state.manual_decrypt_error = ""
            state.manual_decrypt_plaintext = plaintext

        flash("Giải mã thủ công thành công.", "success")
        return redirect(url_for("index"))

    return app


def run_receiver_once(host: str, port: int, timeout: float) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)
            server.settimeout(timeout)
            conn, addr = server.accept()
            with conn:
                header = recv_exact(conn, HEADER_SIZE)
                key, iv, length = parse_header(header)
                cipher_bytes = recv_exact(conn, length)
                plaintext = decrypt_des_cbc(key, iv, cipher_bytes).decode("utf-8", errors="ignore")

        with state.lock:
            state.last_plaintext = plaintext
            state.last_peer = f"{addr[0]}:{addr[1]}"
            state.receiver_status = f"Đã nhận bản tin từ {state.last_peer}."
            state.receiver_error = ""
    except (TimeoutError, OSError, ValueError, ConnectionError) as exc:
        with state.lock:
            state.receiver_status = "Không nhận được bản tin mới."
            state.receiver_error = str(exc)
    finally:
        with state.lock:
            state.receiver_running = False


app = create_app()


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
