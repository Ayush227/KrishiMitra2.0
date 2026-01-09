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
from views import auth_view, community_view, dashboard_view, landing_view, market_view, chat_view, tool_view, calendar_view, guide_view, admin_view, profile_view, equipment_view, labour_view

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
    
    # --- USERS ---
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password_hash TEXT, 
                  bio TEXT, profile_pic TEXT, full_name TEXT, mobile TEXT, village TEXT, 
                  city TEXT, state TEXT, pincode TEXT, role TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, username TEXT, content TEXT, timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, username TEXT, date TEXT, task TEXT, completed INTEGER)''')
    
    # --- TOOLS (Updated with next_available_date) ---
    c.execute('''CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY, username TEXT, tool_name TEXT, desc TEXT, 
        rent_price TEXT, sell_price TEXT, mobile TEXT, address TEXT, image_path TEXT, 
        status TEXT DEFAULT 'Available',
        next_available_date TEXT
    )''')
    
    # --- TOOL REQUESTS ---
    c.execute('''CREATE TABLE IF NOT EXISTS tool_requests (
        id INTEGER PRIMARY KEY, tool_id INTEGER, buyer_username TEXT, req_type TEXT, 
        duration TEXT, message TEXT, contact TEXT, req_status TEXT DEFAULT 'Pending', 
        response_msg TEXT, FOREIGN KEY(tool_id) REFERENCES tools(id)
    )''')
    
    # --- LABOUR ---
    c.execute('''CREATE TABLE IF NOT EXISTS labour_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, work_role TEXT, wages TEXT, 
        worker_limit INTEGER, desc TEXT, location TEXT, timestamp TEXT, status TEXT DEFAULT 'Open'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS labour_applicants (
        id INTEGER PRIMARY KEY AUTOINCREMENT, job_id INTEGER, applicant_username TEXT, 
        fullname TEXT, work_role TEXT, mobile TEXT, address TEXT, photo_path TEXT, timestamp TEXT,
        FOREIGN KEY(job_id) REFERENCES labour_jobs(id)
    )''')
    
    # --- MIGRATIONS (Auto-fix existing DBs) ---
    try: c.execute("ALTER TABLE tools ADD COLUMN status TEXT DEFAULT 'Available'")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE tools ADD COLUMN next_available_date TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE tool_requests ADD COLUMN req_status TEXT DEFAULT 'Pending'")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE tool_requests ADD COLUMN response_msg TEXT")
    except sqlite3.OperationalError: pass

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

@app.route('/profile')
def my_profile():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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
    full_name = request.form.get('full_name', '')
    mobile = request.form.get('mobile', '')
    email = request.form.get('email', '') 
    village = request.form.get('village', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    pincode = request.form.get('pincode', '')
    bio = request.form.get('bio', '')
    role = request.form.get('role', 'Farmer')
    pic = request.form.get('profile_pic', '')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE users SET full_name=?, mobile=?, email=?, village=?, city=?, state=?, pincode=?, bio=?, role=?, profile_pic=? WHERE username=?''', 
              (full_name, mobile, email, village, city, state, pincode, bio, role, pic, session['username']))
    conn.commit()
    conn.close()
    return redirect(url_for('my_profile'))

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

# --- EQUIPMENT HUB ROUTES ---

@app.route('/tools_market')
def tools_market():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Fetch Tools
    c.execute("SELECT * FROM tools ORDER BY id DESC")
    tools = c.fetchall()

    # 2. Fetch Requests
    c.execute("SELECT id, tool_id, buyer_username, req_type, duration, message, contact, req_status FROM tool_requests")
    all_requests = c.fetchall()

    # 3. Check Users Applications
    c.execute("SELECT tool_id, req_status, response_msg FROM tool_requests WHERE buyer_username=?", (session['username'],))
    my_applications = {row[0]: {'status': row[1], 'msg': row[2]} for row in c.fetchall()}

    conn.close()

    requests_data = {}
    for r in all_requests:
        tid = r[1]
        if tid not in requests_data: requests_data[tid] = []
        requests_data[tid].append({
            'id': r[0], 'buyer': r[2], 'type': r[3], 'dur': r[4], 
            'msg': r[5], 'contact': r[6], 'status': r[7]
        })

    return equipment_view.render_tools(tools, session['username'], requests_data, my_applications)

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
    c.execute("INSERT INTO tools (username, tool_name, desc, rent_price, sell_price, mobile, address, image_path, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Available')", 
              (session['username'], name, desc, rent, sell, mobile, address, image_filename))
    conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

@app.route('/submit_tool_interest', methods=['POST'])
def submit_tool_interest():
    if 'username' not in session: return redirect(url_for('home'))
    tool_id = request.form['tool_id']
    req_type = request.form['req_type']
    duration = request.form['duration']
    message = request.form['message']
    contact = request.form['contact']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # --- LOGIC: Check Duplicate Request ---
    c.execute("SELECT id FROM tool_requests WHERE tool_id=? AND buyer_username=? AND req_status='Pending'", 
              (tool_id, session['username']))
    existing = c.fetchone()
    
    if existing:
        conn.close()
        # You could add a flash message here, but for now we redirect back
        return redirect(url_for('tools_market'))

    c.execute("INSERT INTO tool_requests (tool_id, buyer_username, req_type, duration, message, contact, req_status) VALUES (?, ?, ?, ?, ?, ?, 'Pending')",
              (tool_id, session['username'], req_type, duration, message, contact))
    conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

@app.route('/set_tool_status', methods=['POST'])
def set_tool_status():
    if 'username' not in session: return redirect(url_for('home'))
    tool_id = request.form['tool_id']
    new_status = request.form['status'] # 'Available' or 'Rented'
    available_date = request.form.get('next_date', '') # Only if Rented

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verify Owner
    c.execute("SELECT username FROM tools WHERE id=?", (tool_id,))
    tool = c.fetchone()
    if tool and tool[0] == session['username']:
        if new_status == 'Available':
            available_date = '' # Clear date if available
            
        c.execute("UPDATE tools SET status=?, next_available_date=? WHERE id=?", 
                  (new_status, available_date, tool_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for('tools_market'))

@app.route('/withdraw_interest/<int:tool_id>')
def withdraw_interest(tool_id):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tool_requests WHERE tool_id=? AND buyer_username=?", (tool_id, session['username']))
    conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

@app.route('/manage_request', methods=['POST'])
def manage_request():
    if 'username' not in session: return redirect(url_for('home'))
    action = request.form['action'] # 'fulfill' or 'reject'
    req_id = request.form['req_id']
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if action == 'fulfill':
        c.execute("UPDATE tool_requests SET req_status='Fulfilled' WHERE id=?", (req_id,))
        # Do NOT automatically mark tool as Rented here, let owner do it manually with date
        
    elif action == 'reject':
        reason = request.form.get('reason', 'No reason provided.')
        c.execute("UPDATE tool_requests SET req_status='Rejected', response_msg=? WHERE id=?", (reason, req_id))

    conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

@app.route('/delete_tool/<int:tool_id>')
def delete_tool(tool_id):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM tools WHERE id=?", (tool_id,))
    tool = c.fetchone()
    if tool and tool[0] == session['username']:
        c.execute("DELETE FROM tools WHERE id=?", (tool_id,))
        c.execute("DELETE FROM tool_requests WHERE tool_id=?", (tool_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('tools_market'))

# --- LABOUR ROUTES ---
@app.route('/labour_hub')
def labour_hub():
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT j.id, j.username, j.work_role, j.wages, j.worker_limit, j.desc, j.location, j.timestamp,
        (SELECT COUNT(*) FROM labour_applicants WHERE job_id = j.id) as current_count
        FROM labour_jobs j ORDER BY j.id DESC''')
    jobs = c.fetchall()
    conn.close()
    return labour_view.render_labour_hub(jobs, session['username'])

@app.route('/post_job', methods=['POST'])
def post_job():
    if 'username' not in session: return redirect(url_for('home'))
    work_role = request.form['work_role']
    wages = request.form['wages']
    worker_limit = request.form['worker_limit']
    desc = request.form['desc']
    location = request.form['location']
    timestamp = datetime.now().strftime("%d %b %Y")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO labour_jobs (username, work_role, wages, worker_limit, desc, location, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (session['username'], work_role, wages, worker_limit, desc, location, timestamp))
    conn.commit()
    conn.close()
    return redirect(url_for('labour_hub'))

@app.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT worker_limit, username, work_role FROM labour_jobs WHERE id=?", (job_id,))
    job = c.fetchone()
    if not job: conn.close(); return "Job not found"
    limit = job[0]; job_role = job[2]
    c.execute("SELECT id FROM labour_applicants WHERE job_id=? AND applicant_username=?", (job_id, session['username']))
    existing_app = c.fetchone()
    if existing_app: conn.close(); return redirect(url_for('labour_hub'))
    c.execute("SELECT COUNT(*) FROM labour_applicants WHERE job_id=?", (job_id,))
    count = c.fetchone()[0]
    if count >= limit: conn.close(); return "Job is full"
    if request.method == 'GET':
        conn.close()
        return labour_view.render_application_form(job_id, job_role)
    if request.method == 'POST':
        name = request.form['fullname']; role = request.form['work_role']; mobile = request.form['mobile']; address = request.form['address']
        timestamp = datetime.now().strftime("%d %b %Y")
        image_filename = "default_user.png"
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                filename = secure_filename(file.filename); filename = f"worker_{int(datetime.now().timestamp())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)); image_filename = filename
        c.execute('''INSERT INTO labour_applicants (job_id, applicant_username, fullname, work_role, mobile, address, photo_path, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (job_id, session['username'], name, role, mobile, address, image_filename, timestamp))
        conn.commit(); conn.close()
        return redirect(url_for('labour_hub'))

@app.route('/job_details/<int:job_id>')
def job_details(job_id):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM labour_jobs WHERE id=?", (job_id,))
    job = c.fetchone()
    if not job or job[0] != session['username']: conn.close(); return redirect(url_for('labour_hub'))
    c.execute('''SELECT id, fullname, work_role, mobile, address, photo_path, timestamp, applicant_username FROM labour_applicants WHERE job_id = ?''', (job_id,))
    applicants = c.fetchall(); conn.close()
    return labour_view.render_job_details(job_id, applicants)

@app.route('/remove_applicant/<int:app_id>')
def remove_applicant(app_id):
    if 'username' not in session: return redirect(url_for('home'))
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT job_id FROM labour_applicants WHERE id=?", (app_id,))
    app_data = c.fetchone()
    if app_data:
        job_id = app_data[0]
        c.execute("SELECT username FROM labour_jobs WHERE id=?", (job_id,))
        job_owner = c.fetchone()
        if job_owner and job_owner[0] == session['username']:
            c.execute("DELETE FROM labour_applicants WHERE id=?", (app_id,))
            conn.commit(); conn.close()
            return redirect(url_for('job_details', job_id=job_id))
    conn.close(); return redirect(url_for('labour_hub'))

@app.route('/chat')
def chat(): return chat_view.render_chat()

@app.route('/chat_api', methods=['POST'])
def chat_api():
    msg = request.json.get('message', '').lower()
    chatbot_data = load_brain()
    reply = "I didn't understand that."
    for intent in chatbot_data.get('intents', []):
        for pattern in intent['patterns']:
            if pattern in msg: return jsonify({"reply": random.choice(intent['responses'])})
    return jsonify({"reply": reply})

def load_brain():
    try: return json.load(open(JSON_PATH, 'r', encoding='utf-8'))
    except: return {"intents": []}

@app.route('/tool', methods=['GET', 'POST'])
def tool():
    if 'username' not in session: return redirect(url_for('home'))
    result = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            try:
                file = request.files['file']
                image = Image.open(io.BytesIO(file.read()))
                prompt = "Analyze leaf. Identify disease."
                response = model.generate_content([prompt, image])
                result = {"disease": response.text, "image_name": file.filename}
            except: result = {"disease": "Error", "image_name": "Error"}
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
    conn.commit(); conn.close()
    return redirect(url_for('calendar'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit(); conn.close()
    return redirect(url_for('calendar'))

@app.route('/auto_schedule', methods=['POST'])
def auto_schedule():
    crop_name = request.form['crop_name']
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
    schedules = []
    if crop_name == "Wheat": schedules = [(0, "🚜 Sow Wheat"), (120, "🌾 Harvest")]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for days, task in schedules:
        c.execute("INSERT INTO todos (username, date, task, completed) VALUES (?, ?, ?, 0)", (session['username'], (start_date + timedelta(days=days)).strftime("%Y-%m-%d"), task))
    conn.commit(); conn.close()
    return redirect(url_for('calendar'))

@app.route('/guide')
def guide():
    if 'username' not in session: return redirect(url_for('home'))
    return guide_view.render_guide()

if __name__ == '__main__':
    app.run(debug=True, port=5000)