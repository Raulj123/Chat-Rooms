<script lang="ts">
  import { onMount } from "svelte";
  import Room from "./components/chatRoom.svelte";
  let client_id = Date.now();
  let roomID: any = null;
  let users: any;
  let ws: any;
  let conn: any;

  function sendMessage(event: Event) {
    event.preventDefault();
    var input = document.getElementById("messageText") as HTMLInputElement;
    if (input !== null) {
      ws.send(input.value);
      console.log(input.value);
      input.value = "";
      console.log(input.value);
    }
  }
  async function createRoom() {
    try {
      const room_id = Math.floor(Math.random() * 90000) + 10000;
      const api2 = `http://127.0.0.1:8000/create_room/${room_id}`;
      const res = await fetch(api2, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      roomID = data.roomID;
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function sendRoom(event: Event) {
    event.preventDefault();
    console.log("room");
    try {
      const roomIdInput = document.getElementById(
        "room_id"
      ) as HTMLInputElement;
      if (roomIdInput != null) {
        const roomId = roomIdInput.value;
        const api3 = "ws://127.0.0.1:8000/join_room/" + roomId;
        ws = new WebSocket(api3);
        conn = false;
        ws.onopen = () => {
          console.log("WebSocket connection established.");
          conn = true;
        };
        // const api4 = "http://127.0.0.1:8000/users/" + roomId;
        // try {
        //   const res = await fetch(api4, {
        //     method: "GET",
        //     headers: {
        //       "Content-Type": "application/json",
        //     },
        //   });
        //   const data = await res.json();
        //   users = data.num_people;
        //   console.log(users);
        // } catch (error) {
        //   console.error("Error:", error);
        // }
        ws.onmessage = function (event: MessageEvent) {
          var messages = document.getElementById("messages");
          if (messages !== null) {
            var message = document.createElement("li");
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
          }
        };
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
</script>

<div class="container">
  <div class="sidebar">
    <p>
      Private chats!
      <br />
      <small>Create or join a room</small>
    </p>

    <button on:click={createRoom}>Create Room</button>
    {#if roomID != null}
      <p>Your room id is {roomID}</p>
    {/if}

    <div class="form">
      <h3>Join Room</h3>
      <form method="post" action="" on:submit={sendRoom}>
        <input
          type="text"
          id="room_id"
          autocomplete="off"
          placeholder="Enter room id"
        />
        <button>Submit</button>
      </form>
    </div>
  </div>
  <div class="main">
    {#if users}
      users In this room: {users}
    {/if}
    {#if conn == true}
      <ul id="messages"></ul>
      <form class="send" action="" on:submit={sendMessage}>
        <input type="text" id="messageText" autocomplete="off" />
        <button>Send</button>
      </form>
    {/if}
   
  </div>
  
</div>

<style>
  button {
    width: 100px;
    height: 50px;
  }
  input[type="text"] {
    width: 250px;
    height: 30px;
    border-radius: 5px;
    border: none;
  }
  #messages {
    height: 200px;
    overflow-y: auto;
    list-style-type: none;
    padding: 0;
    margin: 0 auto;
    text-align: center;
  }
  .send input {
    width: 200px;
  }
  .container {
    display: flex;
  }
  .container button {
    height: 35px;
  }
  .sidebar {
    flex: 0 0 30%;
    padding: 0 1rem;
    border: 1px solid black;
    height: 100vh;
    background-color: rgb(19, 19, 19);
    max-width: 250px;
    border-radius: 10px;
  }
  .sidebar button,
  .form button,
  .send button {
    margin-top: 0.7rem;
  }
  .main {
    flex: 1;
    padding: 0 1rem;
  }
  .form {
    margin-top: 30px;
  }
  .form h3 {
    margin-bottom: 5px;
  }
 .main input {
  width: 500px;
 }
 .main form {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  text-align: center;
  margin-bottom: 20px;
 }
</style>
