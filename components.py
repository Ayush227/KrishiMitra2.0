# components.py - THE PYTHON FRONTEND ENGINE

def get_css():
    return """
    <style>
        :root { --primary: #198754; --accent: #ffc107; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f0fdf4; color: #333; }
        nav { background: white; height: 70px; padding: 0 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .card { background: white; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: 0.3s; text-decoration: none; color: #333; border: 1px solid #eee; }
        .card:hover { transform: translateY(-5px); }
        input { padding: 10px; width: 100%; border: 1px solid #ccc; border-radius: 5px; margin: 5px 0; }
        button { padding: 10px 20px; background: var(--primary); color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """

def create_header(title="KrishiMitra"):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {get_css()}
    </head>
    <body>
    """

def create_navbar(username=None):
    links = ""
    if username:
        if username == 'admin':
            links += '<a href="/admin" style="margin-right:15px; font-weight:bold; color:#333;">Admin Panel</a>'
        links += f'<span style="margin-right:15px;">Hello, {username}</span><a href="/logout"><button>Logout</button></a>'
    else:
        links = '<a href="/login"><button>Login</button></a>'
        
    return f"""
    <nav>
        <div style="font-size: 1.5rem; font-weight: 800; color: #198754;"><i class="fas fa-leaf"></i> KrishiMitra</div>
        <div>{links}</div>
    </nav>
    """

def create_card(title, subtitle, icon, link, color):
    """A Python Function to generate a Card UI Component"""
    return f"""
    <a href="{link}" class="card" style="display:block;">
        <div style="font-size: 2.5rem; margin-bottom: 15px; color: {color}"><i class="fas fa-{icon}"></i></div>
        <h3>{title}</h3>
        <p>{subtitle}</p>
    </a>
    """

def login_page(error=""):
    return f"""
    {create_header("Login")}
    <div style="height:100vh; display:flex; justify-content:center; align-items:center; background-image: url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?q=80&w=1920'); background-size: cover;">
        <div style="background:white; padding:40px; border-radius:15px; width:350px; text-align:center;">
            <h2 style="color:#198754; margin-bottom:20px;">Welcome Back</h2>
            <p style="color:red;">{error}</p>
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" style="width:100%; margin-top:10px;">Login</button>
            </form>
            <hr style="margin: 20px 0;">
            <form method="POST" action="/signup">
                <input type="text" name="username" placeholder="New Username" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="New Password" required>
                <button type="submit" style="background:#0d6efd; width:100%; margin-top:10px;">Create Account</button>
            </form>
        </div>
    </div>
    </body></html>
    """

def dashboard_page(username):
    # Generating cards using Python Loop/Functions instead of HTML copy-paste
    cards_html = ""
    tools = [
        ("Mandi Rates", "Live Prices", "chart-line", "/market", "#fd7e14"),
        ("Kisan Bot", "AI Assistant", "robot", "/chat", "#0dcaf0"),
        ("Encyclopedia", "Crop Guide", "book-open", "/guide", "#6f42c1"),
        ("Calendar", "Task Planner", "calendar-alt", "/calendar", "#d63384"),
    ]
    for t in tools:
        cards_html += create_card(t[0], t[1], t[2], t[3], t[4])

    return f"""
    {create_header("Dashboard")}
    {create_navbar(username)}
    <div style="max-width:1100px; margin:40px auto; padding:0 20px;">
        <h2 style="margin-bottom:20px; color:#146c43;">Your Dashboard</h2>
        
        <div class="card" style="background: linear-gradient(120deg, #198754, #20c997); color: white; display:flex; justify-content:space-between; align-items:center; padding:30px; margin-bottom:20px;">
            <div style="text-align:left;">
                <h3><i class="fas fa-map-marker-alt"></i> Local Weather</h3>
                <h1 style="font-size:3rem;">28°C</h1>
                <p>Sunny • Humidity 45%</p>
            </div>
            <i class="fas fa-cloud-sun" style="font-size:4rem; opacity:0.8;"></i>
        </div>

        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:20px;">
            {cards_html}
        </div>
    </div>
    </body></html>
    """

def market_page(rates, date):
    rows = ""
    for item in rates:
        color = "green" if item['trend'] == 'up' else "red"
        rows += f"""
        <tr>
            <td style="padding:15px; border-bottom:1px solid #eee;"><strong>{item['name']}</strong><br><small>{item['variety']}</small></td>
            <td style="padding:15px; border-bottom:1px solid #eee;">{item['mandi']}</td>
            <td style="padding:15px; border-bottom:1px solid #eee;"><strong>₹{item['price']}</strong></td>
            <td style="padding:15px; border-bottom:1px solid #eee; color:{color}; font-weight:bold;">{item['change']}</td>
        </tr>
        """
        
    return f"""
    {create_header("Market Rates")}
    {create_navbar("Farmer")}
    <div style="max-width:1000px; margin:30px auto; padding:20px;">
        <a href="/" style="text-decoration:none; color:#333;">&larr; Back</a>
        <h2 style="color:#198754; margin:20px 0;">Live Mandi Rates <small>({date})</small></h2>
        <table style="width:100%; background:white; border-collapse:collapse; box-shadow:0 5px 15px rgba(0,0,0,0.05); border-radius:10px; overflow:hidden;">
            <tr style="background:#198754; color:white;"><th style="padding:15px; text-align:left;">Crop</th><th style="padding:15px; text-align:left;">Mandi</th><th style="padding:15px; text-align:left;">Price</th><th style="padding:15px; text-align:left;">Trend</th></tr>
            {rows}
        </table>
    </div>
    </body></html>
    """