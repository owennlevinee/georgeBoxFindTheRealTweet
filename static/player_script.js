const socket = io();

window.onload = () => {
  const storedRoom = localStorage.getItem('room');
  const storedName = localStorage.getItem('name');
  console.log(storedRoom, storedName);
  if (storedRoom && storedName) {
    socket.emit('rejoin_room', { room: storedRoom, name: storedName });
  }
}; //handle accidental refreshes


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
  localStorage.setItem('room', document.getElementById('room').value);
  localStorage.setItem('name', document.getElementById('name').value);
});

socket.on('error', (data) => {
  document.getElementById('status').innerText = data.message;
});

socket.on('first_join_success', () =>{
  document.getElementById('room').style.display = "none";
  document.getElementById('name').style.display = "none";
  document.getElementById('join').style.display = "none";
  document.getElementById('joined_first').style.display = "flex";
  document.getElementById('start_game_button').style.display = "flex";
  localStorage.setItem('room', document.getElementById('room').value);
  localStorage.setItem('name', document.getElementById('name').value);
});

function startGame(){
  socket.emit('start_game', localStorage.getItem('room'));
}