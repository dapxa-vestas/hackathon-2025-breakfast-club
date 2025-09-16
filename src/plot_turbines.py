import json
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, send_file, render_template_string
import io
import threading
import socket

app = Flask(__name__)

# Shared dictionary for running states
running_states = {}

def read_coordinates(filepath='../data/turbine_coordinates.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
    lats = [unit['Latitude'] for unit in data['units']]
    lons = [unit['Longitude'] for unit in data['units']]
    ids = [unit['unit_id'] for unit in data['units']]
    return lats, lons, ids



def create_plot():
    lats, lons, ids = read_coordinates('../data/turbine_coordinates.json')
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#eaf6fb')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Choose color based on running state
    colors = []
    for unit_id in ids:
        if running_states.get(unit_id) is True:
            colors.append('green')
        elif running_states.get(unit_id) is False:
            colors.append('red')
        else:
            colors.append('gray')  # Unknown state

    # Draw dots for turbines
    ax.scatter(lons, lats, color=colors, s=80, zorder=3, edgecolor='white', linewidth=1.5)
    for lon, lat, unit_id in zip(lons, lats, ids):
        ax.text(lon, lat + 0.002, unit_id, fontsize=11, ha='center', va='bottom', fontweight='bold', color='#1a5276')

    ax.set_xlabel('Longitude', fontsize=13, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=13, fontweight='bold')
    ax.set_title('Wind Turbine Locations', fontsize=18, fontweight='bold', color='#154360')
    ax.set_aspect('equal', adjustable='datalim')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf

@app.route('/')
def index():
    html = '''
    <html>
    <head><title>Turbine Plot</title></head>
    <body style="background-color:#f4faff; font-family:sans-serif;">
        <h1 style="color:#154360;">Wind Turbine Locations</h1>
        <img id="plotimg" src="/plot.png" alt="Turbine Plot" style="border:2px solid #154360; box-shadow:2px 2px 8px #b0c4de;">
        <script>
        setInterval(function() {
            var img = document.getElementById('plotimg');
            img.src = '/plot.png?' + new Date().getTime(); // Prevent caching
        }, 2000);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/plot.png')
def plot_png():
    buf = create_plot()
    return send_file(buf, mimetype='image/png')

def tcp_listener(host='127.0.0.1', port=65433):
    """Listen to TCP broadcast and update running_states."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        buffer = ''
        while True:
            data = s.recv(1024)
            if not data:
                break
            buffer += data.decode()
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line:
                    try:
                        obj = json.loads(line)
                        running_states[obj['unit_id']] = obj['running']
                        print(f"unit_id: {obj['unit_id']}, running: {obj['running']}")
                    except Exception as e:
                        print(f"Error parsing broadcast: {e}")

threading.Thread(target=tcp_listener, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)