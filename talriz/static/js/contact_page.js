const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    add_to_chat(message);
}

function send_message() {
    const chatTextBox = document.getElementById("chat-text-box");
    let seller = document.getElementById("seller_user").value;
    let buyer = document.getElementById("logged_user").value;
    const message = chatTextBox.value;

    let jsonString = {'message': message, 'buyer': buyer,'seller': seller};
    chatTextBox.value = "";
    socket.send(JSON.stringify(jsonString));
}

function add_to_chat(messageJSON) {
    const chatMessages = document.getElementById("chat-messages");

    chatMessages.insertAdjacentHTML("beforeend", message_to_html(messageJSON))
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
    console.log('Message added')
    
    request = new XMLHttpRequest();
    request.open("POST", "/submit-messages/");
    
    csrf_token = "";
    for (let cookie of document.cookie.split("; ")) {
    let [key, value] = cookie.split("=");
        if (key === "csrftoken") {
            csrf_token = value;
        }
    }
    request.setRequestHeader("X-CSRFToken", csrf_token);

    request.send(JSON.stringify(messageJSON));
}

function message_to_html(messageJSON) { 
    const username = messageJSON.buyer;
    const message = messageJSON.message;

    let messageHTML = "<div> <sender><b>" + username + "</b>: " + message + "</sender></div>";

    return messageHTML;
}