from .shared import get_header, get_navbar

def render_tool(result=None):
    
    # Generate the Result HTML if a diagnosis exists
    result_html = ""
    if result:
        color = "#dc3545" # Red for Danger
        if result['severity'] == "None": color = "#198754" # Green for Healthy
        
        result_html = f"""
        <div class="report-overlay" id="reportCard">
            <div class="medical-report">
                <div class="report-header">
                    <div>
                        <h2 style="margin:0;">DIAGNOSTIC REPORT</h2>
                        <span style="font-size:0.8rem; opacity:0.8;">ID: #KM-{result['image_name'][:5].upper()}</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-weight:bold; color:{color}; border:2px solid {color}; padding:5px 10px; border-radius:5px;">
                            {result['severity'].upper()}
                        </div>
                    </div>
                </div>
                
                <div class="report-body">
                    <div class="scan-row">
                        <span class="label">Detected Issue:</span>
                        <span class="value" style="color:{color}; font-size:1.3rem;">{result['disease']}</span>
                    </div>
                    <div class="scan-row">
                        <span class="label">AI Confidence:</span>
                        <span class="value">{result['accuracy']} <i class="fas fa-check-circle" style="color:#198754;"></i></span>
                    </div>
                    
                    <div style="margin-top:20px; background:#f8f9fa; padding:15px; border-left:5px solid #198754;">
                        <h4 style="margin:0 0 5px 0; color:#198754;"><i class="fas fa-pills"></i> Rx: Prescription / Remedy</h4>
                        <p style="margin:0; font-size:1rem; color:#555;">{result['remedy']}</p>
                    </div>
                </div>

                <div class="report-footer">
                    <button onclick="closeReport()" class="btn-close">Close Report</button>
                    <button onclick="window.print()" class="btn-print"><i class="fas fa-print"></i> Print</button>
                </div>
            </div>
        </div>
        """

    return f"""
    {get_header("Crop Doctor | Diagnostics")}
    {get_navbar(back_link="/")}
    
    <style>
        /* HOSPITAL THEME */
        body {{
            background-color: #f0f4f8;
            background-image: 
                linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)),
                url('https://img.freepik.com/free-vector/clean-medical-background_53876-116876.jpg');
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
        }}

        .container {{
            max-width: 900px;
            margin: 40px auto;
            text-align: center;
        }}

        /* SCANNER CARD */
        .scanner-card {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            position: relative;
            border: 1px solid #e1e1e1;
        }}

        .scanner-header {{
            background: #0d6efd; /* Medical Blue */
            padding: 20px;
            color: white;
            display: flex; justify-content: space-between; align-items: center;
        }}

        /* PULSE ANIMATION */
        .ecg-line {{
            width: 150px;
            height: 50px;
            background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Electrocardiogram_animated.gif/220px-Electrocardiogram_animated.gif');
            background-size: cover;
            filter: invert(1);
            opacity: 0.8;
        }}

        /* UPLOAD AREA */
        .upload-zone {{
            padding: 50px;
            border: 3px dashed #cbd5e0;
            margin: 30px;
            border-radius: 15px;
            transition: 0.3s;
            position: relative;
            background: #f8fbff;
        }}
        .upload-zone:hover {{ border-color: #0d6efd; background: #eaf2ff; }}

        /* LASER SCANNER EFFECT */
        .laser-line {{
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(to right, transparent, #ef4444, transparent);
            box-shadow: 0 0 10px #ef4444;
            display: none; /* Hidden by default */
            z-index: 10;
        }}
        .scanning .laser-line {{
            display: block;
            animation: scanMove 2s infinite ease-in-out;
        }}
        @keyframes scanMove {{ 0% {{ top: 0; }} 100% {{ top: 100%; }} }}

        input[type="file"] {{
            position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer;
        }}

        /* MEDICAL REPORT (Modal) */
        .report-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(5px);
            z-index: 1000;
            display: flex; justify-content: center; align-items: center;
            animation: fadeIn 0.3s;
        }}
        .medical-report {{
            background: white;
            width: 90%; max-width: 500px;
            border-top: 8px solid #0d6efd;
            border-radius: 10px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            overflow: hidden;
            animation: slideUp 0.4s;
        }}
        @keyframes slideUp {{ from {{ transform: translateY(50px); opacity:0; }} to {{ transform: translateY(0); opacity:1; }} }}
        
        .report-header {{ padding: 20px; background: #f8f9fa; border-bottom: 1px solid #eee; display: flex; justify-content:space-between; }}
        .report-body {{ padding: 30px; text-align: left; }}
        
        .scan-row {{ display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .label {{ font-weight: 600; color: #777; }}
        .value {{ font-weight: 800; color: #333; }}

        .report-footer {{ padding: 20px; background: #f8f9fa; text-align: right; display: flex; gap: 10px; justify-content: flex-end; }}
        
        .btn-close {{ background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }}
        .btn-print {{ background: #0d6efd; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }}
        
        /* LOADING SCREEN */
        .loading-screen {{
            display: none;
            position: absolute; top:0; left:0; width:100%; height:100%;
            background: white;
            flex-direction: column; justify-content: center; align-items: center;
            z-index: 20;
        }}
        .loader {{
            border: 8px solid #f3f3f3; border-top: 8px solid #0d6efd;
            border-radius: 50%; width: 60px; height: 60px;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}

    </style>

    <div class="container">
        <h1 style="color:#0d6efd; font-weight:800; margin-bottom:10px;"><i class="fas fa-hospital-symbol"></i> CROP HOSPITAL</h1>
        <p style="color:#555; margin-bottom:40px;">AI-Powered Diagnostic Center • 95% Precision Rate</p>

        <div class="scanner-card">
            
            <div class="scanner-header">
                <div>
                    <h3 style="margin:0;">UPLOAD SAMPLE</h3>
                    <small>Accepted: JPG, PNG</small>
                </div>
                <div class="ecg-line"></div>
            </div>

            <form method="POST" action="/tool" enctype="multipart/form-data" id="scanForm">
                <div class="upload-zone" id="dropZone">
                    <div class="laser-line"></div> <i class="fas fa-microscope" style="font-size: 4rem; color: #cbd5e0; margin-bottom: 20px;"></i>
                    <h3 style="color:#555;">Drag & Drop Leaf Image</h3>
                    <p style="color:#999;">or click to browse gallery</p>
                    <input type="file" name="file" accept="image/*" onchange="startScan()" required>
                </div>
            </form>
            
            <div class="loading-screen" id="loader">
                <div class="loader"></div>
                <h3 style="margin-top:20px; color:#0d6efd;">Analyzing Cellular Structure...</h3>
                <p style="color:#777;">Please wait while AI diagnoses the sample.</p>
            </div>

        </div>
        
        <div style="display:flex; gap:20px; margin-top:40px; justify-content:center;">
            <div style="background:white; padding:20px; border-radius:10px; box-shadow:0 5px 15px rgba(0,0,0,0.05); width:200px;">
                <i class="fas fa-shield-alt" style="font-size:2rem; color:#198754; margin-bottom:10px;"></i>
                <h4>95% Accuracy</h4>
                <p style="font-size:0.8rem; color:#777;">Trustworthy Results</p>
            </div>
            <div style="background:white; padding:20px; border-radius:10px; box-shadow:0 5px 15px rgba(0,0,0,0.05); width:200px;">
                <i class="fas fa-user-md" style="font-size:2rem; color:#0d6efd; margin-bottom:10px;"></i>
                <h4>Expert Remedies</h4>
                <p style="font-size:0.8rem; color:#777;">Instant Prescriptions</p>
            </div>
        </div>

    </div>

    {result_html}

    <script>
        function startScan() {{
            const zone = document.getElementById('dropZone');
            const loader = document.getElementById('loader');
            const form = document.getElementById('scanForm');
            
            // 1. Start Laser Animation
            zone.classList.add('scanning');
            
            // 2. Show Loading Screen after short delay
            setTimeout(() => {{
                loader.style.display = 'flex';
                // 3. Submit Form
                setTimeout(() => {{
                    form.submit();
                }}, 2000); // 2 second fake scan time
            }}, 500);
        }}

        function closeReport() {{
            document.getElementById('reportCard').style.display = 'none';
        }}
    </script>
    </body></html>
    """