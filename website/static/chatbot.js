const ICON = "/home/rindfleisch/mysite/website/static/assets/BRAND_LOGO.png";

messageEvent = document.getElementById("inputMessage");
messageEvent.addEventListener("keyup", function(event) {
    let chatMessages = document.getElementById("chat-messages");
    if (event.key == "Enter") {
        let message = messageEvent.value;

        let userMessage = document.createElement("li");
        userMessage.classList.add("message-box");
        userMessage.textContent = message;
        chatMessages.appendChild(userMessage);

        // Add typing indicator with avatar and animated dots
        let typingIndicator = document.createElement("li");
        typingIndicator.classList.add("answer-box");
        typingIndicator.id = "typing-indicator";

        let img = document.createElement("img");
        img.src = ICON;
        img.alt = "Flei Icon";

        let typingText = document.createElement("span");
        typingText.textContent = "Flei is typing";

        let dot1 = document.createElement("span");
        dot1.classList.add("dot");
        dot1.textContent = "·";

        let dot2 = document.createElement("span");
        dot2.classList.add("dot");
        dot2.textContent = "·";

        let dot3 = document.createElement("span");
        dot3.classList.add("dot");
        dot3.textContent = "·";

        typingIndicator.appendChild(img);
        typingIndicator.appendChild(typingText);
        typingIndicator.appendChild(dot1);
        typingIndicator.appendChild(dot2);
        typingIndicator.appendChild(dot3);
        chatMessages.appendChild(typingIndicator);

        chatMessages.scrollTop = chatMessages.scrollHeight;
        messageEvent.value = "";

        // Simulate delay before showing the response
        setTimeout(() => {
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                typingIndicator.remove();

                // Bot answer
                let botAnswer = document.createElement("li");
                botAnswer.classList.add("answer-box");

                let img = document.createElement("img");
                img.src = ICON;
                img.alt = "Flei Icon";

                let answerSpan = document.createElement("span");
                answerSpan.id = "answer";
                answerSpan.textContent = data.answer;

                botAnswer.appendChild(img);
                botAnswer.appendChild(answerSpan);
                chatMessages.appendChild(botAnswer);

                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
        }, 2000);
    }
});


function toggleChatContainer() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
        chatContainer.style.display = 'block';
    } else {
        chatContainer.style.display = 'none';
    }
}


