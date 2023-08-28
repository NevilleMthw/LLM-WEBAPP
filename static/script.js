document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    sendButton.addEventListener('click', function () {
        const message = userInput.value;
        if (message.trim() !== '') {
            addMessage('You', message);
            userInput.value = '';

            fetch('/generate_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_input: message,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    const response = data.response;
                    addMessage('GPT', response);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.textContent = `${sender}: ${text}`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
