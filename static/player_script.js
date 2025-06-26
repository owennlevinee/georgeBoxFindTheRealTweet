const socket = io();

// PLAYER SIDE
function joinGame() {
  const room = document.getElementById('room').value;
  const name = document.getElementById('name').value;
  socket.emit('join_room', { room, name });
}

socket.on('join_success', (data) => {
  document.getElementById('room').style.display = "none";
  document.getElementById('name').style.display = "none";
  document.getElementById('join').style.display = "none";
  document.getElementById('joined').style.display = "flex";
});

socket.on('error', (data) => {
  document.getElementById('status').innerText = data.message;
});

