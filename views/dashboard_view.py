from .shared import get_header, get_navbar

def render_dashboard(user):
    return f"""
    {get_header("Dashboard | KrishiMitra")}
    {get_navbar(user=user)}
    
    <style>
        /* 1. GLOBAL BACKGROUND (MESH GRADIENT) */
        body {{
            background-color: #f3f4f6;
            background-image: 
                radial-gradient(at 0% 0%, hsla(150,33%,92%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(28,100%,88%,1) 0, transparent 50%), 
                radial-gradient(at 100% 100%, hsla(190,100%,90%,1) 0, transparent 50%), 
                radial-gradient(at 0% 100%, hsla(260,100%,92%,1) 0, transparent 50%);
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
        }}

        /* 2. LAYOUT GRID */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        /* 3. WEATHER WIDGET (Premium Glass) */
        .weather-widget {{
            grid-column: span 2;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 25px;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 15px 35px rgba(31, 38, 135, 0.15);
            color: #1a5c48;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s;
        }}
        .weather-widget:hover {{ transform: translateY(-5px); }}
        
        .weather-bg {{
            position: absolute;
            top: -20%; right: -10%;
            width: 300px; height: 300px;
            background: linear-gradient(135deg, #198754, #20c997);
            filter: blur(60px);
            border-radius: 50%;
            opacity: 0.3;
            z-index: 0;
        }}

        /* 4. FLIP CARD STYLES */
        .flip-card {{
            background-color: transparent;
            height: 280px;
            perspective: 1000px;
            cursor: pointer;
            text-decoration: none;
        }}

        .flip-card-inner {{
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            transform-style: preserve-3d;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }}

        .flip-card:hover .flip-card-inner {{
            transform: rotateY(180deg);
        }}

        .flip-card-front, .flip-card-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 25px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-sizing: border-box;
        }}

        /* FRONT DESIGN */
        .flip-card-front {{
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        }}

        /* Icon Bubble */
        .icon-bubble {{
            width: 90px;
            height: 90px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            font-size: 2.5rem;
            color: white;
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
            transition: transform 0.3s;
        }}
        .flip-card:hover .icon-bubble {{ transform: scale(1.1); }}

        .card-title {{
            font-size: 1.4rem;
            font-weight: 800;
            color: #444;
            letter-spacing: 0.5px;
            margin: 0;
        }}

        /* BACK DESIGN */
        .flip-card-back {{
            color: white;
            transform: rotateY(180deg);
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .card-desc {{ font-size: 1rem; line-height: 1.6; font-weight: 500; opacity: 0.95; margin-top: 10px; }}

        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .weather-widget {{ grid-column: span 1; flex-direction: column; text-align: center; gap: 20px; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>

    <div class="container">
        <h2 style="color: #198754; margin-bottom: 10px; font-weight: 900; text-transform: uppercase; text-shadow: 0 2px 10px rgba(25,135,84,0.1);">
            Welcome, {user}
        </h2>
        <p style="color: #666; margin-bottom: 30px; font-size: 1.1rem;">Here is your farming overview for today.</p>
        
        <div class="grid">
            
            <div class="weather-widget">
                <div class="weather-bg"></div>
                <div style="position: relative; z-index: 1;">
                    <h3 style="font-weight:700; color:#146c43; margin:0;"><i class="fas fa-map-marker-alt"></i> New Delhi</h3>
                    <h1 style="font-size: 4.5rem; margin: 10px 0; font-weight: 900; background: linear-gradient(to right, #198754, #20c997); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">28°C</h1>
                    <p style="font-size: 1.2rem; color:#555; font-weight:600; margin:0;">Sunny ☀️</p>
                </div>
                <i class="fas fa-cloud-sun" style="font-size: 7rem; color: #ffc107; filter: drop-shadow(0 10px 20px rgba(255,193,7,0.4)); position:relative; z-index:1;"></i>
            </div>

            <a href="/market" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #ff7e00;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #ff9900, #ff5e00);">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h3 class="card-title">Mandi Rates</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #ff7e00, #ff2200);">
                        <h3>📈 Live Market</h3>
                        <p class="card-desc">Real-time price tracking for all major crops across Indian Mandis.</p>
                    </div>
                </div>
            </a>

            <a href="/community" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #6c35de;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #a450ff, #6c35de);">
                            <i class="fas fa-users"></i>
                        </div>
                        <h3 class="card-title">Community</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #8e2de2, #4a00e0);">
                        <h3>👥 Farmer Forum</h3>
                        <p class="card-desc">Ask questions, share advice, and connect with local farmers.</p>
                    </div>
                </div>
            </a>

            <a href="/chat" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #00c6ff;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #00d2ff, #0072ff);">
                            <i class="fas fa-robot"></i>
                        </div>
                        <h3 class="card-title">Kisan Bot</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #00c6ff, #0072ff);">
                        <h3>🤖 AI Assistant</h3>
                        <p class="card-desc">24/7 Expert help on seeds, weather, and government schemes.</p>
                    </div>
                </div>
            </a>

            <a href="/tool" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #ffba00;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #ffba00, #ff0000);">
                            <i class="fas fa-camera"></i>
                        </div>
                        <h3 class="card-title">Crop Doctor</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #fce38a, #f38181);">
                        <h3>📸 Disease Scan</h3>
                        <p class="card-desc">Instantly detect diseases by uploading a photo of your crop.</p>
                    </div>
                </div>
            </a>

            <a href="/calendar" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #ff0080;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #ff5ea5, #ff0080);">
                            <i class="fas fa-calendar-alt"></i>
                        </div>
                        <h3 class="card-title">Calendar</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #ff6a88, #ff99ac);">
                        <h3>📅 Smart Planner</h3>
                        <p class="card-desc">Manage your sowing dates, irrigation schedule, and tasks.</p>
                    </div>
                </div>
            </a>

            <a href="/guide" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #11998e;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #38ef7d, #11998e);">
                            <i class="fas fa-book-open"></i>
                        </div>
                        <h3 class="card-title">Encyclopedia</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #11998e, #38ef7d);">
                        <h3>📚 Knowledge Hub</h3>
                        <p class="card-desc">Complete A-Z guide on crops, soil types, and farming methods.</p>
                    </div>
                </div>
            </a>
            
            <a href="/tools_market" class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front" style="border-bottom: 5px solid #2c3e50;">
                        <div class="icon-bubble" style="background: linear-gradient(135deg, #4b6cb7, #182848);">
                            <i class="fas fa-tractor"></i>
                        </div>
                        <h3 class="card-title">Equipment</h3>
                    </div>
                    <div class="flip-card-back" style="background: linear-gradient(135deg, #4b6cb7, #182848);">
                        <h3>🚜 Tools Market</h3>
                        <p class="card-desc">Rent or buy tractors, sprayers, and tools from nearby farmers.</p>
                    </div>
                </div>
            </a>

           
            <a href="/tools_market" class="flip-card">
                <div class="card" onclick="window.location.href='/labour_hub'">
                     <div class="icon-container" style="background: linear-gradient(135deg, #d97706, #b45309);">
                    <i class="fas fa-hard-hat"></i>
                     </div>
                    <h3>Labour Hub</h3>
                    <p>Hire workers or find daily wage jobs.</p>
                </div>
            </a>        
        </div>
    </div>
    """