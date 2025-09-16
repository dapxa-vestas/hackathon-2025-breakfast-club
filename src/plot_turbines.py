import json
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, send_file, render_template_string
import io

app = Flask(__name__)

def read_coordinates(filepath='../data/turbine_coordinates.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
    lats = [unit['Latitude'] for unit in data['units']]
    lons = [unit['Longitude'] for unit in data['units']]
    ids = [unit['unit_id'] for unit in data['units']]
    return lats, lons, ids

def read_wind_speeds(filepath='../data/wind_data.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
    speeds = [unit.get('wind_speed', None) for unit in data['units']]
    return speeds

def read_wind_directions(filepath='../data/wind_data.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
    directions = [unit.get('wind_direction', None) for unit in data['units']]
    return directions

def draw_wind_turbine(ax, x, y, size=0.008, color='green'):
    ax.plot([x, x], [y, y - size * 2], color='gray', lw=2, zorder=2)
    hub = plt.Circle((x, y), size * 0.3, color=color, zorder=3)
    ax.add_patch(hub)
    for angle in [0, 120, 240]:
        theta = np.deg2rad(angle)
        blade_x = x + size * np.cos(theta)
        blade_y = y + size * np.sin(theta)
        ax.plot([x, blade_x], [y, blade_y], color='black', lw=1, zorder=3)

def create_plot():
    lats, lons, ids = read_coordinates('../data/turbine_coordinates.json')
    try:
        wind_speeds = read_wind_speeds('../data/wind_data.json')
        wind_dirs = read_wind_directions('../data/wind_data.json')
    except Exception:
        wind_speeds = [None] * len(ids)
        wind_dirs = [None] * len(ids)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#eaf6fb')
    ax.grid(True, linestyle='--', alpha=0.5)

    for lon, lat, unit_id, ws, wd in zip(lons, lats, ids, wind_speeds, wind_dirs):
        draw_wind_turbine(ax, lon, lat, size=0.01)
        label = f"{unit_id}"
        if ws is not None:
            label += f"\n{ws} m/s"
        if wd is not None:
            label += f"\n{wd}°"
        ax.text(lon, lat + 0.002, label, fontsize=10, ha='center', va='bottom', fontweight='bold', color='#1a5276')

    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.set_title('Wind Turbine Locations with Wind Speed & Direction', fontsize=16, fontweight='bold', color='#154360')
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
    <body>
        <h1>Wind Turbine Locations</h1>
        <img src="/plot.png" alt="Turbine Plot">
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/plot.png')
def plot_png():
    buf = create_plot()
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)