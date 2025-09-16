import socket
import json
import time
import threading
import sys

# TCP server that streams windspeed and wind direction data from a JSON file to any connected clients
# The stream is infinite: when the end of the data is reached, it starts over

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432      # Port to listen on

# Load windspeed data from JSON file
with open('../data/wind_data.json', 'r') as f:
    wind_data = json.load(f)["data"]

clients = []  # List of connected client sockets
clients_lock = threading.Lock()
stop_event = threading.Event()

def broadcast_loop():
    idx = 0
    while not stop_event.is_set():
        entry = wind_data[idx]
        out = {
            "unit_id": entry["unit_id"],
            "wind_speed": entry["wind_speed"],
            "wind_direction": entry.get("wind_direction", None)
        }
        json_str = json.dumps(out) + '\n'
        with clients_lock:
            for conn in clients[:]:
                try:
                    conn.sendall(json_str.encode())
                except Exception:
                    clients.remove(conn)
        print(f"Broadcasted: {json_str.strip()}")
        time.sleep(0.1)
        idx = (idx + 1) % len(wind_data)

def client_accept_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while not stop_event.is_set():
            try:
                s.settimeout(1.0)
                conn, addr = s.accept()
                with clients_lock:
                    clients.append(conn)
                print(f"Client connected: {addr}")
            except socket.timeout:
                continue

try:
    threading.Thread(target=broadcast_loop, daemon=True).start()
    client_accept_loop()
except KeyboardInterrupt:
    print("\nBroadcast interrupted by user. Shutting down...")
    stop_event.set()
    with clients_lock:
        for conn in clients:
            try:
                conn.close()
            except Exception:
                pass
    sys.exit(0)
