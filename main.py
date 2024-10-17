from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import eventlet

app = Flask(__name__)
socketio = SocketIO(app)
canvas_state = [['#FFFFFF' for _ in range(256)] for _ in range(256)]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clicker')
def clicker():
    return render_template('clicker.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/pixel-drawing')
def cell_simulator():
    return render_template('pixel_drawing.html')

@socketio.on('draw_pixel')
def handle_draw_pixel(data):
    x, y, color = data['x'], data['y'], data['color']
    canvas_state[x][y] = color
    emit('draw_pixel', data, broadcast=True)

@socketio.on('request_canvas_state')
def handle_request_canvas_state():
    emit('initialize_canvas', canvas_state)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=1000, debug=True)
