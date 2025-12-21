import os
import sqlite3
import json
import random
import difflib
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image
import io

# --- IMPORT VIEWS ---
from views import auth_view, community_view, dashboard_view, landing_view, market_view, chat_view, tool_view, calendar_view, guide_view, admin_view, profile_view, equipment_view

app = Flask(__name__)
app.secret_key = 'krishimitra_secure_key'

# --- CONFIGURATION ---
genai.configure(api_key="AIzaSyBjyoKI3gyigMLOUWnVZGfhgY72MH2or_w") 
model = genai.GenerativeModel('gemini-flash-latest')

# SETUP PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
JSON_PATH = os.path.join(BASE_DIR, "chatbot_data.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # --- UPDATED USERS TABLE (New: City, Role) ---
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, 
                  username TEXT UNIQUE, 
                  email TEXT, 
                  password_hash TEXT, 
                  bio TEXT, 
                  profile_pic TEXT,
                  full_name TEXT,
                  mobile TEXT,
                  village TEXT,
                  city TEXT,
                  state TEXT,
                  pincode TEXT,
                  role TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, username TEXT, content TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, username TEXT, date TEXT, task TEXT, completed INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tools (id INTEGER PRIMARY KEY, username TEXT, tool_name TEXT, desc TEXT, rent_price TEXT, sell_price TEXT, mobile TEXT, address TEXT, image_path TEXT)''')
    
    # Admin
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_pass = generate_password_hash("admin123")
        c.execute("INSERT INTO users (username, email, password_hash, bio, profile_pic, role) VALUES (?, ?, ?, ?, ?, ?)", 
                  ('admin', 'admin@krishimitra.com', admin_pass, "System Administrator", "https://cdn-icons-png.flaticon.com/512/2942/2942813.png", "Admin"))
    
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---

@app.route('/')
def home():
    if 'username' in session: return dashboard_view.render_dashboard(session['username'])
    return landing_view.render_landing()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect(url_for('home'))
        return auth_view.render_login(error="Invalid Credentials")
    return auth_view.render_login()

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed = generate_password_hash(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Default role is Farmer
        c.execute("INSERT INTO users (username, email, password_hash, bio, profile_pic, role) VALUES (?, ?, ?, ?, ?, ?)", 
                  (username, email, hashed, "", "", "Farmer"))
        conn.commit()
        conn.close()
        return auth_view.render_login(success="Account Created! Login Now.")
    except:
        return auth_view.render_login(error="User already exists.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# --- UPDATED PROFILE ROUTES ---
@app.route('/profile')
def my_profile():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Fetch ALL fields including city and role (indices 9 and 12)
    c.execute("SELECT id, username, email, bio, profile_pic, full_name, mobile, village, city, state, pincode, role FROM users WHERE username=?", (session['username'],))
    user_data = c.fetchone()
    conn.close()
    return profile_view.render_profile(user_data, True, session['username'])

@app.route('/user/<username>')
def view_user(username):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, email, bio, profile_pic, full_name, mobile, village, city, state, pincode, role FROM users WHERE username=?", (username,))
    user_data = c.fetchone()
    conn.close()
    if user_data:
        return profile_view.render_profile(user_data, False, session['username'])
    return "User not found"

@app.route('/get_user_profile/<username>')
def get_user_profile(username):
    if 'username' not in session: return jsonify({'error': 'Unauthorized'}), 401
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, bio, profile_pic FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        bio = user[1] if user[1] else "No bio."
        pic = user[2] if user[2] else ""
        return jsonify({'username': user[0], 'bio': bio, 'pic': pic})
    return jsonify({'error': 'User not found'}), 404

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session: return redirect(url_for('home'))
    
    # Get form data
    full_name = request.form.get('full_name', '')
    mobile = request.form.get('mobile', '')
    email = request.form.get('email', '') # Optional
    village = request.form.get('village', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    pincode = request.form.get('pincode', '')
    bio = request.form.get('bio', '')
    role = request.form.get('role', 'Farmer')
    pic = request.form.get('profile_pic', '')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''UPDATE users SET 
                 full_name=?, mobile=?, email=?, village=?, city=?, state=?, pincode=?, bio=?, role=?, profile_pic=? 
                 WHERE username=?''', 
              (full_name, mobile, email, village, city, state, pincode, bio, role, pic, session['username']))
    
    conn.commit()
    conn.close()
    return redirect(url_for('my_profile'))

# --- ADMIN ROUTES ---
@app.route('/admin')
def admin_panel():
    if session.get('username') != 'admin': return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, email FROM users")
    users = c.fetchall()
    c.execute("SELECT id, username, content, timestamp FROM posts")
    posts = c.fetchall()
    conn.close()
    return admin_view.render_admin(users, posts, session['username'])

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('username') != 'admin': return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# --- MODULES ---
@app.route('/market')
def market():
    if 'username' not in session: return redirect(url_for('home'))
    today = datetime.now().strftime("%d %b, %Y")
    return market_view.render_market(today)

@app.route('/community', methods=['GET', 'POST'])
def community():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        content = request.form['content']
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        c.execute("INSERT INTO posts (username, content, timestamp) VALUES (?, ?, ?)", (session['username'], content, timestamp))
        conn.commit()
        conn.close()
        return redirect(url_for('community'))
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return community_view.render_community(posts, session['username'])

@app.route('/tools_market')
def tools_market():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tools ORDER BY id DESC")
    tools = c.fetchall()
    conn.close()
    return equipment_view.render_tools(tools, session['username'])

@app.route('/add_tool', methods=['POST'])
def add_tool():
    if 'username' not in session: return redirect(url_for('home'))
    name = request.form['tool_name']
    desc = request.form['desc']
    rent = request.form['rent_price']
    sell = request.form['sell_price']
    mobile = request.form['mobile']
    address = request.form['address']
    image_filename = "default_tool.png"
    if 'tool_image' in request.files:
        file = request.files['tool_image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filename = f"{int(datetime.now().timestamp())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tools (username, tool_name, desc, rent_price, sell_price, mobile, address, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
              (session['username'], name, desc, rent, sell, mobile, address, image_filename))
    conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

# --- CHATBOT & AI ---
def load_brain():
    try: return json.load(open(JSON_PATH, 'r', encoding='utf-8'))
    except: return {"intents": []}
chatbot_data = load_brain()

@app.route('/chat')
def chat(): return chat_view.render_chat()

@app.route('/chat_api', methods=['POST'])
def chat_api():
    msg = request.json.get('message', '').lower()
    reply = "I didn't understand that. Try asking about 'Tractors', 'Wheat', or 'Rice'."
    
    all_patterns = []
    pattern_map = {} 
    
    if not chatbot_data.get('intents'):
        return jsonify({"reply": "Error: Brain missing!"})

    for intent in chatbot_data.get('intents', []):
        for pattern in intent['patterns']:
            all_patterns.append(pattern)
            pattern_map[pattern] = intent
            
    # --- ADD THIS LINE HERE (CRITICAL FIX) ---
    # This sorts patterns so "tractor price" (long) is checked BEFORE "price" (short)
    all_patterns.sort(key=len, reverse=True) 
    # ---------------------------------------

    found_intent = None
    for pattern in all_patterns:
        if pattern in msg:
            found_intent = pattern_map[pattern]
            break
    if found_intent: reply = random.choice(found_intent['responses'])
    return jsonify({"reply": reply})

@app.route('/tool', methods=['GET', 'POST'])
def tool():
    if 'username' not in session: return redirect(url_for('home'))
    result = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            try:
                file = request.files['file']
                image = Image.open(io.BytesIO(file.read()))
                prompt = """Analyze leaf. Identify disease. Headers: DIAGNOSIS, CONFIDENCE, SEVERITY, REMEDY."""
                response = model.generate_content([prompt, image])
                text = response.text
                diagnosis="Unknown"; confidence="0%"; severity="Unknown"; remedy="Consult expert."
                for line in text.split('\n'):
                    if "DIAGNOSIS:" in line: diagnosis = line.split(':')[1].strip()
                    if "CONFIDENCE:" in line: confidence = line.split(':')[1].strip()
                    if "SEVERITY:" in line: severity = line.split(':')[1].strip()
                    if "REMEDY:" in line: remedy = line.split(':')[1].strip()
                result = {"disease": diagnosis, "accuracy": confidence, "remedy": remedy, "severity": severity, "image_name": file.filename}
            except Exception as e:
                result = {"disease": "Error", "accuracy": "0%", "remedy": "Check Key", "severity": "Error", "image_name": "Error"}
    return tool_view.render_tool(result)

@app.route('/calendar')
def calendar():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, date, task FROM todos WHERE username=?", (session['username'],))
    tasks = [{"id": row[0], "date": row[1], "title": row[2]} for row in c.fetchall()]
    conn.close()
    return calendar_view.render_calendar(tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO todos (username, date, task, completed) VALUES (?, ?, ?, 0)", (session['username'], request.form['date'], request.form['task']))
    conn.commit()
    conn.close()
    return redirect(url_for('calendar'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('calendar'))

@app.route('/auto_schedule', methods=['POST'])
def auto_schedule():
    crop_name = request.form['crop_name']
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
    schedules = []
    if crop_name == "Wheat": schedules = [(0, "🚜 Sow Wheat"), (21, "💧 1st Irrigation"), (45, "🧪 Apply Urea"), (65, "💧 2nd Irrigation"), (120, "🌾 Harvest")]
    elif crop_name == "Rice": schedules = [(0, "🌱 Sow Paddy"), (25, "🚜 Transplant"), (30, "💧 Maintain Water"), (60, "🧪 Apply Potash"), (110, "🌾 Harvest")]
    elif crop_name == "Cotton": schedules = [(0, "🌱 Sow Cotton"), (30, "✂️ Thinning"), (45, "💧 1st Irrigation"), (90, "🐛 Check Bollworm"), (150, "☁️ Picking")]
    elif crop_name == "Tomato": schedules = [(0, "🌱 Transplant"), (20, "🥢 Staking"), (45, "💧 Irrigation"), (60, "🍅 Harvest")]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for days, task in schedules:
        c.execute("INSERT INTO todos (username, date, task, completed) VALUES (?, ?, ?, 0)", (session['username'], (start_date + timedelta(days=days)).strftime("%Y-%m-%d"), task))
    conn.commit()
    conn.close()
    return redirect(url_for('calendar'))

@app.route('/guide')
def guide():
    if 'username' not in session: return redirect(url_for('home'))
    return guide_view.render_guide()

if __name__ == '__main__':
    app.run(debug=True, port=5000)