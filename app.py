from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}  # Format: {'ROOMCODE': {'players': [names]}}

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host')
def join():
    return render_template('host.html')

@socketio.on('create_room')
def create_room():
    room_code = generate_room_code()
    rooms[room_code] = {'players': []}

    # This adds the host's socket to the room
    join_room(room_code)

    # Send the room code back to the host
    emit('room_created', {'room': room_code})

@socketio.on('join_room')
def handle_join(data):
    room = data['room'].upper()
    name = data['name'].strip()

    if not name:
        emit('error', {'message': 'Name cannot be empty.'})
        return

    if room not in rooms:
        emit('error', {'message': 'Room not found.'})
        return

    if name in rooms[room]['players']:
        emit('error', {'message': f'Name "{name}" is already taken in this room.'})
        return

    rooms[room]['players'].append(name)
    join_room(room)
    emit('join_success')
    emit('update_players', {'players': rooms[room]['players']}, room=room)

@socketio.on('start_game')
def start_game(roomCode):
    if len(rooms[roomCode]["players"]) > 1:
        print("start")
        emit('start_game')
    else:
        print("no start")




        






if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)