import socket
import json
from collections import defaultdict

# TCP client that connects to the server and receives streamed windspeed data
# Stores wind speeds by unit_id and calculates average for each unit_id on every new data point

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

wind_speeds = defaultdict(list)  # Store wind speeds for each unit_id

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the server
    buffer = ''
    while True:
        data = s.recv(1024)  # Receive data from server
        if not data:
            break
        buffer += data.decode()  # Decode bytes to string and add to buffer
        # Process each line-delimited JSON object
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            if line:
                obj = json.loads(line)  # Parse JSON
                unit_id = obj['unit_id']
                wind_speed = obj['wind_speed']
                wind_speeds[unit_id].append(wind_speed)  # Store wind speed
                avg = sum(wind_speeds[unit_id]) / len(wind_speeds[unit_id])  # Calculate average
                print(f"unit_id: {unit_id}, wind_speed: {wind_speed}, avg: {avg:.2f}")  # Print info
