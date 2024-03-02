<script lang="ts">
import { onMount } from "svelte";
  let ws: any;
  
  function sendMessage(event: Event) {
    event.preventDefault();
    var input = document.getElementById("messageText") as HTMLInputElement;
    if (input !== null) {
      ws.send(input.value);
      input.value = "";
      console.log(input.value);
    }
  }
  onMount(async () => {
    
   
    
    
  });
</script>

Chat room!

User: n
<form action="" on:submit={sendMessage}>
  <input type="text" id="messageText" autocomplete="off" />
  <button>Send</button>
</form>
<ul id="messages"></ul>
