document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');

    sendBtn.addEventListener('click', async () => {
        const message = userInput.value;
        if (!message) return;

        appendMessage('user', message);
        userInput.value = '';

        try {
            const response = await fetch('/api/test_user/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();
            // The response might contain a formatted string with newlines
            appendMessage('assistant', data.response.replace(/\n/g, '<br>'));

        } catch (error) {
            console.error('Error:', error);
            appendMessage('assistant', 'Sorry, something went wrong.');
        }
    });

    function appendMessage(role, content) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble', role);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = content;

        messageBubble.appendChild(messageContent);
        chatContainer.appendChild(messageBubble);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});