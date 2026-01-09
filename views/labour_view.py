from .shared import get_header, get_navbar
import sqlite3

def render_labour_hub(jobs, current_user):
    # --- HUB LOGIC ---
    # Quick check to see which jobs the user has applied to
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT job_id FROM labour_applicants WHERE applicant_username=?", (current_user,))
    applied_jobs = [row[0] for row in cursor.fetchall()]
    db.close()

    cards_html = ""
    for job in jobs:
        job_id = job[0]; owner = job[1]; role = job[2]; wages = job[3]; limit = job[4]
        desc = job[5]; loc = job[6]; time = job[7]; count = job[8]

        is_owner = (owner == current_user)
        is_full = (count >= limit)
        has_user_applied = (job_id in applied_jobs)
        
        if is_owner:
            action_btn = f'<a href="/job_details/{job_id}" class="action-btn manage-btn"><i class="fas fa-users-cog"></i> Manage ({count}/{limit})</a>'
        elif has_user_applied:
            action_btn = f'<button class="action-btn applied-btn" disabled><i class="fas fa-check-double"></i> Applied</button>'
        elif is_full:
            action_btn = f'<button class="action-btn full-btn" disabled><i class="fas fa-ban"></i> Full ({count}/{limit})</button>'
        else:
            action_btn = f'<a href="/apply_job/{job_id}" class="action-btn apply-btn"><i class="fas fa-user-plus"></i> Apply Now ({count}/{limit})</a>'

        cards_html += f"""
        <div class="job-card">
            <div class="job-header">
                <div class="role-title">{role}</div>
                <div class="wage-tag">₹{wages}</div>
            </div>
            <div class="job-body">
                <div class="job-info">
                    <span><i class="fas fa-user"></i> {owner}</span>
                    <span><i class="fas fa-map-marker-alt"></i> {loc}</span>
                </div>
                <p class="job-desc">{desc}</p>
                <div class="job-meta">
                    <span>{time}</span>
                    <span class="{ 'status-full' if is_full else 'status-open' }">{ '🔴 Full' if is_full else '🟢 Open' }</span>
                </div>
            </div>
            <div class="job-footer">{action_btn}</div>
        </div>
        """

    return f"""
    {get_header("Labour Hub")}
    {get_navbar(back_link="/")}
    <style>
        body {{ background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 30px 20px; }}
        .page-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; }}
        .page-title h1 {{ margin: 0; background: linear-gradient(to right, #fbbf24, #d97706); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .post-btn {{ background: linear-gradient(135deg, #d97706, #b45309); color: white; padding: 12px 25px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; }}
        
        .job-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .job-card {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); border-radius: 15px; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; }}
        .job-header {{ background: rgba(0,0,0,0.2); padding: 15px; display: flex; justify-content: space-between; align-items: center; }}
        .role-title {{ font-size: 1.2rem; font-weight: bold; color: white; }}
        .wage-tag {{ background: #10b981; color: white; padding: 4px 8px; border-radius: 5px; font-weight: bold; font-size: 0.9rem; }}
        .job-body {{ padding: 15px; flex-grow: 1; }}
        .job-info {{ display: flex; gap: 15px; font-size: 0.9rem; color: #94a3b8; margin-bottom: 10px; }}
        .job-desc {{ color: #cbd5e1; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px; }}
        .job-meta {{ display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; }}
        .status-open {{ color: #4ade80; }} .status-full {{ color: #ef4444; }}
        .job-footer {{ padding: 15px; background: rgba(0,0,0,0.2); }}
        
        .action-btn {{ display: block; width: 100%; padding: 10px; text-align: center; border-radius: 8px; text-decoration: none; font-weight: bold; border: none; cursor: pointer; }}
        .apply-btn {{ background: #2563eb; color: white; }}
        .manage-btn {{ background: #475569; color: white; border: 1px solid #64748b; }}
        .full-btn {{ background: #334155; color: #94a3b8; cursor: not-allowed; }}
        .applied-btn {{ background: #059669; color: white; cursor: not-allowed; opacity: 0.8; }}
        
        /* Modal Styles */
        .modal-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: none; justify-content: center; align-items: center; }}
        .glass-form {{ background: #1e293b; padding: 30px; border-radius: 15px; width: 450px; border: 1px solid rgba(255,255,255,0.1); }}
        input, select, textarea {{ width: 100%; padding: 10px; margin-bottom: 15px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 5px; }}
        .close-btn {{ float: right; cursor: pointer; font-size: 1.2rem; }}
    </style>

    <div class="container">
        <div class="page-header">
            <div class="page-title">
                <h1>Labour Hub</h1>
                <p>Hire workers or Find daily wage work</p>
            </div>
            <button class="post-btn" onclick="document.getElementById('jobModal').style.display = 'flex'">
                <i class="fas fa-plus"></i> Post Requirement
            </button>
        </div>
        <div class="job-grid">{cards_html}</div>
    </div>

    <div id="jobModal" class="modal-overlay">
        <div class="glass-form">
            <span class="close-btn" onclick="document.getElementById('jobModal').style.display = 'none'">&times;</span>
            <h2 style="color:white; margin-top:0;">Post Job</h2>
            <form action="/post_job" method="POST">
                <input type="text" name="work_role" placeholder="Work Role (e.g. Harvesting)" required>
                <input type="text" name="wages" placeholder="Wages (e.g. 500/day)" required>
                <input type="number" name="worker_limit" placeholder="Workers Needed (e.g. 5)" required>
                <input type="text" name="location" placeholder="Location" required>
                <textarea name="desc" rows="3" placeholder="Description" required></textarea>
                <button type="submit" class="post-btn" style="width:100%">Post</button>
            </form>
        </div>
    </div>
    """

def render_application_form(job_id, job_role):
    # Same as before
    return f"""
    {get_header("Apply for Job")}
    {get_navbar(back_link="/labour_hub")}
    <style>
        body {{ background-color: #0f172a; color: white; font-family: 'Segoe UI', sans-serif; }}
        .form-container {{ max-width: 500px; margin: 50px auto; background: #1e293b; padding: 40px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }}
        h2 {{ text-align: center; margin-bottom: 30px; color: #fbbf24; }}
        label {{ display: block; margin-bottom: 8px; color: #94a3b8; font-size: 0.9rem; }}
        input {{ width: 100%; padding: 12px; margin-bottom: 20px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px; }}
        .submit-btn {{ width: 100%; padding: 15px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }}
        .error-msg {{ color: #ef4444; font-size: 0.85rem; display: none; margin-top: -15px; margin-bottom: 15px; }}
    </style>

    <div class="form-container">
        <h2>Apply for {job_role}</h2>
        <form action="/apply_job/{job_id}" method="POST" enctype="multipart/form-data" onsubmit="return validateApplication()">
            <label>Full Name</label>
            <input type="text" name="fullname" placeholder="Enter your full name" required>
            <label>Work Role / Skill</label>
            <input type="text" name="work_role" value="{job_role}" required>
            <label>Mobile Number (10 Digits)</label>
            <input type="text" id="mobile" name="mobile" maxlength="10" placeholder="98XXXXXXXX" required>
            <div id="mobileError" class="error-msg">❌ Must be exactly 10 digits</div>
            <label>Current Address</label>
            <input type="text" name="address" placeholder="Village, City..." required>
            <label>Upload Photo (Identity Verification)</label>
            <input type="file" name="photo" accept="image/*" required>
            <button type="submit" class="submit-btn">Submit Application</button>
        </form>
    </div>
    <script>
        function validateApplication() {{
            const mobile = document.getElementById('mobile').value;
            if (!/^[0-9]{{10}}$/.test(mobile)) {{
                document.getElementById('mobileError').style.display = 'block';
                return false;
            }}
            return true;
        }}
    </script>
    """

def render_job_details(job_id, applicants):
    # applicants structure: (id, fullname, work_role, mobile, address, photo_path, timestamp, username)
    
    list_html = ""
    if not applicants:
        list_html = "<div style='text-align:center; padding:40px; color:#64748b;'>No applicants yet.</div>"
    
    for app in applicants:
        app_id, name, role, mobile, addr, photo, time, user = app
        photo_url = f"/static/uploads/{photo}"
        
        # Prepare arguments for JS functions
        js_data = f"'{name}', '{role}', '{mobile}', '{addr}', '{photo_url}', '{time}', '{job_id}'"

        list_html += f"""
        <div class="applicant-row">
            <div class="app-avatar">
                <img src="{photo_url}" onerror="this.src='https://via.placeholder.com/150?text=User'">
            </div>
            
            <div class="app-info">
                <div class="app-name">{name} <span class="app-username">(@{user})</span></div>
                <div class="app-meta">
                    <span><i class="fas fa-briefcase"></i> {role}</span>
                    <span style="color:#4ade80;"><i class="fas fa-phone-alt"></i> {mobile}</span>
                    <span><i class="fas fa-map-pin"></i> {addr}</span>
                </div>
            </div>

            <div class="app-actions">
                <button onclick="generateCV({js_data})" class="btn-icon cv" title="View Profile/CV">
                    <i class="fas fa-file-alt"></i>
                </button>
                <button onclick="generateSlip({js_data})" class="btn-icon invoice" title="Print Hiring Slip">
                    <i class="fas fa-file-invoice-dollar"></i>
                </button>
                <a href="tel:{mobile}" class="btn-icon call" title="Call"><i class="fas fa-phone"></i></a>
                <a href="/remove_applicant/{app_id}" class="btn-icon remove" title="Remove" onclick="return confirm('Remove {name}?')"><i class="fas fa-trash"></i></a>
            </div>
        </div>
        """

    return f"""
    {get_header("Manage Team")}
    {get_navbar(back_link="/labour_hub")}
    <style>
        body {{ background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        
        .header-section {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 30px; }}
        h2 {{ margin: 0; color: #fbbf24; font-size: 1.8rem; }}
        p {{ color: #94a3b8; margin-top: 5px; }}

        .applicant-row {{
            background: #1e293b; border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px; padding: 15px 20px; margin-bottom: 15px;
            display: flex; align-items: center; gap: 20px;
            transition: 0.2s ease;
        }}
        .applicant-row:hover {{ background: #273548; border-color: rgba(255,255,255,0.1); }}

        .app-avatar img {{
            width: 60px; height: 60px; border-radius: 50%; object-fit: cover;
            border: 2px solid #3b82f6; transition: 0.3s;
        }}
        .app-avatar img:hover {{ transform: scale(1.5); box-shadow: 0 5px 15px rgba(0,0,0,0.5); }}

        .app-info {{ flex-grow: 1; }}
        .app-name {{ font-size: 1.1rem; font-weight: bold; color: white; margin-bottom: 5px; }}
        .app-username {{ font-size: 0.9rem; color: #64748b; font-weight: normal; }}
        
        .app-meta {{ display: flex; gap: 15px; font-size: 0.85rem; color: #cbd5e1; flex-wrap: wrap; }}
        .app-meta span {{ display: flex; align-items: center; gap: 6px; }}
        .app-meta i {{ color: #fbbf24; }}

        .app-actions {{ display: flex; gap: 10px; }}
        .btn-icon {{
            width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
            border-radius: 8px; color: white; transition: 0.2s; text-decoration: none; border:none; cursor:pointer; font-size:1rem;
        }}
        .btn-icon.cv {{ background: #3b82f6; }}
        .btn-icon.cv:hover {{ background: #2563eb; }}

        .btn-icon.invoice {{ background: #8b5cf6; }}
        .btn-icon.invoice:hover {{ background: #7c3aed; }}

        .btn-icon.call {{ background: #10b981; }}
        .btn-icon.call:hover {{ background: #059669; }}
        
        .btn-icon.remove {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }}
        .btn-icon.remove:hover {{ background: #ef4444; color: white; }}
        
        @media (max-width: 600px) {{
            .applicant-row {{ flex-direction: column; text-align: center; }}
            .app-meta {{ justify-content: center; }}
            .app-actions {{ width: 100%; justify-content: space-around; margin-top: 10px; }}
        }}
    </style>

    <div class="container">
        <div class="header-section">
            <h2>Applicant Management</h2>
            <p>Review and manage workers registered for Job #{job_id}</p>
        </div>
        
        <div class="applicants-list">
            {list_html}
        </div>
    </div>

    <script>
        // --- 1. GENERATE CV / PROFILE ---
        function generateCV(name, role, mobile, addr, photo, time, jobid) {{
            const win = window.open('', '', 'width=800,height=900');
            const content = `
                <html><head><title>Worker Profile - ` + name + `</title>
                <style>
                    body {{ font-family: 'Helvetica', sans-serif; background: #f8fafc; padding: 40px; }}
                    .cv-card {{ background: white; max-width: 700px; margin: auto; padding: 40px; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: 1px solid #ddd; }}
                    .header {{ display: flex; align-items: center; border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 20px; }}
                    .photo {{ width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #e2e8f0; margin-right: 30px; }}
                    .name-section h1 {{ margin: 0; color: #1e293b; font-size: 2rem; }}
                    .name-section h3 {{ margin: 5px 0 0 0; color: #64748b; font-weight: normal; }}
                    
                    .section-title {{ color: #3b82f6; font-weight: bold; margin-top: 30px; letter-spacing: 1px; font-size: 0.9rem; }}
                    .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px; }}
                    .info-item label {{ display: block; color: #94a3b8; font-size: 0.8rem; }}
                    .info-item div {{ font-size: 1.1rem; color: #334155; font-weight: 500; }}
                    
                    .verification {{ margin-top: 40px; background: #f0fdf4; padding: 15px; border-radius: 8px; color: #15803d; text-align: center; border: 1px dashed #15803d; }}
                    .footer {{ margin-top: 40px; text-align: center; font-size: 0.8rem; color: #cbd5e1; }}
                </style>
                </head><body>
                    <div class="cv-card">
                        <div class="header">
                            <img src="` + photo + `" class="photo">
                            <div class="name-section">
                                <h1>` + name + `</h1>
                                <h3>` + role + `</h3>
                            </div>
                        </div>

                        <div class="section-title">CONTACT INFORMATION</div>
                        <div class="info-grid">
                            <div class="info-item"><label>PHONE</label><div>` + mobile + `</div></div>
                            <div class="info-item"><label>LOCATION</label><div>` + addr + `</div></div>
                            <div class="info-item"><label>APPLIED ON</label><div>` + time + `</div></div>
                            <div class="info-item"><label>JOB ID</label><div>#` + jobid + `</div></div>
                        </div>

                        <div class="verification">
                            ✅ Identity Verified via KrishiMitra Platform
                        </div>

                        <center><button onclick="window.print()" style="margin-top:30px; padding:10px 20px; cursor:pointer;">Print Profile</button></center>
                    </div>
                </body></html>
            `;
            win.document.write(content);
            win.document.close();
        }}

        // --- 2. GENERATE WORK SLIP / INVOICE ---
        function generateSlip(name, role, mobile, addr, photo, time, jobid) {{
            const win = window.open('', '', 'width=800,height=600');
            const date = new Date().toLocaleDateString();
            const content = `
                <html><head><title>Hiring Slip</title>
                <style>
                    body {{ font-family: 'Courier New', monospace; background: #fff; padding: 40px; color: #000; }}
                    .invoice-box {{ border: 2px solid #000; max-width: 700px; margin: auto; padding: 30px; }}
                    .header {{ text-align: center; border-bottom: 2px dashed #000; padding-bottom: 20px; margin-bottom: 20px; }}
                    .row {{ display: flex; justify-content: space-between; margin-bottom: 15px; }}
                    .label {{ font-weight: bold; }}
                    .signature {{ margin-top: 60px; display: flex; justify-content: space-between; }}
                    .sig-line {{ border-top: 1px solid #000; width: 200px; text-align: center; padding-top: 5px; }}
                </style>
                </head><body>
                    <div class="invoice-box">
                        <div class="header">
                            <h1>HIRING SLIP / WORK ORDER</h1>
                            <p>KRISHIMITRA LABOUR HUB</p>
                        </div>

                        <div class="row">
                            <span><span class="label">DATE:</span> ` + date + `</span>
                            <span><span class="label">JOB ID:</span> #` + jobid + `</span>
                        </div>
                        
                        <div style="margin: 30px 0; border: 1px solid #000; padding: 15px;">
                            <div class="row"><span class="label">WORKER NAME:</span> <span>` + name.toUpperCase() + `</span></div>
                            <div class="row"><span class="label">ROLE:</span> <span>` + role.toUpperCase() + `</span></div>
                            <div class="row"><span class="label">CONTACT:</span> <span>` + mobile + `</span></div>
                            <div class="row"><span class="label">LOCATION:</span> <span>` + addr + `</span></div>
                        </div>

                        <div class="row">
                            <span class="label">STATUS:</span>
                            <span>HIRED / APPLIED (Provisional)</span>
                        </div>

                        <div class="signature">
                            <div class="sig-line">Employer Signature</div>
                            <div class="sig-line">Worker Signature</div>
                        </div>
                        
                        <center style="margin-top:40px;">
                            <small>This is a computer generated slip.</small><br>
                            <button onclick="window.print()" style="margin-top:10px;">Print Slip</button>
                        </center>
                    </div>
                </body></html>
            `;
            win.document.write(content);
            win.document.close();
        }}
    </script>
    """