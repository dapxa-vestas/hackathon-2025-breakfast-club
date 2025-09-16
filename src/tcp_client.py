import socket
import json
import time
import threading
from collections import defaultdict, deque

# TCP client that connects to the upstream server and receives streamed windspeed and wind direction data
# Calculates running state and streams unit_id and running state to any listener via TCP

HOST = '127.0.0.1'  # Upstream server's hostname or IP address
PORT = 65432        # Upstream server port
BROADCAST_PORT = 65433  # Port to broadcast running state

wind_speeds = defaultdict(deque)
WINDOW_SECONDS = 10

listeners = []  # List of sockets to broadcast to

# Function to broadcast running state to all listeners
def broadcast(unit_id, running):
    msg = json.dumps({'unit_id': unit_id, 'running': running}) + '\n'
    for conn in listeners[:]:
        try:
            conn.sendall(msg.encode())
        except Exception:
            listeners.remove(conn)

# Thread to accept listener connections
def listener_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('0.0.0.0', BROADCAST_PORT))
        server_sock.listen()
        print(f"Broadcast server listening on port {BROADCAST_PORT}")
        while True:
            conn, addr = server_sock.accept()
            listeners.append(conn)
            print(f"Listener connected: {addr}")

threading.Thread(target=listener_server, daemon=True).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the upstream server
    buffer = ''
    while True:
        data = s.recv(1024)
        if not data:
            break
        buffer += data.decode()
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            if line:
                obj = json.loads(line)
                unit_id = obj['unit_id']
                wind_speed = obj['wind_speed']
                timestamp = time.time()
                wind_speeds[unit_id].append((timestamp, wind_speed))
                while wind_speeds[unit_id] and timestamp - wind_speeds[unit_id][0][0] > WINDOW_SECONDS:
                    wind_speeds[unit_id].popleft()
                avg_speed = sum(val for _, val in wind_speeds[unit_id]) / len(wind_speeds[unit_id])
                running = avg_speed < 10
                broadcast(unit_id, running)
