import socket
import threading
import json

# ─── Network configuration ───────────────────────────────────────────────────
HOST = "127.0.0.1"   # Localhost – all clients must run on the same machine
PORT = 65432          # Arbitrary non-privileged port

# ─── Shared server state (protected by lock for thread safety) ────────────────
clients = []   # List of active client sockets, used to broadcast results
results = []   # Accumulated list of result dicts from every connected client
lock = threading.Lock()  # Ensures only one thread modifies clients/results at a time


def handle_client(conn, addr):
    """Handle a single client connection.

    Each client sends one JSON payload containing its ranking result, then waits
    to receive the full broadcast of all results collected so far.  Multiple
    clients can connect simultaneously; each is served by its own thread.
    """
    print(f"[SERVER] New connection from {addr}")
    try:
        # ── Step 1: Receive the client result (JSON string ending with \n) ──
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\n" in data:
                break

        # ── Step 2: Parse the JSON payload ────────────────────────────────────
        if data:
            payload = json.loads(data.decode().strip())
            username   = payload.get("username",  addr[0])
            top_city   = payload.get("top_city",  "Unknown")
            top_score  = payload.get("top_score", 0)
            career     = payload.get("career",    "Unknown")

            # ── Step 3: Store the result in the shared results list ───────────
            with lock:
                results.append({
                    "username":  username,
                    "top_city":  top_city,
                    "top_score": top_score,
                    "career":    career,
                })
            print(f"[SERVER] Result received from {username}: {top_city} ({top_score}/100)")

            # ── Step 4: Broadcast all collected results to THIS client ─────────
            # The client will use the friend cities to re-weight its own ranking.
            with lock:
                broadcast = json.dumps(results) + "\n"
            conn.sendall(broadcast.encode())

    except Exception as e:
        print(f"[SERVER] Error handling {addr}: {e}")
    finally:
        # ── Step 5: Clean up – remove client from active list and close socket ─
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[SERVER] Connection closed: {addr}")


def main():
    """Start the multi-client TCP server and accept connections indefinitely."""
    print(f"[SERVER] City Ranker Server starting on {HOST}:{PORT}")
    print("[SERVER] Waiting for clients to connect and submit results...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"[SERVER] Listening. Press Ctrl+C to shut down.\n")

        while True:
            # Block until a new client connects, then spawn a daemon thread for it
            conn, addr = server_sock.accept()
            with lock:
                clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == "__main__":
    main()
