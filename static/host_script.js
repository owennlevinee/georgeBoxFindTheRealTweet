const socket = io();
  let roomCode = '';
  window.onload = function() {
    socket.emit('create_room');
  }

  socket.on('room_created', (data) => {
    roomCode = data.room;
    document.getElementById('room-code').innerText = "Room Code: " + roomCode;
  });

  // 👇 This is what should update the player list:
  socket.on('update_players', (data) => {
    const list = document.getElementById('player-list');
    list.innerHTML = '';
    data.players.forEach(player => {
      const li = document.createElement('li');
      li.innerText = player;
      list.appendChild(li);
    });
  });

function startGame() {
    socket.emit('start_game', roomCode);
}