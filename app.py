from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}  # Format: {'ROOMCODE': {'players': [names]},{'current_game_state': 0-4}}



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
    rooms[room_code] = {
        'players': [],
        'current_game_state': 0
                        }

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
    
    if rooms[room]['current_game_state'] != 0:
        emit('error', {'message': 'Room has already started.'})
        return

    if name in rooms[room]['players']:
        emit('error', {'message': f'Name "{name}" is already taken in this room.'})
        return
    if rooms[room]['players'] == []:
        rooms[room]['players'].append(name)
        join_room(room)
        emit('first_join_success')
        emit('update_players', {'players': rooms[room]['players']}, room=room)
    else:
        rooms[room]['players'].append(name)
        join_room(room)
        emit('join_success')
        emit('update_players', {'players': rooms[room]['players']}, room=room)

@socketio.on('start_game')
def start_game(roomCode):
    roomCode = roomCode.upper()
    if len(rooms[roomCode]["players"]) > 1:
        print("start")
        rooms[roomCode]["current_game_state"] = 1
        emit('game_started', room=roomCode)
    else:
        print("no start")
        emit('error', {'message': 'Not enough players!'})

@socketio.on('rejoin_room')
def handle_rejoin(data):
    room = data['room'].upper()
    name = data['name'].strip()

    if room not in rooms or name not in rooms[room]['players']:
        emit('error', {'message': 'Rejoin failed. Room or player not found.'})
        return

    join_room(room)
    emit('join_success')
    emit('update_players', {'players': rooms[room]['players']}, room=room)


        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)