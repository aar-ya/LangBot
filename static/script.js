// Language content configuration
const LANGUAGE_CONTENT = {
  english: {
    placeholder: "Type your message in English...",
    sendButton: "Send",
    footer: "Learning English with AI assistance"
  },
  french: {
    placeholder: "Écrivez votre message en français...",
    sendButton: "Envoyer",
    footer: "Apprentissage du français avec assistance IA"
  },
  spanish: {
    placeholder: "Escribe tu mensaje en español...",
    sendButton: "Enviar",
    footer: "Aprendiendo español con asistencia de IA"
  },
  german: {
    placeholder: "Schreiben Sie Ihre Nachricht auf Deutsch...",
    sendButton: "Senden",
    footer: "Deutsch lernen mit KI-Unterstützung"
  },
  italian: {
    placeholder: "Scrivi il tuo messaggio in italiano...",
    sendButton: "Inviare",
    footer: "Imparare l'italiano con l'assistenza dell'IA"
  },
  hindi: {
    placeholder: "अपना संदेश हिंदी में लिखें...",
    sendButton: "भेजें",
    footer: "एआई सहायता के साथ हिंदी सीखना"
  },
  japanese: {
    placeholder: "メッセージを日本語で入力してください...",
    sendButton: "送信",
    footer: "AIアシスタントと一緒に日本語を学ぶ"
  }
};

// DOM elements
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('sendBtn');
const chatHistory = document.getElementById('chatHistory');
const sendText = document.getElementById('sendText');

// Initialize language content
function initLanguageContent() {
  const content = LANGUAGE_CONTENT[CURRENT_LANGUAGE] || LANGUAGE_CONTENT.english;
  messageInput.placeholder = content.placeholder;
  sendText.textContent = content.sendButton;
  document.querySelector('.footer p').textContent = content.footer;
}

// Add message to chat
function addMessageToChat(content, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;
  
  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';
  avatarDiv.innerHTML = sender === 'user' 
    ? '<i class="fas fa-user"></i>' 
    : '<i class="fas fa-robot"></i>';
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  contentDiv.innerHTML = `<p>${content}</p>`;
  
  messageDiv.appendChild(avatarDiv);
  messageDiv.appendChild(contentDiv);
  chatHistory.appendChild(messageDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Create typing indicator
function createTypingIndicator() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message bot typing';
  
  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';
  avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  contentDiv.innerHTML = `
    <div class="typing-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
  `;
  
  typingDiv.appendChild(avatarDiv);
  typingDiv.appendChild(contentDiv);
  return typingDiv;
}

// Send message to server
async function sendMessage() {
  const message = messageInput.value.trim();
  if (!message) return;
  
  addMessageToChat(message, 'user');
  messageInput.value = '';
  messageInput.style.height = 'auto';
  
  try {
    const typingIndicator = createTypingIndicator();
    chatHistory.appendChild(typingIndicator);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: message,
        language: CURRENT_LANGUAGE
      }),
    });
    
    chatHistory.removeChild(typingIndicator);
    
    if (!response.ok) throw new Error('Network error');
    const data = await response.json();
    addMessageToChat(data.reply, 'bot');
  } catch (error) {
    addMessageToChat("Sorry, I'm having trouble responding. Please try again.", 'bot');
    console.error('Error:', error);
  }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Auto-resize textarea
messageInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

// Initialize on load
document.addEventListener('DOMContentLoaded', initLanguageContent);