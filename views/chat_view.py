from .shared import get_header, get_navbar

def render_chat():
    return f"""
    {get_header("Kisan AI")}
    {get_navbar(back_link="/")}
    
    <style>
        /* 1. FUTURISTIC BACKGROUND */
        body {{
            background: radial-gradient(circle at top left, #1a2980 0%, #26d0ce 100%);
            height: 100vh;
            margin: 0;
            overflow: hidden;
            font-family: 'Segoe UI', sans-serif;
        }}
        
        /* Floating Background Particles */
        .particle {{
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: floatUp 20s infinite linear;
            z-index: -1;
        }}
        @keyframes floatUp {{ from {{ transform: translateY(100vh) scale(0); opacity:0; }} to {{ transform: translateY(-100px) scale(1); opacity:0.5; }} }}

        /* 2. GLASS CHAT CONTAINER */
        .chat-container {{
            width: 90%;
            max-width: 900px;
            height: 85vh;
            margin: 20px auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: zoomIn 0.5s ease-out;
        }}
        @keyframes zoomIn {{ from {{ transform: scale(0.95); opacity:0; }} to {{ transform: scale(1); opacity:1; }} }}

        /* 3. HEADER */
        .chat-header {{
            background: rgba(0, 0, 0, 0.2);
            padding: 15px 25px;
            display: flex; align-items: center; gap: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
        }}
        .bot-icon-box {{
            width: 50px; height: 50px;
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(0, 198, 255, 0.7); }} 70% {{ box-shadow: 0 0 0 10px rgba(0, 198, 255, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(0, 198, 255, 0); }} }}

        /* 4. CHAT BODY */
        .chat-body {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex; flex-direction: column; gap: 15px;
        }}
        
        /* 5. GLASS MESSAGES */
        .msg {{
            max-width: 80%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 1rem;
            line-height: 1.5;
            position: relative;
            color: white;
            backdrop-filter: blur(5px);
            animation: slideUp 0.3s ease-out;
        }}
        @keyframes slideUp {{ from {{ transform: translateY(20px); opacity:0; }} to {{ transform: translateY(0); opacity:1; }} }}

        .bot-msg {{
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom-left-radius: 2px;
        }}
        
        .user-msg {{
            align-self: flex-end;
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            box-shadow: 0 5px 15px rgba(0, 114, 255, 0.3);
            border-bottom-right-radius: 2px;
            text-align: right;
        }}

        /* 6. TYPING DOTS */
        .typing {{
            display: none;
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 15px;
            border-radius: 20px;
            gap: 5px;
        }}
        .dot {{ width: 8px; height: 8px; background: white; border-radius: 50%; animation: bounce 1.4s infinite; }}
        .dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .dot:nth-child(3) {{ animation-delay: 0.4s; }}
        @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}

        /* 7. INPUT AREA */
        .input-area {{
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            display: flex; align-items: center; gap: 10px;
        }}
        
        input {{
            flex: 1;
            padding: 15px 25px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1rem;
            outline: none;
            transition: 0.3s;
        }}
        input::placeholder {{ color: rgba(255, 255, 255, 0.6); }}
        input:focus {{ background: rgba(255, 255, 255, 0.2); border-color: rgba(255, 255, 255, 0.5); }}

        .send-btn {{
            width: 50px; height: 50px;
            border-radius: 50%;
            border: none;
            background: white;
            color: #0072ff;
            font-size: 1.2rem;
            cursor: pointer;
            transition: 0.3s;
            display: flex; align-items: center; justify-content: center;
        }}
        .send-btn:hover {{ transform: rotate(45deg) scale(1.1); box-shadow: 0 0 20px rgba(255, 255, 255, 0.5); }}

        /* 8. QUICK CHIPS */
        .chips {{
            display: flex; gap: 10px; padding: 10px 20px;
            overflow-x: auto;
            scrollbar-width: none;
        }}
        .chip {{
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.85rem;
            cursor: pointer;
            white-space: nowrap;
            transition: 0.3s;
        }}
        .chip:hover {{ background: white; color: #0072ff; }}

    </style>

    <div class="particle" style="width: 100px; height: 100px; left: 10%; animation-duration: 25s;"></div>
    <div class="particle" style="width: 200px; height: 200px; left: 70%; animation-duration: 35s;"></div>
    <div class="particle" style="width: 50px; height: 50px; left: 40%; animation-duration: 15s;"></div>

    <div class="chat-container">
        <div class="chat-header">
            <div class="bot-icon-box"><i class="fas fa-robot"></i></div>
            <div>
                <h3 style="margin:0;">Kisan AI 2.0</h3>
                <span style="font-size:0.8rem; opacity:0.8; color:#00ffa3;">● Online & Ready</span>
            </div>
        </div>
        
        <div class="chat-body" id="chatBox">
            <div class="msg bot-msg">Namaste! 🙏 I am your smart farming assistant. Ask me about Apples, Tractors, or Weather.</div>
        </div>

        <div class="chat-body" style="padding:0 20px; flex:none; min-height:0;">
            <div class="typing" id="typingIndicator">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>

        <div class="chips">
            <div class="chip" onclick="fill('Apple Price')">🍎 Apple Rate</div>
            <div class="chip" onclick="fill('Tomato Disease')">🍅 Tomato Care</div>
            <div class="chip" onclick="fill('Tractor Price')">🚜 Tractor</div>
            <div class="chip" onclick="fill('Weather Today')">☁️ Weather</div>
            <div class="chip" onclick="fill('PM Kisan Scheme')">🏛️ Schemes</div>
        </div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ask anything..." onkeypress="if(event.key==='Enter') sendMsg()">
            <button class="send-btn" onclick="sendMsg()"><i class="fas fa-paper-plane"></i></button>
        </div>
    </div>

    <script>
        function fill(text) {{
            let input = document.getElementById("userInput");
            input.value = text;
            sendMsg();
        }}

        async function sendMsg() {{
            let input = document.getElementById("userInput");
            let text = input.value.trim();
            if(!text) return;
            
            let box = document.getElementById("chatBox");
            let typing = document.getElementById("typingIndicator");

            // User Msg
            box.innerHTML += `<div class="msg user-msg">${{text}}</div>`;
            input.value = "";
            box.scrollTop = box.scrollHeight;

            // Typing Animation
            typing.style.display = "flex";
            box.scrollTop = box.scrollHeight;

            // Fetch
            try {{
                let response = await fetch('/chat_api', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{message: text}})
                }});
                let data = await response.json();
                
                setTimeout(() => {{
                    typing.style.display = "none";
                    box.innerHTML += `<div class="msg bot-msg">${{data.reply}}</div>`;
                    box.scrollTop = box.scrollHeight;
                }}, 600); 

            }} catch(e) {{
                typing.style.display = "none";
                box.innerHTML += `<div class="msg bot-msg" style="color:#ff4d4d">Connection Error.</div>`;
            }}
        }}
    </script>
    </body></html>
    """