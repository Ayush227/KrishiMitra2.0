from .shared import get_header

def render_login(error="", success=""):
    return f"""
    {get_header("Login | KrishiMitra")}
    
    <style>
        /* ANIMATED BACKGROUND */
        body {{
            margin: 0;
            height: 100vh;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(-45deg, #198754, #0f5132, #20c997, #ffc107);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}

        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* GLASSMORPHISM CARD */
        .glass-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            width: 400px;
            padding: 40px;
            text-align: center;
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.5);
            animation: floatUp 0.8s ease-out;
        }}

        @keyframes floatUp {{
            from {{ transform: translateY(50px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}

        /* INPUT FIELDS WITH GLOW */
        .input-group {{
            margin-bottom: 20px;
            text-align: left;
        }}
        
        .input-group label {{
            font-size: 0.9rem;
            color: #555;
            font-weight: 600;
            margin-bottom: 5px;
            display: block;
        }}

        input {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            outline: none;
            transition: 0.3s;
            font-size: 1rem;
            background: rgba(255,255,255,0.8);
        }}

        input:focus {{
            border-color: #198754;
            box-shadow: 0 0 10px rgba(25, 135, 84, 0.2);
            background: white;
        }}

        /* BUTTONS */
        .btn-main {{
            width: 100%;
            padding: 12px;
            background: linear-gradient(to right, #198754, #146c43);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .btn-main:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(20, 108, 67, 0.3);
        }}

        /* TOGGLE SWITCH (Interactive) */
        .toggle-box {{
            display: flex;
            background: #e9ecef;
            border-radius: 50px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }}

        .toggle-btn {{
            flex: 1;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            font-weight: bold;
            color: #555;
            transition: 0.3s;
            z-index: 2;
        }}

        .toggle-btn.active {{
            color: white;
        }}

        #btn-bg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 50%;
            height: 100%;
            background: #198754;
            border-radius: 50px;
            transition: 0.4s;
            z-index: 1;
        }}

    </style>

    <div class="glass-card">
        <h2 style="color:#198754; margin-bottom: 5px;"><i class="fas fa-leaf"></i> KrishiMitra</h2>
        <p style="color:#777; margin-bottom: 25px; font-size: 0.9rem;">Welcome back, Farmer!</p>

        {f'<div style="background:#f8d7da; color:#842029; padding:10px; border-radius:8px; margin-bottom:15px; font-size:0.9rem;">{error}</div>' if error else ''}
        {f'<div style="background:#d1e7dd; color:#0f5132; padding:10px; border-radius:8px; margin-bottom:15px; font-size:0.9rem;">{success}</div>' if success else ''}

        <div class="toggle-box">
            <div id="btn-bg"></div>
            <div class="toggle-btn active" onclick="showLogin()">Login</div>
            <div class="toggle-btn" onclick="showSignup()">Sign Up</div>
        </div>

        <form id="loginForm" method="POST" action="/login">
            <div class="input-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter your username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn-main">Login Securely</button>
        </form>

        <form id="signupForm" method="POST" action="/signup" style="display:none; animation: fadeIn 0.5s;">
            <div class="input-group">
                <label>Choose Username</label>
                <input type="text" name="username" placeholder="Create a username" required>
            </div>
            <div class="input-group">
                <label>Email Address</label>
                <input type="email" name="email" placeholder="Your email" required>
            </div>
            <div class="input-group">
                <label>Create Password</label>
                <input type="password" name="password" placeholder="Strong password" required>
            </div>
            <button type="submit" class="btn-main" style="background: linear-gradient(to right, #0dcaf0, #0d6efd);">Create Account</button>
        </form>

    </div>

    <script>
        var loginForm = document.getElementById("loginForm");
        var signupForm = document.getElementById("signupForm");
        var btnBg = document.getElementById("btn-bg");
        var btns = document.querySelectorAll(".toggle-btn");

        function showLogin() {{
            loginForm.style.display = "block";
            signupForm.style.display = "none";
            btnBg.style.left = "0";
            btns[0].classList.add("active");
            btns[1].classList.remove("active");
        }}

        function showSignup() {{
            loginForm.style.display = "none";
            signupForm.style.display = "block";
            btnBg.style.left = "50%";
            btns[0].classList.remove("active");
            btns[1].classList.add("active");
        }}
    </script>
    </body></html>
    """