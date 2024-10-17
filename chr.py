
from flask import Flask, render_template_string
from flask_socketio import SocketIO, send,emit
import eventlet

app = Flask(__name__)
socketio = SocketIO(app)
canvas_state = [['#FFFFFF' for _ in range(256)] for _ in range(256)]
@app.route('/')
def home():
    home_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="icon" type="image/png" href="/static/favicon.png">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to the Home Page</h1>
        <a href="/clicker">Clicker Game</a><br>
        <a href="/chat">Chat</a><br>
        <a href="/pixel-drawing">pixel-drawing</a>
    </body>
    </html>
    """
    return render_template_string(home_html)

@app.route('/clicker')
def clicker():
    clicker_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clicker Game</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            #clicker-button {
                padding: 20px;
                font-size: 20px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Clicker Game</h1>
        <p>Score: <span id="score">0</span></p>
        <button id="clicker-button">Click me!</button>
        <script>
            let score = 0;
            document.getElementById('clicker-button').addEventListener('click', function() {
                score++;
                document.getElementById('score').innerText = score;
            });
        </script>
        <a href="/">Home</a>
    </body>
    </html>
    """
    return render_template_string(clicker_html)

@app.route('/chat')
def chat():
    chat_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            #chat {
                margin-top: 20px;
            }
            #messages {
                border: 1px solid #ccc;
                height: 200px;
                overflow-y: scroll;
                padding: 10px;
            }
            #message-input {
                width: 80%;
                padding: 10px;
            }
            #send-button {
                padding: 10px;
            }
            #username-prompt {
                display: none;
            }
            #logout-button {
                margin-top: 20px;
                padding: 10px;
            }
        </style>
    </head>
    <body>
        <div id="username-prompt">
            <h2>Enter your username</h2>
            <input id="username-input" type="text" placeholder="Username">
            <button id="set-username-button">Set Username</button>
            <p id="username-error" style="color: red; display: none;">Invalid username. Must start with a letter and contain only letters, numbers, and underscores.</p>
        </div>
        <div id="chat-section" style="display: none;">
            <h2>Chat</h2>
            <div id="messages"></div>
            <input id="message-input" type="text" placeholder="Type a message...">
            <button id="send-button">Send</button>
            <button id="logout-button">Logout</button>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io();
            const messages = document.getElementById('messages');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const usernamePrompt = document.getElementById('username-prompt');
            const chatSection = document.getElementById('chat-section');
            const usernameInput = document.getElementById('username-input');
            const setUsernameButton = document.getElementById('set-username-button');
            const logoutButton = document.getElementById('logout-button');
            const usernameError = document.getElementById('username-error');

            function isValidUsername(username) {
                const regex = /^[a-zA-Z][a-zA-Z0-9_]*$/;
                return regex.test(username);
            }

            function setUsername() {
                const username = usernameInput.value;
                if (isValidUsername(username)) {
                    localStorage.setItem('username', username);
                    usernamePrompt.style.display = 'none';
                    chatSection.style.display = 'block';
                    usernameError.style.display = 'none';
                } else {
                    usernameError.style.display = 'block';
                }
            }

            function logout() {
                localStorage.removeItem('username');
                usernamePrompt.style.display = 'block';
                chatSection.style.display = 'none';
            }

            setUsernameButton.addEventListener('click', setUsername);
            usernameInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    setUsername();
                }
            });
            logoutButton.addEventListener('click', logout);

            const storedUsername = localStorage.getItem('username');
            if (storedUsername) {
                usernamePrompt.style.display = 'none';
                chatSection.style.display = 'block';
            } else {
                usernamePrompt.style.display = 'block';
                chatSection.style.display = 'none';
            }

            socket.on('message', function(msg) {
                const messageElement = document.createElement('div');
                messageElement.innerHTML = msg;
                messages.appendChild(messageElement);
                messages.scrollTop = messages.scrollHeight;
            });

            sendButton.addEventListener('click', function() {
                const message = messageInput.value;
                const username = localStorage.getItem('username');
                if (message && username) {
                    socket.send(username + ': ' + message);
                    messageInput.value = '';
                }
            });

            messageInput.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    sendButton.click();
                }
            });
        </script>
        <a href="/">Home</a>
    </body>
    </html>
    """
    return render_template_string(chat_html)

@app.route('/pixel-drawing')
def cell_simulator():
    cell_simulator_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Collaborative Pixel Drawing</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            #canvas {
                border: 1px solid black;
                margin-top: 20px;
                image-rendering: pixelated;
            }
            #controls {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Collaborative Pixel Drawing</h1>
        <canvas id="canvas" width="512" height="512"></canvas>
        <div id="controls">
            <input type="color" id="color-picker" value="#000000">
            <button id="draw-button">Draw</button>
            <button id="erase-button">Erase</button>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const colorPicker = document.getElementById('color-picker');
            const drawButton = document.getElementById('draw-button');
            const eraseButton = document.getElementById('erase-button');
            const resolution = 2; // Each pixel is 2x2 on the canvas
            const COLS = canvas.width / resolution;
            const ROWS = canvas.height / resolution;
            let drawing = false;
            let erasing = false;

            const socket = io();

            canvas.addEventListener('mousedown', () => drawing = true);
            canvas.addEventListener('mouseup', () => drawing = false);
            canvas.addEventListener('mousemove', draw);

            drawButton.addEventListener('click', () => {
                erasing = false;
                drawButton.disabled = true;
                eraseButton.disabled = false;
            });

            eraseButton.addEventListener('click', () => {
                erasing = true;
                drawButton.disabled = false;
                eraseButton.disabled = true;
            });

            function draw(event) {
                if (!drawing) return;
                const x = Math.floor(event.offsetX / resolution);
                const y = Math.floor(event.offsetY / resolution);
                const color = erasing ? '#FFFFFF' : colorPicker.value;
                socket.emit('draw_pixel', { x, y, color });
            }

            socket.on('draw_pixel', ({ x, y, color }) => {
                ctx.fillStyle = color;
                ctx.fillRect(x * resolution, y * resolution, resolution, resolution);
            });

            socket.on('initialize_canvas', (canvasState) => {
                for (let x = 0; x < COLS; x++) {
                    for (let y = 0; y < ROWS; y++) {
                        ctx.fillStyle = canvasState[x][y];
                        ctx.fillRect(x * resolution, y * resolution, resolution, resolution);
                    }
                }
            });

            function initializeCanvas() {
                socket.emit('request_canvas_state');
            }

            initializeCanvas();
        </script>
        <a href="/">Home</a>
    </body>
    </html>
    """
    return render_template_string(cell_simulator_html)

@socketio.on('draw_pixel')
def handle_draw_pixel(data):
    x, y, color = data['x'], data['y'], data['color']
    canvas_state[x][y] = color
    emit('draw_pixel', data, broadcast=True)

@socketio.on('request_canvas_state')
def handle_request_canvas_state():
    emit('initialize_canvas', canvas_state)

@app.route('/about')
def about():
    about_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About</title>
    </head>
    <body>
        <h1>About Us</h1>
        <p>This is the about page.</p>
        <a href="/">Home</a>
    </body>
    </html>
    """
    return render_template_string(about_html)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == "__main__":
    # Run Flask application with eventlet
    socketio.run(app, host='0.0.0.0', port=1000, debug=True)
