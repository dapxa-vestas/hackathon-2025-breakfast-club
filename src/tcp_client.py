import socket
import json
import time
import threading
import sys
from collections import defaultdict, deque

# TCP client that connects to the upstream server and receives streamed windspeed and wind direction data
# Calculates running state and streams unit_id and running state to any listener via TCP

HOST = 'breakfast-club-app-server'  # Upstream server's hostname or IP address
PORT = 65432        # Upstream server port
BROADCAST_PORT = 65433  # Port to broadcast running state

wind_speeds = defaultdict(deque)
WINDOW_SECONDS = 10

listeners = []  # List of sockets to broadcast to
stop_event = threading.Event()

# Function to broadcast running state to all listeners
def broadcast(unit_id, running):
    msg = json.dumps({'unit_id': unit_id, 'running': running}) + '\n'
    print(f"Broadcast message: {msg.strip()}")  # Print the actual message sent
    for conn in listeners[:]:
        try:
            conn.sendall(msg.encode())
            print(f"Sent to listener: unit_id={unit_id}, running={running}")
        except Exception:
            listeners.remove(conn)
            print("Listener connection lost, removed from list.")

# Thread to accept listener connections
def listener_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('0.0.0.0', BROADCAST_PORT))
        server_sock.listen()
        print(f"Broadcast server listening on port {BROADCAST_PORT}")
        while not stop_event.is_set():
            try:
                server_sock.settimeout(1.0)
                conn, addr = server_sock.accept()
                listeners.append(conn)
                print(f"Listener connected: {addr}")
            except socket.timeout:
                continue

def connect_and_stream():
    while not stop_event.is_set():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Attempting to connect to {HOST}:{PORT}...")
                s.settimeout(5.0)
                s.connect((HOST, PORT))  # Connect to the upstream server
                print(f"Connected to {HOST}:{PORT}")
                buffer = ''
                while not stop_event.is_set():
                    try:
                        s.settimeout(1.0)
                        data = s.recv(1024)
                        if not data:
                            print("Connection lost. Reconnecting...")
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
                    except socket.timeout:
                        continue
        except (ConnectionRefusedError, OSError):
            print(f"ERROR: Could not connect to {HOST}:{PORT}. Retrying in 5 seconds...")
            time.sleep(5)

threading.Thread(target=listener_server, daemon=True).start()

try:
    connect_and_stream()
except KeyboardInterrupt:
    print("\nClient interrupted by user. Shutting down...")
    stop_event.set()
    for conn in listeners:
        try:
            conn.close()
        except Exception:
            pass
    sys.exit(0)
