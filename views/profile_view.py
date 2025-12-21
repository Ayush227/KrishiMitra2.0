from .shared import get_header, get_navbar

def render_profile(user_data, is_own_profile, current_user):
    # user_data = (id, username, email, bio, profile_pic, full_name, mobile, village, city, state, pincode, role)
    
    # Handle missing data
    full_name = user_data[5] if user_data[5] else "Farmer Name"
    mobile = user_data[6] if user_data[6] else "Not set"
    email = user_data[2] if user_data[2] else "Not set"
    village = user_data[7] if user_data[7] else "Not set"
    city = user_data[8] if user_data[8] else "Not set"
    state = user_data[9] if user_data[9] else "Not set"
    pincode = user_data[10] if user_data[10] else "Not set"
    role = user_data[11] if user_data[11] else "Farmer"
    
    profile_pic = user_data[4] if user_data[4] else "https://cdn-icons-png.flaticon.com/512/847/847969.png"
    bio = user_data[3] if user_data[3] else "No bio added yet."

    edit_section = ""
    if is_own_profile:
        edit_section = f"""
        <div style="text-align:center; margin-top:30px;">
            <button onclick="toggleEdit()" class="edit-btn">
                <i class="fas fa-user-edit"></i> Edit Profile
            </button>
        </div>

        <div id="editModal" class="modal-overlay">
            <div class="modal-box">
                <div class="modal-header">
                    <h2>Edit Profile</h2>
                    <i class="fas fa-times close-icon" onclick="toggleEdit()"></i>
                </div>
                
                <form action="/update_profile" method="POST" onsubmit="return validateProfile()">
                    
                    <div class="form-section">
                        <label>1. Full Name</label>
                        <input type="text" name="full_name" value="{user_data[5] if user_data[5] else ''}" placeholder="Enter Full Name" required>
                    </div>

                    <div class="grid-2">
                        <div class="form-section">
                            <label>2. Mobile (10 Digits)</label>
                            <input type="text" id="mobileInput" name="mobile" value="{user_data[6] if user_data[6] else ''}" placeholder="xxxxxxxxxx" maxlength="10" required>
                            <small id="mobileError" class="error-text">Must be exactly 10 digits</small>
                        </div>
                        <div class="form-section">
                            <label>3. Email (Optional)</label>
                            <input type="email" name="email" value="{user_data[2]}" placeholder="example@email.com">
                        </div>
                    </div>

                    <div class="grid-2">
                         <div class="form-section">
                            <label>4. Village</label>
                            <input type="text" name="village" value="{user_data[7] if user_data[7] else ''}" placeholder="Village Name" required>
                        </div>
                        <div class="form-section">
                            <label>5. City</label>
                            <input type="text" name="city" value="{user_data[8] if user_data[8] else ''}" placeholder="City Name" required>
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="form-section">
                            <label>6. State</label>
                            <input type="text" name="state" value="{user_data[9] if user_data[9] else ''}" placeholder="State" required>
                        </div>
                        <div class="form-section">
                            <label>7. Pincode</label>
                            <input type="text" name="pincode" value="{user_data[10] if user_data[10] else ''}" placeholder="6-digit PIN" required>
                        </div>
                    </div>

                    <div class="form-section">
                        <label>8. Bio</label>
                        <textarea name="bio" rows="2" placeholder="Tell us about your farm...">{user_data[3]}</textarea>
                    </div>

                    <div class="form-section">
                        <label>9. Role</label>
                        <select name="role">
                            <option value="Farmer" {'selected' if role == 'Farmer' else ''}>Farmer (Kisan)</option>
                            <option value="Seller" {'selected' if role == 'Seller' else ''}>Seller (Dukandaar)</option>
                            <option value="Buyer" {'selected' if role == 'Buyer' else ''}>Buyer (Vyapari)</option>
                            <option value="Expert" {'selected' if role == 'Expert' else ''}>Expert (Krishi Vigyani)</option>
                        </select>
                    </div>

                    <div class="form-section">
                        <label>Profile Picture URL</label>
                        <input type="text" name="profile_pic" value="{user_data[4]}" placeholder="Image Link (Optional)">
                    </div>

                    <button type="submit" class="save-btn">Save Changes</button>
                </form>
            </div>
        </div>
        """

    return f"""
    {get_header("My Profile")}
    {get_navbar(back_link="/")}

    <style>
        /* 1. VIBRANT BACKGROUND */
        body {{
            background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', sans-serif;
            color: #333;
        }}
        
        .container {{ max-width: 850px; margin: 40px auto; padding: 0 20px; }}
        
        /* 2. MAIN CARD */
        .profile-card {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.8);
        }}

        /* Header Accent */
        .profile-header-bg {{
            position: absolute; top: 0; left: 0; width: 100%; height: 150px;
            background: linear-gradient(135deg, #00b09b, #96c93d);
            opacity: 0.9;
        }}

        .profile-content {{ position: relative; z-index: 2; margin-top: 40px; }}

        /* 3. AVATAR & BADGE */
        .img-container {{
            position: relative; width: 160px; height: 160px; margin: 0 auto 20px auto;
        }}
        .profile-img {{
            width: 100%; height: 100%;
            border-radius: 50%;
            border: 6px solid white;
            object-fit: cover;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            transition: transform 0.5s ease;
        }}
        .profile-img:hover {{ transform: scale(1.05) rotate(5deg); }}

        .role-badge {{
            position: absolute; bottom: 5px; right: 5px;
            background: #ff9f43; color: white;
            padding: 6px 15px; border-radius: 20px;
            font-size: 0.85rem; font-weight: bold;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            text-transform: uppercase; letter-spacing: 1px;
            animation: bounceIn 0.8s;
        }}
        @keyframes bounceIn {{ 0% {{transform: scale(0);}} 80% {{transform: scale(1.2);}} 100% {{transform: scale(1);}} }}

        /* 4. TEXT STYLES */
        h1 {{ margin: 0; font-size: 2.2rem; font-weight: 800; color: #2d3436; }}
        .username {{ color: #00b09b; font-weight: 600; font-size: 1.1rem; margin-bottom: 15px; display:block; }}
        .bio {{ 
            font-style: italic; color: #636e72; max-width: 600px; margin: 0 auto 40px auto; 
            background: rgba(0,0,0,0.03); padding: 15px; border-radius: 15px;
        }}

        /* 5. INTERACTIVE DETAILS GRID */
        .details-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; text-align: left;
        }}

        .detail-card {{
            background: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: all 0.3s ease; border-left: 5px solid #00b09b;
        }}
        .detail-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }}

        .d-label {{ font-size: 0.75rem; color: #b2bec3; text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 5px; }}
        .d-value {{ font-size: 1.05rem; font-weight: 600; color: #2d3436; display: flex; align-items: center; gap: 10px; }}
        .d-icon {{ color: #00b09b; font-size: 1.2rem; }}

        /* 6. BUTTONS */
        .edit-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; padding: 14px 40px;
            border-radius: 50px; font-weight: bold; font-size: 1rem;
            cursor: pointer; transition: 0.3s;
            box-shadow: 0 10px 20px rgba(118, 75, 162, 0.3);
        }}
        .edit-btn:hover {{ transform: scale(1.05); box-shadow: 0 15px 30px rgba(118, 75, 162, 0.5); }}

        /* 7. MODAL STYLING */
        .modal-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);
            z-index: 1000; display: none; justify-content: center; align-items: center;
            animation: fadeIn 0.3s;
        }}
        @keyframes fadeIn {{ from {{opacity:0;}} to {{opacity:1;}} }}

        .modal-box {{
            background: white; width: 600px; max-width: 90%;
            border-radius: 20px; padding: 30px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.25);
            max-height: 90vh; overflow-y: auto;
        }}
        .modal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .close-icon {{ font-size: 1.5rem; color: #ff7675; cursor: pointer; transition: 0.2s; }}
        .close-icon:hover {{ transform: rotate(90deg); }}

        /* FORM ELEMENTS */
        .form-section {{ margin-bottom: 20px; }}
        label {{ display: block; font-weight: 600; color: #636e72; margin-bottom: 8px; font-size: 0.9rem; }}
        input, select, textarea {{
            width: 100%; padding: 12px; border: 2px solid #dfe6e9;
            border-radius: 10px; font-size: 1rem; color: #2d3436; transition: 0.3s;
        }}
        input:focus, select:focus, textarea:focus {{ border-color: #00b09b; outline: none; }}
        
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        
        .error-text {{ color: #e17055; font-size: 0.8rem; margin-top: 5px; display: none; font-weight: bold; }}

        .save-btn {{
            width: 100%; padding: 15px; background: #00b09b; color: white;
            border: none; border-radius: 10px; font-weight: bold; font-size: 1.1rem;
            cursor: pointer; margin-top: 10px; transition: 0.3s;
        }}
        .save-btn:hover {{ background: #009985; }}

        /* Responsive */
        @media (max-width: 600px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
            .details-grid {{ grid-template-columns: 1fr; }}
            .profile-card {{ padding: 20px; }}
        }}
    </style>

    <div class="container">
        
        <div class="profile-card">
            <div class="profile-header-bg"></div>
            
            <div class="profile-content">
                <div class="img-container">
                    <img src="{profile_pic}" class="profile-img" onerror="this.src='https://via.placeholder.com/150'">
                    <div class="role-badge">{role}</div>
                </div>
                
                <h1>{full_name}</h1>
                <span class="username">@{user_data[1]}</span>
                
                <div class="bio">
                    <i class="fas fa-quote-left" style="color:#b2bec3; font-size:0.8rem;"></i> 
                    {bio} 
                    <i class="fas fa-quote-right" style="color:#b2bec3; font-size:0.8rem;"></i>
                </div>

                <div class="details-grid">
                    <div class="detail-card">
                        <span class="d-label">Mobile</span>
                        <div class="d-value"><i class="d-icon fas fa-phone-alt"></i> {mobile}</div>
                    </div>
                    <div class="detail-card">
                        <span class="d-label">Email</span>
                        <div class="d-value"><i class="d-icon fas fa-envelope"></i> {email}</div>
                    </div>
                    <div class="detail-card">
                        <span class="d-label">Village</span>
                        <div class="d-value"><i class="d-icon fas fa-home"></i> {village}</div>
                    </div>
                    <div class="detail-card">
                        <span class="d-label">City</span>
                        <div class="d-value"><i class="d-icon fas fa-city"></i> {city}</div>
                    </div>
                    <div class="detail-card">
                        <span class="d-label">State</span>
                        <div class="d-value"><i class="d-icon fas fa-map-marked-alt"></i> {state}</div>
                    </div>
                    <div class="detail-card">
                        <span class="d-label">Pincode</span>
                        <div class="d-value"><i class="d-icon fas fa-thumbtack"></i> {pincode}</div>
                    </div>
                </div>

                {edit_section}
            </div>
        </div>

    </div>

    <script>
        function toggleEdit() {{
            const modal = document.getElementById('editModal');
            modal.style.display = (modal.style.display === 'flex') ? 'none' : 'flex';
        }}

        function validateProfile() {{
            const mobile = document.getElementById('mobileInput').value;
            const mobileError = document.getElementById('mobileError');
            const regex = /^[0-9]{{10}}$/;

            if (!regex.test(mobile)) {{
                mobileError.style.display = 'block';
                return false; // Stop form submission
            }} else {{
                mobileError.style.display = 'none';
                return true; // Allow form submission
            }}
        }}

        // Close modal if clicking outside
        window.onclick = function(event) {{
            const modal = document.getElementById('editModal');
            if (event.target == modal) {{
                modal.style.display = "none";
            }}
        }}
    </script>
    </body></html>
    """