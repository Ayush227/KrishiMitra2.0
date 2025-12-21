from .shared import get_header, get_navbar

def render_tools(tools, current_user):
    
    tools_html = ""
    for tool in tools:
        # tool data: (id, username, tool_name, desc, rent_price, sell_price, mobile, address, image_path)
        
        # Prepare data for JS
        tool_data = f"'{tool[2]}', '{tool[3]}', '{tool[4]}', '{tool[5]}', '{tool[6]}', '{tool[7]}', '{tool[1]}', '/static/uploads/{tool[8]}'"
        
        tools_html += f"""
        <div class="inventory-card">
            <div class="card-image">
                <img src="/static/uploads/{tool[8]}" onerror="this.src='https://via.placeholder.com/300?text=No+Image'">
                <div class="status-badge">Available</div>
            </div>
            
            <div class="card-details">
                <h3 class="tool-title">{tool[2]}</h3>
                <p class="tool-desc">{tool[3]}</p>
                
                <div class="specs-grid">
                    <div class="spec-item">
                        <span class="label">RENTAL</span>
                        <span class="value rent">₹{tool[4]}</span>
                    </div>
                    <div class="spec-item">
                        <span class="label">BUY NOW</span>
                        <span class="value sell">₹{tool[5]}</span>
                    </div>
                </div>

                <div class="seller-info">
                    <i class="fas fa-user-circle"></i> @{tool[1]} | <i class="fas fa-map-pin"></i> {tool[7][-6:] if len(tool[7]) > 6 else 'Loc'}
                </div>

                <button class="action-btn" onclick="printTool({tool_data})">
                    <i class="fas fa-file-invoice"></i> View Invoice
                </button>
            </div>
        </div>
        """

    return f"""
    {get_header("Inventory Hub")}
    {get_navbar(back_link="/")}

    <style>
        /* 1. DARK INVENTORY THEME */
        body {{
            background-color: #0f172a;
            background-image: 
                linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.9)),
                url('https://www.transparenttextures.com/patterns/cubes.png');
            font-family: 'Segoe UI', sans-serif;
            color: #e2e8f0;
            min-height: 100vh;
        }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}

        /* 2. HEADER SECTION */
        .page-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 20px;
        }}
        .page-title h1 {{ font-size: 2.5rem; margin: 0; background: linear-gradient(to right, #4ade80, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .page-title p {{ color: #94a3b8; margin-top: 5px; }}

        .add-btn {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white; padding: 12px 25px; border-radius: 8px;
            font-weight: 600; border: none; cursor: pointer;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
            transition: all 0.3s ease; display: flex; align-items: center; gap: 10px;
        }}
        .add-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5); }}

        /* 3. GLASS FORM MODAL */
        .modal-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); backdrop-filter: blur(8px);
            z-index: 1000; display: none; justify-content: center; align-items: center;
        }}
        .glass-form {{
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 30px; border-radius: 20px; width: 500px; max-width: 90%;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            animation: slideDown 0.4s ease;
        }}
        @keyframes slideDown {{ from {{ opacity: 0; transform: translateY(-50px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .form-group {{ margin-bottom: 15px; }}
        .form-label {{ display: block; margin-bottom: 8px; color: #94a3b8; font-size: 0.9rem; }}
        
        input, textarea, select {{
            width: 100%; padding: 12px; background: #0f172a; border: 1px solid #334155;
            color: white; border-radius: 8px; outline: none; transition: 0.3s;
        }}
        input:focus {{ border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }}

        .submit-btn {{
            width: 100%; padding: 15px; background: #10b981; color: white;
            border: none; border-radius: 8px; font-weight: bold; cursor: pointer;
            font-size: 1rem; margin-top: 10px;
        }}
        .submit-btn:hover {{ background: #059669; }}
        .close-form {{ position: absolute; top: 20px; right: 20px; cursor: pointer; color: #64748b; font-size: 1.5rem; }}

        /* 4. INVENTORY GRID */
        .inventory-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px;
        }}

        .inventory-card {{
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px; overflow: hidden;
            transition: all 0.3s ease;
            position: relative;
        }}
        .inventory-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            border-color: rgba(59, 130, 246, 0.3);
        }}

        .card-image {{ height: 200px; position: relative; overflow: hidden; }}
        .card-image img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .inventory-card:hover .card-image img {{ transform: scale(1.1); }}
        
        .status-badge {{
            position: absolute; top: 10px; right: 10px;
            background: rgba(16, 185, 129, 0.9); color: white;
            padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;
        }}

        .card-details {{ padding: 20px; }}
        .tool-title {{ margin: 0 0 10px 0; color: white; font-size: 1.25rem; }}
        .tool-desc {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; line-height: 1.5; height: 40px; overflow: hidden; }}

        .specs-grid {{ display: flex; gap: 10px; margin-bottom: 20px; background: #0f172a; padding: 10px; border-radius: 10px; }}
        .spec-item {{ flex: 1; text-align: center; }}
        .spec-item .label {{ display: block; font-size: 0.7rem; color: #64748b; letter-spacing: 1px; }}
        .spec-item .value {{ font-size: 1.1rem; font-weight: bold; }}
        .value.rent {{ color: #3b82f6; }}
        .value.sell {{ color: #10b981; }}

        .seller-info {{ font-size: 0.85rem; color: #64748b; margin-bottom: 15px; display: flex; align-items: center; gap: 5px; }}
        
        .action-btn {{
            width: 100%; padding: 12px; background: rgba(255,255,255,0.05);
            color: white; border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px; cursor: pointer; transition: 0.3s;
            display: flex; align-items: center; justify-content: center; gap: 8px;
        }}
        .action-btn:hover {{ background: #3b82f6; border-color: #3b82f6; }}

        /* Validation Error Message */
        .error-msg {{ color: #ef4444; font-size: 0.85rem; margin-top: 5px; display: none; }}
    </style>

    <div class="container">
        
        <div class="page-header">
            <div class="page-title">
                <h1>Equipment Hub</h1>
                <p>Buy, Rent, or Sell Farming Machinery</p>
            </div>
            <button class="add-btn" onclick="openModal()">
                <i class="fas fa-plus"></i> Add Equipment
            </button>
        </div>

        <div id="modalOverlay" class="modal-overlay">
            <div class="glass-form">
                <i class="fas fa-times close-form" onclick="closeModal()"></i>
                <h2 style="margin-top:0; color:white;">List Item</h2>
                
                <form action="/add_tool" method="POST" enctype="multipart/form-data" onsubmit="return validateForm()">
                    
                    <div class="form-group">
                        <label class="form-label">Equipment Name</label>
                        <input type="text" name="tool_name" placeholder="e.g. John Deere Tractor" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Upload Photo</label>
                        <input type="file" name="tool_image" accept="image/*" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Description</label>
                        <textarea name="desc" rows="2" placeholder="Condition, Year of Purchase..." required></textarea>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                        <div class="form-group">
                            <label class="form-label">Rent Price</label>
                            <input type="number" name="rent_price" placeholder="₹ per hour" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Sell Price</label>
                            <input type="number" name="sell_price" placeholder="₹ Total" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Mobile Number</label>
                        <input type="text" id="mobile" name="mobile" placeholder="10 Digit Mobile No" maxlength="10" required>
                        <div id="mobileError" class="error-msg">❌ Must be exactly 10 digits.</div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Address (with Pincode)</label>
                        <input type="text" id="address" name="address" placeholder="Village, District, PIN: 123456" required>
                        <div id="addressError" class="error-msg">❌ Must include a valid 6-digit Pincode.</div>
                    </div>

                    <button type="submit" class="submit-btn">Post to Marketplace</button>
                </form>
            </div>
        </div>

        <div class="inventory-grid">
            {tools_html}
        </div>
        
    </div>

    <script>
        function openModal() {{
            document.getElementById('modalOverlay').style.display = 'flex';
        }}
        function closeModal() {{
            document.getElementById('modalOverlay').style.display = 'none';
        }}

        // --- VALIDATION LOGIC ---
        function validateForm() {{
            let isValid = true;
            
            // 1. Mobile Validation (Exactly 10 digits)
            const mobile = document.getElementById('mobile').value;
            const mobileRegex = /^[0-9]{{10}}$/;
            const mobileErr = document.getElementById('mobileError');
            
            if (!mobileRegex.test(mobile)) {{
                mobileErr.style.display = 'block';
                isValid = false;
            }} else {{
                mobileErr.style.display = 'none';
            }}

            // 2. Address Validation (Must contain 6 digit PIN)
            const address = document.getElementById('address').value;
            // Regex checks for a 6-digit number occurring anywhere in the address string
            const pinRegex = /[0-9]{{6}}/; 
            const addrErr = document.getElementById('addressError');

            if (!pinRegex.test(address)) {{
                addrErr.style.display = 'block';
                isValid = false;
            }} else {{
                addrErr.style.display = 'none';
            }}

            return isValid; // Form submits only if true
        }}

        // --- PRINT INVOICE LOGIC ---
        function printTool(name, desc, rent, sell, mobile, addr, owner, img) {{
            const printWindow = window.open('', '', 'height=700,width=900');
            const date = new Date().toLocaleDateString();

            printWindow.document.write('<html><head><title>KrishiMitra Invoice</title>');
            printWindow.document.write('<style>');
            printWindow.document.write('body {{ font-family: "Courier New", Courier, monospace; padding: 40px; background:#fff; color:#000; }}');
            printWindow.document.write('.invoice-box {{ border: 2px solid #000; padding: 30px; max-width: 700px; margin: auto; }}');
            printWindow.document.write('h1 {{ text-align: center; border-bottom: 2px dashed #000; padding-bottom: 15px; margin-top: 0; }}');
            printWindow.document.write('.row {{ display: flex; justify-content: space-between; margin-bottom: 10px; }}');
            printWindow.document.write('.box {{ border: 1px solid #000; padding: 15px; margin: 20px 0; }}');
            printWindow.document.write('img {{ max-width: 100%; height: 200px; object-fit: contain; display: block; margin: 0 auto; }}');
            printWindow.document.write('</style>');
            printWindow.document.write('</head><body>');
            
            printWindow.document.write('<div class="invoice-box">');
            printWindow.document.write('<h1>INVOICE / QUOTATION</h1>');
            printWindow.document.write('<div class="row"><span>DATE: ' + date + '</span><span>VENDOR: ' + owner.toUpperCase() + '</span></div>');
            
            printWindow.document.write('<div class="box"><img src="' + img + '"></div>');
            
            printWindow.document.write('<h3>ITEM DETAILS</h3>');
            printWindow.document.write('<div class="row"><span>PRODUCT:</span> <strong>' + name.toUpperCase() + '</strong></div>');
            printWindow.document.write('<div class="row"><span>NOTES:</span> <span>' + desc + '</span></div>');
            
            printWindow.document.write('<div class="box" style="background:#eee;">');
            printWindow.document.write('<div class="row"><span>RENTAL RATE:</span> <strong>₹' + rent + '</strong></div>');
            printWindow.document.write('<div class="row"><span>SELLING PRICE:</span> <strong>₹' + sell + '</strong></div>');
            printWindow.document.write('</div>');

            printWindow.document.write('<h3>CONTACT INFORMATION</h3>');
            printWindow.document.write('<div class="row"><span>PHONE:</span> <strong>' + mobile + '</strong></div>');
            printWindow.document.write('<div class="row"><span>LOCATION:</span> <span>' + addr + '</span></div>');
            
            printWindow.document.write('<center style="margin-top:40px; font-size:0.8rem;">GENERATED BY KRISHIMITRA APP</center>');
            printWindow.document.write('</div>');

            printWindow.document.write('</body></html>');
            printWindow.document.close();
            setTimeout(function() {{ printWindow.print(); printWindow.close(); }}, 500);
        }}
    </script>
    </body></html>
    """