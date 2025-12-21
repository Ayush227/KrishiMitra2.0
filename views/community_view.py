from .shared import get_header, get_navbar

def render_community(posts, current_user):
    
    posts_html = ""
    for post in posts:
        # post: (id, username, content, timestamp)
        # Using the first letter of username as the avatar
        user_initial = post[1][0].upper()
        
        posts_html += f"""
        <div class="post-card">
            <div class="post-header">
                <div class="user-avatar" onclick="openProfile('{post[1]}')">
                    {user_initial}
                </div>
                <div>
                    <h3 class="post-user" onclick="openProfile('{post[1]}')">@{post[1]}</h3>
                    <span class="post-time">{post[3]}</span>
                </div>
            </div>
            <div class="post-content">
                {post[2]}
            </div>
            <div class="post-actions">
                <button><i class="far fa-heart"></i> Like</button>
                <button><i class="far fa-comment"></i> Comment</button>
                <button><i class="fas fa-share"></i> Share</button>
            </div>
        </div>
        """

    return f"""
    {get_header("Community Hub")}
    {get_navbar(back_link="/")}

    <style>
        /* 1. GLASSY DARK THEME */
        body {{
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', sans-serif;
            color: white;
            padding-bottom: 50px;
        }}
        
        .feed-container {{
            max-width: 700px;
            margin: 30px auto;
            padding: 0 20px;
        }}

        /* 2. CREATE POST BOX */
        .create-box {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 40px;
            display: flex; gap: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .create-avatar {{
            width: 50px; height: 50px;
            background: linear-gradient(135deg, #198754, #20c997);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 1.2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .create-form {{ flex: 1; }}
        
        textarea {{
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: none; border-radius: 15px;
            padding: 15px; color: white;
            font-size: 1rem; resize: none; outline: none;
            margin-bottom: 10px; transition: 0.3s;
        }}
        textarea:focus {{ background: rgba(0, 0, 0, 0.4); }}
        
        .post-btn {{
            background: #198754; color: white; border: none;
            padding: 10px 25px; border-radius: 50px;
            font-weight: bold; cursor: pointer; float: right;
            transition: 0.3s;
        }}
        .post-btn:hover {{ transform: translateY(-2px); background: #146c43; }}

        /* 3. POST CARDS */
        .post-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px; margin-bottom: 25px;
        }}
        
        .post-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 15px; }}
        
        .user-avatar {{
            width: 45px; height: 45px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; cursor: pointer;
            border: 2px solid rgba(255,255,255,0.2);
        }}
        .user-avatar:hover {{ border-color: #198754; }}

        .post-user {{ margin: 0; font-size: 1.1rem; cursor: pointer; color: #4ade80; }}
        .post-user:hover {{ text-decoration: underline; }}
        
        .post-time {{ font-size: 0.8rem; opacity: 0.6; }}
        .post-content {{ font-size: 1.05rem; line-height: 1.6; margin-bottom: 20px; color: rgba(255,255,255,0.9); }}
        
        .post-actions {{
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 15px; display: flex; gap: 20px;
        }}
        .post-actions button {{
            background: none; border: none; color: rgba(255,255,255,0.6);
            cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 8px;
        }}
        .post-actions button:hover {{ color: #198754; }}

        /* 4. PROFILE POP-UP MODAL */
        .profile-modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(8px);
            z-index: 1000; display: none;
            justify-content: center; align-items: center;
            opacity: 0; transition: opacity 0.3s;
        }}
        .profile-card {{
            background: linear-gradient(135deg, #1c1c1c 0%, #2a2a2a 100%);
            width: 90%; max-width: 350px;
            border-radius: 25px; padding: 30px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: scale(0.8); transition: transform 0.3s;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }}
        
        .modal-active .profile-modal {{ display: flex; opacity: 1; }}
        .modal-active .profile-card {{ transform: scale(1); }}

        .profile-pic-large {{
            width: 100px; height: 100px;
            background: linear-gradient(135deg, #ff0099, #493240);
            border-radius: 50%; margin: 0 auto 20px auto;
            display: flex; align-items: center; justify-content: center;
            font-size: 3rem; font-weight: bold;
            border: 4px solid rgba(255,255,255,0.1);
        }}
    </style>

    <div id="userModal" class="profile-modal">
        <div class="profile-card">
            <div id="modalPic" class="profile-pic-large">U</div>
            <h2 id="modalName" style="margin:0 0 10px 0;">@Username</h2>
            <p id="modalBio" style="color:rgba(255,255,255,0.7); line-height:1.5;">Loading...</p>
            <div style="margin-top:20px; display:flex; justify-content:center; gap:10px;">
                <button class="post-btn" style="float:none; background:transparent; border:1px solid rgba(255,255,255,0.3);" onclick="closeProfile()">Close</button>
            </div>
        </div>
    </div>

    <div class="feed-container">
        <h1 style="text-align:center; margin-bottom:10px;">Community Feed</h1>
        <p style="text-align:center; opacity:0.7; margin-bottom:30px;">Connect with farmers</p>

        <div class="create-box">
            <div class="create-avatar">{current_user[0].upper()}</div>
            <form class="create-form" method="POST" action="/community">
                <textarea name="content" rows="3" placeholder="Share your farming tips..." required></textarea>
                <button type="submit" class="post-btn"><i class="fas fa-paper-plane"></i> Post</button>
            </form>
        </div>

        <div id="feed">
            {posts_html}
        </div>
    </div>

    <script>
        async function openProfile(username) {{
            const nameEl = document.getElementById('modalName');
            const bioEl = document.getElementById('modalBio');
            const picEl = document.getElementById('modalPic');

            document.body.classList.add('modal-active');
            nameEl.innerText = "@" + username;
            bioEl.innerText = "Fetching details...";
            picEl.innerText = username.charAt(0).toUpperCase();

            try {{
                const res = await fetch('/get_user_profile/' + username);
                const data = await res.json();
                
                if (data.username) {{
                    bioEl.innerText = data.bio;
                }} else {{
                    bioEl.innerText = "User details not found.";
                }}
            }} catch (err) {{
                bioEl.innerText = "Error loading profile.";
            }}
        }}

        function closeProfile() {{
            document.body.classList.remove('modal-active');
        }}

        document.getElementById('userModal').addEventListener('click', function(e) {{
            if (e.target === this) closeProfile();
        }});
    </script>
    </body></html>
    """