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

    // RNG formula
    min = BigInt(-9223372036854775808n);
    max = BigInt(9223372036854775807n);
    const range = max - min + 1n;
    const ret = min + BigInt(Math.floor(Math.random() * Number(range)));

    const id = String(ret)

    let jsonString = {'message': message, 'buyer': buyer,'seller': seller, 'id': id};
    chatTextBox.value = "";
    socket.send(JSON.stringify(jsonString));
}

function add_to_chat(messageJSON) {
    console.log(messageJSON);
    let messageSeller = messageJSON['seller']
    let messageBuyer = messageJSON['buyer']

    let currentSeller = document.getElementById("seller_user").value;
    let currentBuyer = document.getElementById("logged_user").value;

    const chatMessages = document.getElementById("chat-messages");
    // Add to live chat
    if ((messageSeller === currentSeller && messageBuyer === currentBuyer)) {
        chatMessages.insertAdjacentHTML("beforeend", sender_to_html(messageJSON));
        chatMessages.scrollIntoView(false);
        chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
        console.log('Message added');
    } else if (messageBuyer === currentSeller && messageSeller === currentBuyer) {
        chatMessages.insertAdjacentHTML("beforeend", receiver_to_html(messageJSON));
        chatMessages.scrollIntoView(false);
        chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
        console.log('Message added');
    }

    // Saves to database
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

function sender_to_html(messageJSON) { 
    const username = messageJSON.buyer;
    const message = messageJSON.message;


    let messageHTML = "<div style='display: flex; justify-content: flex-end'>" + "<div> <sender>" + message + "</sender></div></div>"
    
    return messageHTML;
}
function receiver_to_html(messageJSON) { 
    const username = messageJSON.buyer;
    const message = messageJSON.message;

    let messageHTML = "<div> <receiver>" + message + "</receiver></div>";

    return messageHTML;
}