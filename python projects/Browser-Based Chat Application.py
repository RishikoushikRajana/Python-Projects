from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Browse Chat Application</title>
<style>
  :root {
    --color-bg: #ffffff;
    --color-text: #6b7280;
    --color-primary: #111111;
    --color-input-bg: #f9fafb;
    --color-card-bg: #fefefe;
    --color-border: #e5e7eb;
    --radius: 0.75rem;
    --shadow-light: 0 1px 3px rgba(0,0,0,0.1);
    --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    background: var(--color-bg);
    color: var(--color-text);
    font-family: var(--font-sans);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    position: sticky;
    top: 0;
    background: var(--color-bg);
    box-shadow: var(--shadow-light);
    z-index: 10;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--color-primary);
    letter-spacing: -0.025em;
  }

  nav ul {
    list-style: none;
    display: flex;
    gap: 1.5rem;
    margin: 0;
    padding: 0;
  }

  nav li {
    font-weight: 600;
    font-size: 1rem;
    color: var(--color-text);
  }

  nav li:hover {
    color: var(--color-primary);
  }

  main {
    flex-grow: 1;
    max-width: 1200px;
    margin: 3rem auto 4rem;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .hero {
    text-align: center;
  }

  .hero h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 0.5rem;
    color: var(--color-primary);
  }

  .hero p {
    font-size: 1.125rem;
    color: var(--color-text);
    max-width: 540px;
    margin: 0 auto;
  }

  .chat-container {
    background: var(--color-card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow-light);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    height: 500px;
    max-height: 70vh;
  }

  .chat-log {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .message {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow-light);
    font-size: 1rem;
    line-height: 1.4;
    word-break: break-word;
  }

  .message.user {
    background: #dbeafe;
    color: #1e40af;
    align-self: flex-end;
    border-bottom-right-radius: 0.25rem;
  }

  .message.bot {
    background: #f3f4f6;
    color: var(--color-primary);
    align-self: flex-start;
    border-bottom-left-radius: 0.25rem;
  }

  form.chat-form {
    display: flex;
    gap: 0.75rem;
  }

  form.chat-form input[type="text"] {
    flex-grow: 1;
    padding: 0.875rem 1rem;
    font-size: 1.125rem;
    border: 1px solid var(--color-border);
    border-radius: var(--radius);
    background: var(--color-input-bg);
    transition: border-color 0.3s ease;
  }

  form.chat-form input[type="text"]:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(17,17,17,0.15);
  }

  form.chat-form button {
    background: var(--color-primary);
    border: none;
    color: white;
    font-weight: 700;
    font-size: 1.125rem;
    padding: 0 1.5rem;
    border-radius: var(--radius);
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }

  form.chat-form button:hover {
    background: #000;
    transform: scale(1.05);
  }

  form.chat-form button:active {
    transform: scale(0.95);
  }

  @media (max-width: 640px) {
    .hero h1 {
      font-size: 2.25rem;
    }

    .chat-container {
      height: 360px;
    }

    .message {
      max-width: 85%;
      font-size: 0.9rem;
    }
  }
</style>
</head>
<body>
<header>
  <div class="nav-container" role="banner">
    <div class="logo" aria-label="Browse Chat Logo">BrowseChat</div>
    <nav role="navigation" aria-label="Primary">
      <ul>
        <li><a href="#" tabindex="">Home</a></li>
        <li><a href="#" tabindex="">Docs</a></li>
        <li><a href="#" tabindex="">About</a></li>
      </ul>
    </nav>
  </div>
</header>

<main>
  <section class="hero" role="region" aria-labelledby="hero-title">
    <h1 id="hero-title">Browse-Based Chat Application</h1>
    <p>Engage in real-time conversations directly from your browser. Simple, lightweight, and elegant chat interface.</p>
  </section>

  <section aria-label="Chat interface" class="chat-container">
    <div class="chat-log" role="log" aria-live="polite" aria-relevant="additions" id="chatLog"></div>
    <form class="chat-form" id="chatForm" aria-label="Send a message">
      <input type="text" id="chatInput" name="chatInput" aria-required="true" autocomplete="off" placeholder="Type your message..." />
      <button type="submit" aria-label="Send message">Send</button>
    </form>
  </section>
</main>

<script>
  (() => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatLog = document.getElementById('chatLog');

    function addMessage(text, sender) {
      const msgDiv = document.createElement('div');
      msgDiv.classList.add('message', sender);
      msgDiv.textContent = text;
      chatLog.appendChild(msgDiv);
      chatLog.scrollTo({ top: chatLog.scrollHeight, behavior: 'smooth' });
    }

    async function botReply(userMessage) {
      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage }),
        });
        if (!response.ok) {
          addMessage('Error: Could not get response from server.', 'bot');
          return;
        }
        const data = await response.json();
        addMessage(data.reply, 'bot');
      } catch (error) {
        addMessage('Network error: ' + error.message, 'bot');
      }
    }

    chatForm.addEventListener('submit', e => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (!message) return;
      addMessage(message, 'user');
      chatInput.value = '';
      botReply(message);
      chatInput.focus();
    });

    addMessage('Welcome to BrowseChat! Type a message to start.', 'bot');
  })();
</script>
</body>
</html>
"""

import datetime
import webbrowser  # You'll need this import if you add web search functionality


def generate_bot_reply(user_message: str) -> str:
    text = user_message.lower()

    # Greetings
    if any(greet in text for greet in ("hello", "hi", "hey", "good morning", "good afternoon", "good evening")):
        now = datetime.datetime.now()
        hour = now.hour
        if 5 <= hour < 12:
            return "Good morning! How can I assist you today?"
        elif 12 <= hour < 18:
            return "Good afternoon! How can I assist you today?"
        else:
            return "Good evening! How can I assist you today?"

    # Help and Capabilities
    if "help" in text or "what can you do" in text or "features" in text:
        return "I can tell you the current time, answer basic questions about myself, and even open websites if you ask me to search for something."

    # Identity
    if "who are you" in text or "your name" in text:
        return "I am a simple chatbot designed to assist you with information and tasks."

    # Time
    if "time" in text:
        return "The current time is " + datetime.datetime.now().strftime("%H:%M:%S") + "."

    # Date
    if "date" in text:
        return "Today's date is " + datetime.datetime.now().strftime("%B %d, %Y") + "."

    # Simple Web Search (requires webbrowser import)
    if "search for" in text or "google" in text:
        search_query = text.replace("search for", "").replace("google", "").strip()
        if search_query:
            # Open the search query in the default web browser
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return f"Opening Google and searching for '{search_query}'."
        else:
            return "What would you like me to search for?"

    # Thanks
    if "thank" in text:
        return "You’re welcome! Feel free to chat anytime."

    # Default fallback
    return "Sorry, I didn't understand that. Can you rephrase or ask something else?"

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    reply = generate_bot_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

