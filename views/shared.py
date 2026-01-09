# views/shared.py

def get_css():
    return """
    <style>
        :root { --primary: #198754; --primary-dark: #146c43; --accent: #ffc107; --gradient: linear-gradient(135deg, #198754 0%, #0f5132 100%); }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: #f0fdf4; color: #333; overflow-x: hidden; }
        a { text-decoration: none; }
        
        /* NAV & HEADER */
        nav { background: white; height: 80px; padding: 0 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 1000; }
        .logo { font-size: 1.8rem; font-weight: 800; background: var(--gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .btn-nav { padding: 10px 25px; background: var(--gradient); color: white !important; border-radius: 50px; box-shadow: 0 4px 10px rgba(25, 135, 84, 0.3); border:none; cursor:pointer;}
        
        /* COMMON CARDS */
        .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .card { background: white; padding: 35px; border-radius: 20px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: 0.3s; border: 1px solid rgba(0,0,0,0.02); display:block; color:#333;}
        .card:hover { transform: translateY(-10px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); }
        .icon { font-size: 2.5rem; margin-bottom: 20px; width: 80px; height: 80px; line-height: 80px; border-radius: 50%; background: #f0fdf4; color: var(--primary); display: inline-block; }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """

def get_header(title="KrishiMitra"):
    return f"""<!DOCTYPE html><html lang="en"><head><title>{title}</title><meta name="viewport" content="width=device-width, initial-scale=1.0">{get_css()}</head><body>"""

def get_navbar(user=None, back_link=None):
    if back_link:
        left_side = f'<div class="logo"><i class="fas fa-leaf"></i> KrishiMitra</div>'
        right_side = f'<a href="{back_link}" style="color:#555; font-weight:600;"><i class="fas fa-arrow-left"></i> Back</a>'
    elif user:
        # Added Profile Link AND Labour Hub Link here
        admin_link = '<a href="/admin" style="margin-right:15px; color:#dc3545; font-weight:bold;">Admin Panel</a>' if user == 'admin' else ''
        
        left_side = f'<div class="logo"><i class="fas fa-leaf"></i> KrishiMitra</div>'
        
        # --- ADDED LABOUR HUB LINK BELOW ---
        right_side = f"""
            <div style="display:flex; align-items:center;">
                {admin_link}
                <a href="/labour_hub" style="margin-right:15px; color:#198754; font-weight:600;">
                    <i class="fas fa-hard-hat"></i> Labour Hub
                </a>
                <a href="/profile" style="margin-right:15px; color:#198754; font-weight:600;">
                    <i class="fas fa-user-circle"></i> My Profile
                </a>
                <a href="/logout" class="btn-nav" style="background:#dc3545; padding: 8px 20px;">Logout</a>
            </div>
        """
    else:
        left_side = f'<div class="logo"><i class="fas fa-leaf"></i> KrishiMitra</div>'
        right_side = f'<a href="/login" class="btn-nav">Login</a>'
        
    return f'<nav>{left_side}{right_side}</nav>'