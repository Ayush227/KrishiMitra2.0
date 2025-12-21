from .shared import get_header

def render_landing():
    # We define specific CSS for the landing page here to keep it isolated
    landing_css = """
    <style>
        /* Hero Section */
        .hero { 
            height: 90vh; 
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?q=80&w=1920'); 
            background-size: cover; 
            background-position: center; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            text-align: center; 
            color: white; 
            border-bottom-left-radius: 50px; 
            border-bottom-right-radius: 50px; 
            margin-bottom: 50px;
        }
        .hero h1 { font-size: 4rem; font-weight: 800; text-shadow: 0 5px 15px rgba(0,0,0,0.3); margin-bottom: 15px; }
        .hero p { font-size: 1.3rem; margin-bottom: 30px; opacity: 0.9; max-width: 700px; margin-left: auto; margin-right: auto; }
        
        /* Buttons */
        .btn-cta { 
            padding: 15px 45px; 
            background: linear-gradient(45deg, #ffc107, #fd7e14); 
            color: white; 
            font-weight: bold; 
            font-size: 1.1rem; 
            border-radius: 50px; 
            display: inline-block; 
            box-shadow: 0 10px 20px rgba(253, 126, 20, 0.3);
            transition: 0.3s;
        }
        .btn-cta:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(253, 126, 20, 0.4); }

        /* Stats Bar */
        .stats-container { display: flex; justify-content: center; gap: 30px; margin-top: -100px; margin-bottom: 80px; position: relative; z-index: 10; padding: 0 20px; }
        .stat-box { background: white; padding: 30px 50px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1); min-width: 200px; }
        .stat-box h3 { color: #198754; font-size: 2.5rem; margin-bottom: 5px; }
        .stat-box p { color: #555; font-weight: 600; text-transform: uppercase; font-size: 0.9rem; }

        /* Feature Grid */
        .section-title { text-align: center; color: #146c43; font-size: 2.5rem; margin-bottom: 50px; font-weight: 700; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; max-width: 1200px; margin: 0 auto 80px auto; padding: 0 20px; }
        .feature-card { background: white; padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: 0.3s; border: 1px solid #f0f0f0; }
        .feature-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .feature-icon { font-size: 3rem; margin-bottom: 25px; color: #198754; background: #e8f5e9; width: 100px; height: 100px; line-height: 100px; border-radius: 50%; display: inline-block; }

        /* Footer */
        footer { background: #2c3e50; color: white; text-align: center; padding: 60px 0; }
        footer a { color: #ffc107; text-decoration: none; }
    </style>
    """

    html_content = f"""
    {get_header("Welcome to KrishiMitra")}
    {landing_css}
    
    <nav style="position: absolute; top: 0; width: 100%; background: transparent; box-shadow: none; padding-top: 20px;">
        <div class="logo" style="color: white; -webkit-text-fill-color: white;">
            <i class="fas fa-leaf"></i> KrishiMitra
        </div>
        <div>
            <a href="/login" style="color: white; font-weight: 600; margin-right: 20px; text-shadow: 0 2px 5px rgba(0,0,0,0.5);">Login</a>
            <a href="/login" class="btn-cta" style="padding: 10px 25px; font-size: 1rem;">Sign Up</a>
        </div>
    </nav>

    <div class="hero">
        <div>
            <h1>The Future of <span style="color: #ffc107;">Smart Farming</span></h1>
            <p>Empowering farmers with AI-driven insights, real-time market rates, and expert disease detection. Join the digital agriculture revolution today.</p>
            <a href="/login" class="btn-cta">Get Started Free</a>
        </div>
    </div>

    <div class="stats-container">
        <div class="stat-box"><h3>15k+</h3><p>Active Farmers</p></div>
        <div class="stat-box"><h3>98%</h3><p>AI Accuracy</p></div>
        <div class="stat-box"><h3>500+</h3><p>Mandis Tracked</p></div>
    </div>

    <h2 class="section-title">Why Choose KrishiMitra?</h2>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-robot"></i></div>
            <h3>AI Kisan Assistant</h3>
            <p>Have a question? Our intelligent chatbot is available 24/7 to answer queries about sowing, weather, and government schemes.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
            <h3>Live Market Rates</h3>
            <p>Stay ahead of the market. Get real-time price updates from Mandis across India to ensure you sell at the best price.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="fas fa-camera"></i></div>
            <h3>Disease Doctor</h3>
            <p>Spot crop diseases early. Simply upload a photo of an infected leaf, and our AI will suggest instant remedies.</p>
        </div>
    </div>

    <footer>
        <h2 style="margin-bottom: 20px;">Ready to grow better?</h2>
        <a href="/login" class="btn-cta">Join KrishiMitra Now</a>
        <p style="margin-top: 40px; opacity: 0.6;">&copy; 2025 KrishiMitra Project. Designed for Indian Farmers.</p>
    </footer>

    </body>
    </html>
    """
    return html_content