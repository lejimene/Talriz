const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    add_to_chat(message);
}

function send_message() {
    const chatTextBox = document.getElementById("chat-text-box");
    
    let username = document.getElementById("logged_user").value;

    const message = chatTextBox.value;
    chatTextBox.value = "";
    socket.send(JSON.stringify({'message': message, 'username': username}));
}

function add_to_chat(messageJSON) {
    const chatMessages = document.getElementById("chat-messages");

    chatMessages.insertAdjacentHTML("beforeend", message_to_html(messageJSON))
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
    console.log('Message added')
}

function message_to_html(messageJSON) { 
    const username = messageJSON.username;
    const message = messageJSON.message;

    let messageHTML = "<div> <sender><b>" + username + "</b>: " + message + "</sender></div>";

    return messageHTML;
}