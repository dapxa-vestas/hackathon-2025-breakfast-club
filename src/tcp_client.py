import socket
import json
from collections import defaultdict

# TCP client that connects to the server and receives streamed windspeed and wind direction data
# Stores wind speeds and wind directions by unit_id and calculates averages for each unit_id on every new data point

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

wind_speeds = defaultdict(list)      # Store wind speeds for each unit_id
wind_directions = defaultdict(list)  # Store wind directions for each unit_id

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
                wind_direction = obj.get('wind_direction', None)
                wind_speeds[unit_id].append(wind_speed)  # Store wind speed
                if wind_direction is not None:
                    wind_directions[unit_id].append(wind_direction)  # Store wind direction
                avg_speed = sum(wind_speeds[unit_id]) / len(wind_speeds[unit_id])
                avg_dir = (sum(wind_directions[unit_id]) / len(wind_directions[unit_id])) if wind_directions[unit_id] else None
                print(f"unit_id: {unit_id}, wind_speed: {wind_speed}, avg_speed: {avg_speed:.2f}, wind_direction: {wind_direction}, avg_direction: {avg_dir:.2f}" if avg_dir is not None else f"unit_id: {unit_id}, wind_speed: {wind_speed}, avg_speed: {avg_speed:.2f}, wind_direction: {wind_direction}")
