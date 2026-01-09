from .shared import get_header, get_navbar

def render_tools(tools, current_user, requests_data=None, my_applications=None):
    if requests_data is None: requests_data = {}
    if my_applications is None: my_applications = {}

    tools_html = ""
    
    for tool in tools:
        # tool: 0:id, 1:username, 2:name, 3:desc, 4:rent, 5:sell, 6:mobile, 7:addr, 8:img, 9:status, 10:next_available_date
        t_id = tool[0]
        owner = tool[1]
        name = tool[2]
        desc = tool[3]
        rent_p = tool[4]
        sell_p = tool[5]
        mobile = tool[6]
        addr = tool[7]
        img = tool[8]
        status = tool[9] if len(tool) > 9 else "Available" 
        next_date = tool[10] if len(tool) > 10 else ""

        is_owner = (owner == current_user)
        is_rented = (status == "Rented")
        
        my_app_status = my_applications.get(t_id) 
        has_applied = (my_app_status is not None)

        # --- 1. OWNER VIEW ---
        if is_owner:
            req_list = requests_data.get(t_id, [])
            active_reqs = [r for r in req_list if r['status'] != 'Rejected']
            req_count = len(active_reqs)
            
            # Request Rows
            req_rows = ""
            for req in active_reqs:
                row_style = "border-left: 4px solid #10b981;" if req['status'] == 'Fulfilled' else "border-left: 4px solid #3b82f6;"
                status_html = f"<span class='status-tag {req['status'].lower()}'>{req['status']}</span>"
                
                req_rows += f"""
                <div class="req-item" style="{row_style}">
                    <div class="req-header">
                        <strong>@{req['buyer']}</strong> {status_html}
                        <div class="req-actions">
                            <form action="/manage_request" method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="fulfill">
                                <input type="hidden" name="req_id" value="{req['id']}">
                                <button type="submit" class="icon-btn success" title="Mark Fulfilled"><i class="fas fa-check"></i></button>
                            </form>
                            <button onclick="openRejectModal({req['id']}, '{req['buyer']}')" class="icon-btn danger" title="Reject"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                    <div class="req-details"><span class="tag {req['type'].lower()}">{req['type']}</span> <span class="duration">{req['dur']}</span></div>
                    <div class="req-msg">"{req['msg']}"</div>
                    <div class="req-contact"><i class="fas fa-phone"></i> {req['contact']}</div>
                </div>
                """
            if not req_rows: req_rows = "<div class='empty-state'>No active requests.</div>"

            # Owner Status Button logic
            if is_rented:
                status_btn = f"""
                <form action="/set_tool_status" method="POST" style="display:inline;">
                    <input type="hidden" name="tool_id" value="{t_id}">
                    <input type="hidden" name="status" value="Available">
                    <button type="submit" class="toggle-btn available">Mark Available</button>
                </form>"""
            else:
                status_btn = f"""<button onclick="openStatusModal({t_id})" class="toggle-btn rented">Mark Rented</button>"""

            action_section = f"""
            <div class="owner-controls">
                <div class="control-row">
                    {status_btn}
                    <a href="/delete_tool/{t_id}" onclick="return confirm('Permanently delete?')" class="del-link">Delete</a>
                </div>
                {f'<div class="date-info">Back on: {next_date}</div>' if is_rented and next_date else ''}
                <button onclick="openRequestsModal({t_id})" class="manage-btn">Requests ({req_count})</button>
                <div id="req-data-{t_id}" style="display:none;">{req_rows}</div>
            </div>
            """

        # --- 2. BUYER VIEW ---
        else:
            if has_applied:
                app_stat = my_app_status['status']
                app_msg = my_app_status['msg']
                
                if app_stat == 'Rejected':
                    action_section = f"""<div class="rejected-box"><div class="rej-reason">Rejected: "{app_msg}"</div><a href="/withdraw_interest/{t_id}" class="withdraw-btn sm">Dismiss</a></div>"""
                elif app_stat == 'Fulfilled':
                    action_section = f"""<div class="fulfilled-box">Deal Confirmed!<button class="invoice-btn" onclick="printTool('{name}', '{desc}', '{rent_p}', '{sell_p}', '{mobile}', '{addr}', '{owner}', '/static/uploads/{img}')">Invoice</button></div>"""
                else:
                    action_section = f"""<div class="applied-box"><span>Request Pending</span><a href="/withdraw_interest/{t_id}" class="withdraw-btn">Undo Interest</a></div>"""
            
            else:
                # Logic for Fresh Application (Even if Rented)
                if is_rented:
                    # Pop up logic for Rented Item
                    btn_text = "Join Waitlist"
                    # We pass the 'next_date' to the JS function
                    click_action = f"checkRentedAndApply('{t_id}', '{name}', '{next_date}')"
                    btn_class = "action-btn waitlist"
                else:
                    btn_text = "I'm Interested"
                    click_action = f"openInterestModal('{t_id}', '{name}')"
                    btn_class = "action-btn primary"

                action_section = f"""
                <div class="buyer-actions">
                    <button class="{btn_class}" onclick="{click_action}">
                        <i class="fas fa-hand-paper"></i> {btn_text}
                    </button>
                    <button class="action-btn secondary" onclick="printTool('{name}', '{desc}', '{rent_p}', '{sell_p}', '{mobile}', '{addr}', '{owner}', '/static/uploads/{img}')">
                        <i class="fas fa-print"></i>
                    </button>
                </div>
                """

        badge_class = "rented" if is_rented else "available"
        tools_html += f"""
        <div class="inventory-card">
            <div class="card-image">
                <img src="/static/uploads/{img}" onerror="this.src='https://via.placeholder.com/300?text=Item'">
                <div class="status-badge {badge_class}">{status}</div>
                { '<div class="owner-tag">YOU</div>' if is_owner else '' }
            </div>
            <div class="card-details">
                <h3>{name}</h3>
                <div class="price-tag">₹{rent_p}<small>/hr</small></div>
                <p class="desc">{desc}</p>
                <div class="meta-info"><span><i class="fas fa-map-marker-alt"></i> {addr[-15:]}</span><span>@{owner}</span></div>
                <div class="card-footer">{action_section}</div>
            </div>
        </div>
        """

    return f"""
    {get_header("Equipment Hub")}
    {get_navbar(back_link="/")}

    <style>
        :root {{ --primary: #3b82f6; --success: #10b981; --danger: #ef4444; --dark: #0f172a; --card: #1e293b; --text: #e2e8f0; --wait: #f59e0b; }}
        body {{ background-color: var(--dark); font-family: 'Segoe UI', sans-serif; color: var(--text); padding-bottom: 50px; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        .inventory-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .inventory-card {{ background: var(--card); border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); }}
        .card-image {{ height: 180px; position: relative; }}
        .card-image img {{ width: 100%; height: 100%; object-fit: cover; }}
        .status-badge {{ position: absolute; top: 10px; right: 10px; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; color: white; }}
        .status-badge.available {{ background: rgba(16, 185, 129, 0.9); }}
        .status-badge.rented {{ background: rgba(239, 68, 68, 0.9); }}
        .owner-tag {{ position: absolute; top: 10px; left: 10px; background: var(--primary); color: white; padding: 2px 8px; font-size: 0.7rem; border-radius: 4px; font-weight: bold; }}
        
        .card-details {{ padding: 20px; }}
        .price-tag {{ color: var(--success); font-weight: bold; font-size: 1.1rem; }}
        .desc {{ color: #94a3b8; font-size: 0.9rem; margin: 5px 0 15px 0; }}
        .meta-info {{ display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }}
        
        /* Actions */
        .buyer-actions {{ display: grid; grid-template-columns: 1fr auto; gap: 10px; margin-top: 15px; }}
        .action-btn {{ padding: 10px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; color: white; }}
        .action-btn.primary {{ background: rgba(59,130,246,0.2); border: 1px solid var(--primary); }}
        .action-btn.primary:hover {{ background: var(--primary); }}
        .action-btn.waitlist {{ background: rgba(245, 158, 11, 0.2); border: 1px solid var(--wait); color: var(--wait); }}
        .action-btn.waitlist:hover {{ background: var(--wait); color: black; }}
        .action-btn.secondary {{ background: transparent; color: #94a3b8; border: 1px solid #334155; }}
        
        /* Applied States */
        .applied-box {{ background: rgba(59, 130, 246, 0.1); padding: 10px; border-radius: 8px; border: 1px dashed var(--primary); color: var(--primary); font-size: 0.9rem; margin-top: 10px; display: flex; justify-content: space-between; }}
        .withdraw-btn {{ color: var(--danger); font-size: 0.8rem; text-decoration: none; font-weight: bold; }}
        .rejected-box {{ background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 8px; border: 1px solid var(--danger); color: var(--danger); margin-top: 10px; }}
        .fulfilled-box {{ background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 8px; color: var(--success); margin-top: 10px; text-align:center; }}
        .invoice-btn {{ background: transparent; border: 1px solid var(--success); color: var(--success); padding: 5px; border-radius: 4px; cursor: pointer; margin-left: 10px; font-size:0.8rem; }}

        /* Owner Controls */
        .owner-controls {{ background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; margin-top: 10px; }}
        .control-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .toggle-btn {{ border: none; font-size: 0.8rem; font-weight: bold; cursor: pointer; background: transparent; }}
        .toggle-btn.rented {{ color: var(--wait); }}
        .toggle-btn.available {{ color: var(--success); }}
        .del-link {{ color: var(--danger); font-size: 0.8rem; text-decoration: none; }}
        .date-info {{ font-size: 0.8rem; color: #94a3b8; margin-bottom: 5px; font-style: italic; }}
        .manage-btn {{ width: 100%; background: var(--primary); color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; }}

        /* Request Items */
        .req-item {{ background: #0f172a; padding: 10px; margin-bottom: 5px; border-radius: 6px; }}
        .req-header {{ display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px; }}
        .icon-btn {{ width: 25px; height: 25px; border-radius: 50%; border: none; cursor: pointer; color: white; display: inline-flex; justify-content: center; align-items: center; }}
        .icon-btn.success {{ background: var(--success); }} .icon-btn.danger {{ background: var(--danger); }}
        .req-msg {{ font-style: italic; font-size: 0.85rem; color: #cbd5e1; background: rgba(255,255,255,0.05); padding: 5px; border-radius: 4px; }}

        /* Modals */
        .modal-overlay {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 1000; display: none; justify-content: center; align-items: center; backdrop-filter: blur(5px); }}
        .glass-form {{ background: #1e293b; padding: 30px; border-radius: 16px; width: 400px; max-width: 90%; border: 1px solid #334155; position: relative; }}
        .close-icon {{ position: absolute; top: 15px; right: 15px; color: #64748b; cursor: pointer; }}
        input, textarea, select {{ width: 100%; padding: 10px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 8px; margin-top: 5px; }}
        .submit-btn {{ width: 100%; padding: 12px; background: var(--success); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; }}
        .add-btn {{ position:fixed; bottom:30px; right:30px; background:var(--primary); color:white; width:60px; height:60px; border-radius:50%; border:none; box-shadow:0 10px 20px rgba(0,0,0,0.5); font-size:1.5rem; cursor:pointer; display:flex; justify-content:center; align-items:center; z-index:900; }}
    </style>

    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <h1 style="margin:0; background: linear-gradient(to right, #4ade80, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Equipment Hub</h1>
        </div>

        <button class="add-btn" onclick="openModal('addModal')"><i class="fas fa-plus"></i></button>

        <div id="addModal" class="modal-overlay">
            <div class="glass-form">
                <i class="fas fa-times close-icon" onclick="closeModal('addModal')"></i>
                <h2 style="color:white; margin-top:0;">List Item</h2>
                <form action="/add_tool" method="POST" enctype="multipart/form-data">
                    <input type="text" name="tool_name" placeholder="Item Name" required>
                    <input type="file" name="tool_image" required style="margin-top:10px;">
                    <textarea name="desc" rows="2" placeholder="Description" required></textarea>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                        <input type="number" name="rent_price" placeholder="Rent ₹/hr" required>
                        <input type="number" name="sell_price" placeholder="Sell ₹" required>
                    </div>
                    <input type="text" name="mobile" placeholder="Mobile" required>
                    <input type="text" name="address" placeholder="Location" required>
                    <button type="submit" class="submit-btn">Post</button>
                </form>
            </div>
        </div>

        <div id="interestModal" class="modal-overlay">
            <div class="glass-form">
                <i class="fas fa-times close-icon" onclick="closeModal('interestModal')"></i>
                <h2 style="color:white; margin-top:0;">Submit Request</h2>
                <p id="intName" style="color:var(--primary);"></p>
                <form action="/submit_tool_interest" method="POST">
                    <input type="hidden" id="intId" name="tool_id">
                    <select name="req_type"><option value="Rent">Rent</option><option value="Buy">Buy</option></select>
                    <input type="text" name="duration" placeholder="Duration (e.g. 2 days)">
                    <textarea name="message" rows="2" placeholder="Message"></textarea>
                    <input type="text" name="contact" placeholder="My Mobile Number" required>
                    <button type="submit" class="submit-btn">Send</button>
                </form>
            </div>
        </div>

        <div id="statusModal" class="modal-overlay">
            <div class="glass-form" style="width:300px;">
                <i class="fas fa-times close-icon" onclick="closeModal('statusModal')"></i>
                <h3 style="color:white; margin-top:0;">Mark as Rented</h3>
                <form action="/set_tool_status" method="POST">
                    <input type="hidden" id="statToolId" name="tool_id">
                    <input type="hidden" name="status" value="Rented">
                    <label style="color:#94a3b8; font-size:0.9rem;">Available again on:</label>
                    <input type="date" name="next_date" required>
                    <button type="submit" class="submit-btn" style="background:var(--wait); color:black;">Confirm Rented</button>
                </form>
            </div>
        </div>

        <div id="rejectModal" class="modal-overlay">
            <div class="glass-form" style="width:350px;">
                <i class="fas fa-times close-icon" onclick="closeModal('rejectModal')"></i>
                <h3 style="color:var(--danger); margin-top:0;">Reject Request</h3>
                <form action="/manage_request" method="POST">
                    <input type="hidden" name="action" value="reject">
                    <input type="hidden" id="rejId" name="req_id">
                    <textarea name="reason" rows="3" placeholder="Reason for rejection..." required></textarea>
                    <button type="submit" class="submit-btn" style="background:var(--danger);">Reject</button>
                </form>
            </div>
        </div>

        <div id="requestsModal" class="modal-overlay">
            <div class="glass-form">
                <i class="fas fa-times close-icon" onclick="closeModal('requestsModal')"></i>
                <h3 style="color:white; margin-top:0;">Requests</h3>
                <div id="reqContent" style="max-height:400px; overflow-y:auto;"></div>
            </div>
        </div>

        <div class="inventory-grid">{tools_html}</div>
    </div>

    <script>
        function openModal(id) {{ document.getElementById(id).style.display = 'flex'; }}
        function closeModal(id) {{ document.getElementById(id).style.display = 'none'; }}
        
        function openInterestModal(id, name) {{
            openModal('interestModal');
            document.getElementById('intId').value = id;
            document.getElementById('intName').innerText = name;
        }}

        // --- NEW LOGIC: Check Rented Status and Alert ---
        function checkRentedAndApply(id, name, date) {{
            let msg = "This item is currently rented.";
            if (date) {{ msg += "\\nIt will be available after: " + date; }}
            msg += "\\n\\nClick OK to join the waitlist / apply for the next slot.";
            
            if (confirm(msg)) {{
                openInterestModal(id, name);
            }}
        }}

        function openStatusModal(id) {{
            openModal('statusModal');
            document.getElementById('statToolId').value = id;
        }}

        function openRequestsModal(tid) {{
            const content = document.getElementById('req-data-' + tid).innerHTML;
            document.getElementById('reqContent').innerHTML = content;
            openModal('requestsModal');
        }}

        function openRejectModal(rid, user) {{
            closeModal('requestsModal');
            openModal('rejectModal');
            document.getElementById('rejId').value = rid;
        }}

        // Invoice Printer
        function printTool(name, desc, rent, sell, mobile, addr, owner, img) {{
            const win = window.open('', '', 'height=800,width=800');
            const d = new Date().toLocaleDateString();
            const invNo = 'INV-' + Math.floor(Math.random() * 10000);
            
            win.document.write(`<html><head><title>Invoice</title><style>body{{font-family:sans-serif;padding:40px;}}.box{{border:1px solid #eee;padding:20px;margin-bottom:20px;}}</style></head><body>
            <div class="box">
                <h2 style="color:#2ecc71;">KRISHIMITRA INVOICE</h2>
                <p><strong>Invoice #:</strong> ${{invNo}} | <strong>Date:</strong> ${{d}}</p>
                <hr>
                <div style="display:flex;justify-content:space-between;">
                    <div><strong>Vendor:</strong><br>${{owner.toUpperCase()}}<br>${{mobile}}</div>
                    <div><strong>Item:</strong><br>${{name}}<br>${{desc}}</div>
                </div>
                <hr>
                <p style="text-align:right;font-size:1.2rem;"><strong>Rates:</strong> Rent ₹${{rent}}/hr | Buy ₹${{sell}}</p>
                <center style="margin-top:50px;color:#ccc;">Authorized by KrishiMitra Platform</center>
            </div></body></html>`);
            setTimeout(() => {{ win.print(); win.close(); }}, 500);
        }}
    </script>
    </body></html>
    """