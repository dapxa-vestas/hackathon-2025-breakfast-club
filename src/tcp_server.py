import socket
import json
import time

# TCP server that streams windspeed and wind direction data from a JSON file to a client
# The stream is infinite: when the end of the data is reached, it starts over

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

# Load windspeed data from JSON file
with open('../data/wind_data.json', 'r') as f:
    wind_data = json.load(f)["data"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Bind to address and port
    s.listen()            # Start listening for connections
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()  # Accept a client connection
    with conn:
        print('Connected by', addr)
        # Infinite stream: loop over wind_data forever
        while True:
            for entry in wind_data:
                # Prepare JSON object with unit_id, wind_speed, and wind_direction
                out = {
                    "unit_id": entry["unit_id"],
                    "wind_speed": entry["wind_speed"],
                    "wind_direction": entry.get("wind_direction", None)
                }
                # Send as line-delimited JSON
                json_str = json.dumps(out) + '\n'
                conn.sendall(json_str.encode())
                print(f"Sent: {json_str.strip()}")
                time.sleep(0.1)  # Wait 100ms before sending next
