const socket = io();
  let roomCode = '';

  document.getElementById('create_room_button').addEventListener('click', function() {
  socket.emit('create_room');
  document.getElementById('create_room_button').style.display = 'none';
  document.getElementById('player-list').style.display = '';
  document.getElementById('room-code').style.display = '';
  document.getElementById('join_text').style.display = '';
  document.getElementById('player-list-head').style.display = '';
});

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

socket.on('game_started', () => {
  console.log("game has started");
  document.getElementById("game_started_text").style.display = "flex";
  document.getElementById('intro1a').play();
});
