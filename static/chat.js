let isTestActive = false;

document.getElementById('psych-test-btn').addEventListener('click', async () => {
    if (isTestActive) return;
    
    isTestActive = true;
    document.getElementById('psych-test-btn').style.display = 'none';
    document.getElementById('end-test-btn').style.display = 'block';
    
    addMessage("Ok, I understand you want to take up a psychometric analysis.", 'bot-message');
    startPsychometricTest();
});

document.getElementById('end-test-btn').addEventListener('click', () => {
    isTestActive = false;
    document.getElementById('psych-test-btn').style.display = 'block';
    document.getElementById('end-test-btn').style.display = 'none';
    addMessage("Psychometric test ended. Thank you for participating!", 'bot-message');
});

async function startPsychometricTest() {
    try {
        const response = await fetch('/start_psych_test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const data = await response.json();
        addMessage(data.response, 'bot-message');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error starting the test.', 'bot-message');
    }
}

document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user-message');
    input.value = '';

    try {
        const response = await fetch(isTestActive ? '/psych_test_response' : '/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        addMessage(data.response, 'bot-message');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your request.', 'bot-message');
    }
});

function addMessage(text, className) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    // Format the text if it contains specific patterns
    if (className === 'bot-message') {
        // Split by periods to handle different points
        const sentences = text.split('.');
        let formattedText = '';
        
        if (sentences.length > 1) {
            formattedText = '<div class="structured-response">';
            sentences.forEach(sentence => {
                if (sentence.trim()) {
                    // Check if sentence contains a list-like pattern
                    if (sentence.includes(',') && (sentence.includes('include') || sentence.includes('need'))) {
                        const parts = sentence.split(',');
                        formattedText += `<h3>${parts[0]}</h3><ul>`;
                        parts.slice(1).forEach(part => {
                            formattedText += `<li>${part.trim()}</li>`;
                        });
                        formattedText += '</ul>';
                    } else {
                        formattedText += `<p>${sentence.trim()}.</p>`;
                    }
                }
            });
            formattedText += '</div>';
        } else {
            formattedText = text;
        }
        
        messageDiv.innerHTML = formattedText;
    } else {
        messageDiv.textContent = text;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
} 
