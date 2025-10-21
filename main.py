from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Business Assistant</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .chat-box { 
            background: rgba(0,0,0,0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            min-height: 300px;
            max-height: 400px;
            overflow-y: auto;
            text-align: left;
        }
        .message { 
            margin: 10px 0; 
            padding: 10px; 
            border-radius: 8px; 
        }
        .user-message { 
            background: rgba(0,123,255,0.3); 
            margin-left: 20%;
        }
        .ai-message { 
            background: rgba(40,167,69,0.3); 
            margin-right: 20%;
        }
        .controls { 
            display: flex; 
            gap: 10px; 
            margin: 20px 0; 
        }
        input, button { 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
        }
        input { 
            flex: 2; 
            background: white; 
            color: #333; 
        }
        button { 
            background: #007bff; 
            color: white; 
            cursor: pointer; 
            flex: 1;
        }
        .quick-buttons { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }
        .pricing-box {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Business Assistant</h1>
            <p>24/7 Customer Support • Lead Generation • Automated Responses</p>
            <p><em>Built by Sana Nasir - AI Developer</em></p>
        </div>

        <div class="chat-box" id="chatBox">
            <div class="message ai-message">
                <strong>AI:</strong> Welcome! I'm a custom AI assistant that handles customer queries 24/7. 
                Businesses save $500+/month on support costs with assistants like me!
            </div>
        </div>

        <div class="controls">
            <input type="text" id="messageInput" placeholder="Ask about pricing, features, or setup..." required>
            <button onclick="sendMessage()">Send Message</button>
        </div>

        <div class="quick-buttons">
            <button onclick="quickAction('pricing')" style="background: #28a745;">💰 Pricing</button>
            <button onclick="quickAction('features')" style="background: #ffc107; color: black;">✨ Features</button>
            <button onclick="quickAction('time')" style="background: #17a2b8;">⏰ Setup Time</button>
            <button onclick="quickAction('contact')" style="background: #dc3545;">📞 Contact</button>
        </div>

        <div class="pricing-box">
            <h3>💼 Business Package: $99</h3>
            <p>• Custom AI Assistant • 24/7 Operation • Easy Integration • 2-Day Setup • 1 Week Support</p>
            <button onclick="quickAction('order')" style="background: #6f42c1; padding: 15px 30px; font-size: 18px; margin-top: 10px;">
                🚀 Order Now
            </button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const messageInput = document.getElementById('messageInput');

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) {
                alert('Please enter a message!');
                return;
            }

            // Add user message
            chatBox.innerHTML += `<div class="message user-message"><strong>You:</strong> ${message}</div>`;
            messageInput.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'message=' + encodeURIComponent(message)
                });
                
                const data = await response.json();
                
                // Add AI response
                chatBox.innerHTML += `<div class="message ai-message"><strong>AI:</strong> ${data.response}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                chatBox.innerHTML += `<div class="message ai-message" style="background: rgba(220,53,69,0.3);">
                    <strong>Error:</strong> ${error.message}
                </div>`;
            }
        }

        function quickAction(action) {
            const actions = {
                'pricing': 'How much does an AI assistant cost?',
                'features': 'What features are included?',
                'time': 'How long does setup take?',
                'contact': 'I want to contact you for a custom AI assistant',
                'order': 'I want to order an AI assistant for my business'
            };
            messageInput.value = actions[action];
            sendMessage();
        }

        // Enter key support
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Focus input on load
        window.onload = function() {
            messageInput.focus();
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(HTML)

@app.post("/chat")
async def chat(message: str = Form(...)):
    message_lower = message.lower()
    
    # Pricing questions
    if any(word in message_lower for word in ['price', 'cost', 'how much', '$']):
        response = "💰 **AI Assistant Pricing:**\n• Basic Package: $99 (standard features)\n• Premium Package: $199 (advanced features + analytics)\n• Custom Solutions: $299+ (enterprise level)\n\nMost businesses save $500+/month on customer support costs!"
    
    # Feature questions
    elif any(word in message_lower for word in ['feature', 'what include', 'capability', 'what can']):
        response = "✨ **Features Included:**\n• 24/7 Customer Support\n• Lead Generation & Qualification\n• FAQ Automation\n• Multi-language Support\n• Easy Website Integration\n• Custom Training\n• Analytics Dashboard\n• Unlimited Queries"
    
    # Time questions
    elif any(word in message_lower for word in ['time', 'how long', 'setup', 'delivery']):
        response = "⚡ **Setup Timeline:**\n• Basic Setup: 2-3 days\n• Custom Training: 3-5 days\n• Full Integration: 1 week\n\nWe work quickly to understand your business and deploy a tailored solution!"
    
    # Contact/Order questions
    elif any(word in message_lower for word in ['contact', 'order', 'buy', 'purchase', 'hire', 'want']):
        response = "📞 **Ready to get started?**\nContact Sana Nasir for a free consultation!\n\n📧 Email: sana.nasir@example.com\n📱 Phone: +1234567890\n💬 WhatsApp: available\n\nI'll understand your business needs and provide a custom quote within 24 hours!"
    
    # Greeting
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        response = "👋 **Hello!** I'm a demo of the AI assistants built by **Sana Nasir**. I specialize in creating custom AI solutions that save businesses thousands in support costs. How can I help you today?"
    
    # Default response
    else:
        response = f"🤖 I understand you're asking about: '{message}'\n\nI build **custom AI assistants** that:\n• Answer customer questions 24/7\n• Generate qualified leads\n• Reduce support costs by 60%\n• Work across multiple platforms\n\nWould you like to know about **pricing** or **features**?"
    
    return JSONResponse({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)