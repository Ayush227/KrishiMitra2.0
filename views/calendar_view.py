import json
from .shared import get_header, get_navbar

def render_calendar(tasks):
    tasks_json = json.dumps(tasks)

    return f"""
    {get_header("Smart Calendar")}
    {get_navbar(back_link="/")}

    <style>
        /* 1. BACKGROUND & LAYOUT */
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', sans-serif;
            color: white;
            overflow-x: hidden;
        }}

        .calendar-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 40px; /* Increased gap for breathing room */
            max-width: 1200px; /* Wider container */
            margin: 40px auto;
            padding: 0 30px;
            align-items: flex-start; /* Prevents stretching */
        }}

        /* 2. CALENDAR CARD (Left Side - 65% Width) */
        .calendar-card {{
            flex: 2; /* Takes up more space */
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 35px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            min-width: 400px;
        }}

        .cal-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }}
        .month-year {{ font-size: 2rem; font-weight: 800; letter-spacing: 1px; }}
        
        .nav-btn {{
            background: rgba(255,255,255,0.15); border: none; color: white;
            width: 45px; height: 45px; border-radius: 50%;
            cursor: pointer; transition: 0.3s; font-size: 1.2rem;
            display: flex; align-items: center; justify-content: center;
        }}
        .nav-btn:hover {{ background: white; color: #764ba2; transform: scale(1.1); }}

        .weekdays {{
            display: grid; grid-template-columns: repeat(7, 1fr);
            text-align: center; font-weight: 600; margin-bottom: 15px;
            color: rgba(255,255,255,0.6); font-size: 0.9rem; text-transform: uppercase;
        }}
        .days {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 12px; }}
        
        .day {{
            height: 70px; /* Taller cells */
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.2s;
            font-size: 1.1rem; font-weight: 500;
            border: 1px solid transparent;
        }}
        .day:hover {{ background: rgba(255, 255, 255, 0.25); transform: translateY(-3px); }}
        .today {{ background: rgba(255, 255, 255, 0.35); border: 1px solid white; font-weight: 800; }}
        
        .has-task {{ border-color: #ffd700; background: rgba(255, 215, 0, 0.15); }}
        .task-dot {{
            width: 6px; height: 6px; background-color: #ffd700;
            border-radius: 50%; margin-top: 6px;
            box-shadow: 0 0 8px #ffd700; display: none;
        }}
        .has-task .task-dot {{ display: block; }}

        /* 3. TASK SIDEBAR (Right Side - 35% Width) */
        .task-panel {{
            flex: 1; /* Compact width */
            background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            padding: 25px;
            min-width: 320px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            max-height: 80vh; /* Limits height so it doesn't stretch page */
            display: flex; flex-direction: column;
        }}

        /* Compact Forms */
        .compact-box {{
            background: rgba(255,255,255,0.08);
            padding: 15px; border-radius: 15px;
            margin-bottom: 15px;
        }}
        
        .input-row {{ display: flex; gap: 8px; margin-bottom: 8px; }}
        
        input, select {{
            background: rgba(255,255,255,0.9); border: none;
            padding: 10px; border-radius: 8px; font-size: 0.9rem;
            outline: none; width: 100%;
        }}
        
        .btn-action {{
            width: 100%; padding: 10px; border: none; border-radius: 8px;
            font-weight: bold; cursor: pointer; transition: 0.2s;
            font-size: 0.9rem;
        }}
        .btn-green {{ background: #198754; color: white; }}
        .btn-gold {{ background: #ffd700; color: #333; }}
        .btn-action:hover {{ opacity: 0.9; transform: translateY(-1px); }}

        /* Clean List */
        .task-list-container {{
            flex: 1; overflow-y: auto;
            margin-top: 10px; padding-right: 5px;
        }}
        /* Custom Scrollbar */
        .task-list-container::-webkit-scrollbar {{ width: 5px; }}
        .task-list-container::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.3); border-radius: 10px; }}

        .task-card {{
            background: white; color: #444;
            padding: 12px 15px; border-radius: 12px;
            margin-bottom: 8px;
            display: flex; justify-content: space-between; align-items: center;
            border-left: 4px solid #ccc;
            font-size: 0.9rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .task-date {{ font-size: 0.75rem; color: #888; font-weight: 700; margin-bottom: 2px; }}
        .del-icon {{ color: #ff6b6b; cursor: pointer; padding: 5px; }}
        .del-icon:hover {{ color: #d63384; }}

        /* 4. POP-UP MODAL */
        .modal-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(5px);
            z-index: 1000; display: none; justify-content: center; align-items: center;
            opacity: 0; transition: opacity 0.3s ease;
        }}
        .modal-card {{
            background: white; color: #333; width: 90%; max-width: 380px;
            border-radius: 20px; padding: 25px;
            transform: translateY(20px); transition: transform 0.3s ease;
            text-align: center;
        }}
        .modal-open .modal-overlay {{ display: flex; opacity: 1; }}
        .modal-open .modal-card {{ transform: translateY(0); }}

        @media (max-width: 900px) {{
            .calendar-container {{ flex-direction: column; }}
            .calendar-card, .task-panel {{ width: 100%; min-width: auto; }}
        }}
    </style>

    <div id="taskModal" class="modal-overlay">
        <div class="modal-card">
            <h2 id="modalDateDisplay" style="margin:0; color:#764ba2; font-size:2.5rem;">25</h2>
            <p id="modalMonthDisplay" style="color:#777; margin-top:0;">November</p>
            <div style="text-align:left; max-height:200px; overflow-y:auto; margin:15px 0;" id="modalTaskList"></div>
            <button onclick="closeModal()" style="background:#667eea; color:white; border:none; padding:10px 30px; border-radius:50px; cursor:pointer;">Close</button>
        </div>
    </div>

    <div class="calendar-container">
        
        <div class="calendar-card">
            <div class="cal-header">
                <button class="nav-btn" onclick="changeMonth(-1)"><i class="fas fa-chevron-left"></i></button>
                <div class="month-year" id="monthYear"></div>
                <button class="nav-btn" onclick="changeMonth(1)"><i class="fas fa-chevron-right"></i></button>
            </div>
            
            <div class="weekdays">
                <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
            </div>
            <div class="days" id="daysGrid"></div>
        </div>

        <div class="task-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="margin:0; font-size:1.2rem;"><i class="fas fa-clipboard-list"></i> Planner</h3>
                <span style="font-size:0.8rem; background:rgba(255,255,255,0.2); padding:2px 8px; border-radius:10px;">{len(tasks)} Tasks</span>
            </div>
            
            <div class="compact-box">
                <div style="font-size:0.85rem; color:#ffd700; margin-bottom:8px; font-weight:bold;">⚡ Quick Schedule</div>
                <form method="POST" action="/auto_schedule">
                    <div class="input-row">
                        <select name="crop_name" required>
                            <option value="" disabled selected>Crop...</option>
                            <option value="Wheat">Wheat</option>
                            <option value="Rice">Rice</option>
                            <option value="Cotton">Cotton</option>
                            <option value="Tomato">Tomato</option>
                        </select>
                        <input type="date" name="start_date" required>
                    </div>
                    <button type="submit" class="btn-action btn-green">Auto-Fill</button>
                </form>
            </div>

            <div class="compact-box">
                <div style="font-size:0.85rem; color:#fff; margin-bottom:8px; font-weight:bold;">✏️ Add Note</div>
                <form method="POST" action="/add_task">
                    <input type="hidden" name="date" id="selectedDate">
                    <div class="input-row">
                        <input type="text" name="task" placeholder="Type task..." required>
                        <button type="submit" class="btn-action btn-gold" style="width:auto; padding:0 20px;">+</button>
                    </div>
                    <div style="font-size:0.75rem; opacity:0.7; text-align:center;">*Select a date on calendar first</div>
                </form>
            </div>

            <div class="task-list-container">
                {''.join([f'''
                <div class="task-card" style="border-left-color: {'#198754' if 'Sow' in t['title'] else '#0dcaf0' if 'Irrigation' in t['title'] else '#ffd700' if 'Harvest' in t['title'] else '#6f42c1'};">
                    <div>
                        <div class="task-date">{t['date']}</div>
                        <div style="font-weight:600;">{t['title']}</div>
                    </div>
                    <a href="/delete_task/{t['id']}" class="del-icon"><i class="fas fa-times"></i></a>
                </div>
                ''' for t in sorted(tasks, key=lambda x: x['date'])])}
                
                { '<div style="text-align:center; opacity:0.5; font-size:0.9rem; margin-top:20px;">No upcoming tasks.</div>' if not tasks else '' }
            </div>
        </div>
    </div>

    <script>
        const date = new Date();
        const tasks = {tasks_json}; 
        
        function renderCalendar() {{
            date.setDate(1);
            const monthDays = document.getElementById('daysGrid');
            const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
            const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
            const firstDayIndex = date.getDay();
            const nextDays = 7 - new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay() - 1;

            const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            document.getElementById('monthYear').innerText = months[date.getMonth()] + " " + date.getFullYear();

            let days = "";
            for (let x = firstDayIndex; x > 0; x--) {{
                days += `<div class="day" style="opacity:0.3">${{prevLastDay - x + 1}}</div>`;
            }}

            for (let i = 1; i <= lastDay; i++) {{
                let m = (date.getMonth() + 1).toString().padStart(2, '0');
                let d = i.toString().padStart(2, '0');
                let fullDate = `${{date.getFullYear()}}-${{m}}-${{d}}`;
                
                let isToday = (i === new Date().getDate() && date.getMonth() === new Date().getMonth()) ? "today" : "";
                let dayTasks = tasks.filter(t => t.date === fullDate);
                let hasTask = dayTasks.length > 0 ? "has-task" : "";

                days += `<div class="day ${{isToday}} ${{hasTask}}" onclick='handleDayClick("${{fullDate}}", ${{JSON.stringify(dayTasks)}})'>
                            ${{i}} <div class="task-dot"></div>
                        </div>`;
            }}

            for (let j = 1; j <= nextDays; j++) {{
                days += `<div class="day" style="opacity:0.3">${{j}}</div>`;
            }}
            monthDays.innerHTML = days;
        }}

        function changeMonth(n) {{
            date.setMonth(date.getMonth() + n);
            renderCalendar();
        }}

        function handleDayClick(dateStr, dayTasks) {{
            document.getElementById('selectedDate').value = dateStr;
            if (dayTasks.length > 0) {{
                const dObj = new Date(dateStr);
                const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                document.getElementById('modalDateDisplay').innerText = dObj.getDate();
                document.getElementById('modalMonthDisplay').innerText = months[dObj.getMonth()] + " " + dObj.getFullYear();
                
                let html = "";
                dayTasks.forEach(t => {{
                    html += `<div style="padding:10px; border-bottom:1px solid #eee; display:flex; justify-content:space-between;">
                                <span>${{t.title}}</span>
                                <a href="/delete_task/${{t.id}}" style="color:red;"><i class="fas fa-trash"></i></a>
                             </div>`;
                }});
                document.getElementById('modalTaskList').innerHTML = html;
                document.body.classList.add('modal-open');
            }} else {{
                 // Visual feedback: Flash the manual add box
                 const box = document.querySelectorAll('.compact-box')[1];
                 box.style.background = "rgba(255,255,255,0.2)";
                 setTimeout(() => box.style.background = "rgba(255,255,255,0.08)", 300);
            }}
        }}

        function closeModal() {{ document.body.classList.remove('modal-open'); }}
        renderCalendar();
    </script>
    </body></html>
    """