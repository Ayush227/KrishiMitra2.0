import random
from .shared import get_header, get_navbar

# --- DATA GENERATORS ---

def get_trend():
    val = random.choice(['up', 'down', 'stable'])
    if val == 'up': return ('fas fa-arrow-up', '#198754')
    if val == 'down': return ('fas fa-arrow-down', '#dc3545')
    return ('fas fa-minus', '#6c757d')

def generate_items(category_list, min_price, max_price):
    data = []
    for item in category_list:
        trend_icon, trend_color = get_trend()
        data.append({
            "name": item,
            "price": random.randint(min_price, max_price),
            "trend_icon": trend_icon,
            "trend_color": trend_color
        })
    return data

# --- STATIC LISTS ---

FRUITS_LIST = ["Apple (Fuji)", "Banana (Robusta)", "Mango (Alphonso)", "Grapes (Black)", "Orange (Nagpur)", "Papaya", "Pomegranate", "Guava", "Pineapple", "Watermelon", "Muskmelon", "Strawberry", "Kiwi", "Dragon Fruit", "Pear", "Peach", "Plum", "Cherry", "Lychee", "Custard Apple"]
VEG_LIST = ["Potato", "Onion (Red)", "Tomato (Hybrid)", "Cauliflower", "Cabbage", "Spinach", "Okra (Bhindi)", "Brinjal", "Carrot", "Radish", "Green Chilli", "Capsicum", "Bitter Gourd", "Bottle Gourd", "Pumpkin", "Cucumber", "Peas", "Beans", "Garlic", "Ginger"]
FLOWERS_LIST = ["Rose (Red)", "Marigold (Orange)", "Jasmine", "Lotus", "Orchid", "Lily", "Sunflower", "Hibiscus", "Tulip", "Daisy", "Lavender", "Chrysanthemum", "Dahlia", "Gerbera", "Carnation", "Gladiolus", "Tuberose", "Bougainvillea", "Zinnia", "Petunia"]
CROPS_LIST = ["Wheat (Sharbati)", "Rice (Basmati)", "Maize", "Barley", "Millet (Bajra)", "Sorghum (Jowar)", "Cotton", "Sugarcane", "Soybean", "Mustard", "Groundnut", "Chickpea (Chana)", "Lentil (Masoor)", "Black Gram (Urad)", "Green Gram (Moong)", "Jute", "Tea", "Coffee", "Tobacco", "Rubber"]
TOOLS_DATA = [
    {"name": "Tractor (45HP)", "price": "6,50,000"}, {"name": "Rotavator", "price": "95,000"},
    {"name": "Cultivator", "price": "35,000"}, {"name": "Seed Drill", "price": "45,000"},
    {"name": "Plough", "price": "28,000"}, {"name": "Harvester", "price": "18,00,000"},
    {"name": "Sprayer (Manual)", "price": "2,500"}, {"name": "Sprayer (Power)", "price": "12,000"},
    {"name": "Drip Kit (1 Acre)", "price": "45,000"}, {"name": "Water Pump (5HP)", "price": "22,000"},
    {"name": "Sickle", "price": "150"}, {"name": "Spade (Phawda)", "price": "450"},
    {"name": "Axe", "price": "600"}, {"name": "Hoe", "price": "350"},
    {"name": "Wheelbarrow", "price": "3,500"}, {"name": "Chaff Cutter", "price": "18,000"},
    {"name": "Thresher", "price": "1,20,000"}, {"name": "Power Tiller", "price": "1,80,000"},
    {"name": "Solar Trap", "price": "1,200"}, {"name": "Soil Tester", "price": "8,000"}
]

# --- RENDER HELPER ---

def render_section(title, icon, color_theme, items, is_static=False, bg_color_code="#fff"):
    """
    bg_color_code: The color this section wants the background to be
    """
    
    # Gradient for Icon Box
    themes = {
        "fruit": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%)",
        "veg": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
        "flower": "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)",
        "crop": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
        "tool": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"
    }
    bg_gradient = themes.get(color_theme, "#fff")
    
    cards_html = ""
    for item in items:
        if is_static:
            main_price = f"₹{item['price']}"
            sub_info = '<span style="color:#777; font-size:0.8rem;">MRP (Approx)</span>'
            trend_html = '<div style="color:#555; font-size:0.75rem; margin-top:5px;">Fixed Price</div>'
        else:
            price_qtl = item['price']
            price_kg = round(price_qtl / 100, 2)
            main_price = f"₹{price_qtl} <span style='font-size:0.9rem; color:#555; font-weight:normal;'>/Qtl</span>"
            sub_info = f'<span style="color:#198754; font-weight:bold; font-size:0.85rem;">₹{price_kg} / kg</span>'
            trend_html = f'<div style="color:{item["trend_color"]}; font-weight:bold; font-size:0.8rem; margin-top:5px;"><i class="{item["trend_icon"]}"></i> Trend</div>'

        cards_html += f"""
        <div class="market-card">
            <div class="card-icon-small" style="background:{bg_gradient}"><i class="{icon}"></i></div>
            <div style="flex:1;">
                <h4 style="margin:0; color:#333; font-size:1rem; font-weight:700;">{item['name']}</h4>
                <div style="margin-top:5px; margin-bottom:2px;">{main_price}</div>
                <div>{sub_info}</div>
                {trend_html}
            </div>
        </div>
        """
    
    # We add a 'data-color' attribute so JS knows which color to switch to
    return f"""
    <div id="{title.lower()}" class="scroll-section" data-color="{bg_color_code}" style="padding-top: 80px; margin-bottom: 50px;">
        <h2 style="color:#333; border-left: 5px solid #333; padding-left: 15px; margin-bottom: 20px;">
            <i class="{icon}" style="color:#555; margin-right:10px;"></i> {title}
        </h2>
        <div class="market-grid">
            {cards_html}
        </div>
    </div>
    """

def render_market(date):
    fruits = generate_items(FRUITS_LIST, 2000, 15000)
    veg = generate_items(VEG_LIST, 500, 4000)
    flowers = generate_items(FLOWERS_LIST, 100, 2000) 
    crops = generate_items(CROPS_LIST, 1500, 8000)
    
    return f"""
    {get_header("Live Market")}
    {get_navbar(back_link="/")}
    
    <style>
        /* 1. SMOOTH BACKGROUND TRANSITION */
        body {{
            background-color: #fff0f3; /* Default (Fruit Color) */
            transition: background-color 1.2s ease;
            position: relative;
        }}
        
        /* 2. ANIMATED BUBBLES IN BACKGROUND */
        .bubble {{
            position: fixed;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            animation: float 20s infinite linear;
            z-index: -1;
        }}
        @keyframes float {{
            0% {{ transform: translateY(100vh) scale(0); opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ transform: translateY(-100px) scale(1.5); opacity: 0; }}
        }}

        /* NAVIGATION TABS */
        .sticky-nav {{
            position: sticky;
            top: 80px;
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 15px;
            z-index: 999;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
            border-bottom: 1px solid rgba(0,0,0,0.05);
            flex-wrap: wrap;
            transition: background-color 0.5s;
        }}
        
        .nav-pill {{
            padding: 8px 20px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            color: #555;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(0,0,0,0.1);
            transition: 0.3s;
            display: flex; align-items: center; gap: 8px;
        }}
        .nav-pill:hover {{ transform: translateY(-3px); color: black; background: white; }}
        
        .market-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
        }}
        
        .market-card {{
            background: rgba(255, 255, 255, 0.65); /* More see-through */
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 20px;
            border-radius: 15px;
            display: flex; align-items: center; gap: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.03);
            transition: 0.3s;
        }}
        .market-card:hover {{
            background: rgba(255, 255, 255, 0.95);
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: #198754;
        }}
        
        .card-icon-small {{
            width: 50px; height: 50px;
            border-radius: 12px;
            display: flex; justify-content: center; align-items: center;
            font-size: 1.5rem; color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
    </style>

    <div class="bubble" style="width: 200px; height: 200px; left: 10%; animation-duration: 25s;"></div>
    <div class="bubble" style="width: 150px; height: 150px; left: 70%; animation-duration: 20s; animation-delay: 2s;"></div>
    <div class="bubble" style="width: 300px; height: 300px; left: 40%; animation-duration: 30s; animation-delay: 5s;"></div>
    <div class="bubble" style="width: 100px; height: 100px; left: 85%; animation-duration: 18s; animation-delay: 8s;"></div>

    <div class="sticky-nav">
        <a href="#fruits" class="nav-pill" style="border-bottom: 3px solid #ff9a9e;"><i class="fas fa-apple-alt"></i> Fruits</a>
        <a href="#vegetables" class="nav-pill" style="border-bottom: 3px solid #84fab0;"><i class="fas fa-carrot"></i> Veggies</a>
        <a href="#flowers" class="nav-pill" style="border-bottom: 3px solid #e0c3fc;"><i class="fas fa-seedling"></i> Flowers</a>
        <a href="#crops" class="nav-pill" style="border-bottom: 3px solid #f6d365;"><i class="fas fa-wheat"></i> Crops</a>
        <a href="#tools" class="nav-pill" style="border-bottom: 3px solid #a1c4fd;"><i class="fas fa-tractor"></i> Tools</a>
    </div>

    <div class="container">
        <div style="text-align:center; margin: 40px 0;">
            <h1 style="font-weight: 800; color: #333; font-size: 2.5rem; text-shadow: 2px 2px 0px rgba(255,255,255,0.5);">Live Market Dashboard</h1>
            <p style="color: #555; font-weight:500;">Real-time prices from 500+ Mandis across India • {date}</p>
        </div>

        {render_section("Fruits", "fas fa-apple-alt", "fruit", fruits, bg_color_code="#fff0f3")}
        
        {render_section("Vegetables", "fas fa-carrot", "veg", veg, bg_color_code="#f0fff4")}
        
        {render_section("Flowers", "fas fa-seedling", "flower", flowers, bg_color_code="#f3f0ff")}
        
        {render_section("Crops", "fas fa-wheat", "crop", crops, bg_color_code="#fffdf0")}
        
        {render_section("Farming Tools", "fas fa-tractor", "tool", TOOLS_DATA, is_static=True, bg_color_code="#f0f8ff")}
        
        <div style="height: 300px;"></div> </div>

    <script>
        // Options for the observer
        const options = {{
            root: null,
            rootMargin: '-50% 0px -50% 0px', // Trigger when section is in middle of screen
            threshold: 0
        }};

        // Callback function
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const newColor = entry.target.getAttribute('data-color');
                    if (newColor) {{
                        document.body.style.backgroundColor = newColor;
                    }}
                }}
            }});
        }}, options);

        // Observe all sections
        const sections = document.querySelectorAll('.scroll-section');
        sections.forEach(section => {{
            observer.observe(section);
        }});
    </script>

    </body></html>
    """