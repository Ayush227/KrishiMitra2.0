from .shared import get_header, get_navbar

# --- THE MASSIVE KNOWLEDGE BASE (100+ Items) ---
GUIDE_DATA = [
    # --- CEREALS & GRAINS ---
    { "name": "Wheat (Sharbati)", "category": "grain", "icon": "fas fa-wheat", "color": "#f5deb3", "soil": "Loam/Clay.", "climate": "Cool (10-15°C).", "sowing": "Nov-Dec", "harvest": "Mar-Apr", "tip": "Sow before Dec 15.", "nutrients": "Carbs, Fiber, Iron", "benefits": "Energy, metabolism, digestion." },
    { "name": "Rice (Basmati)", "category": "grain", "icon": "fas fa-seedling", "color": "#90ee90", "soil": "Clayey.", "climate": "Hot & Humid.", "sowing": "Jun-July", "harvest": "Oct-Nov", "tip": "Needs standing water.", "nutrients": "Carbs, Vit B", "benefits": "Instant energy, gut health." },
    { "name": "Maize (Corn)", "category": "grain", "icon": "fas fa-corn", "color": "#ffd700", "soil": "Fertile Loam.", "climate": "Warm.", "sowing": "Jun-July", "harvest": "100 days", "tip": "Check for Armyworm.", "nutrients": "Fiber, Antioxidants", "benefits": "Eye health, prevents anemia." },
    { "name": "Barley (Jau)", "category": "grain", "icon": "fas fa-leaf", "color": "#e6c229", "soil": "Sandy Loam.", "climate": "Cool.", "sowing": "Oct-Nov", "harvest": "Mar-Apr", "tip": "Saline tolerant.", "nutrients": "Beta-glucan, Selenium", "benefits": "Cholesterol control, weight loss." },
    { "name": "Pearl Millet (Bajra)", "category": "grain", "icon": "fas fa-circle", "color": "#8b4513", "soil": "Sandy.", "climate": "Hot/Dry.", "sowing": "June", "harvest": "Sept", "tip": "Drought hardy.", "nutrients": "Iron, Protein", "benefits": "Heart health, diabetes control." },
    { "name": "Sorghum (Jowar)", "category": "grain", "icon": "fas fa-bread-slice", "color": "#d2b48c", "soil": "Black soil.", "climate": "Warm.", "sowing": "June", "harvest": "Oct", "tip": "Treat seeds with sulfur.", "nutrients": "Protein, Fiber", "benefits": "Bone health, immunity." },
    { "name": "Finger Millet (Ragi)", "category": "grain", "icon": "fas fa-cookie", "color": "#800000", "soil": "Red Loam.", "climate": "Tropical.", "sowing": "May-Aug", "harvest": "Dec", "tip": "Good for rainfed areas.", "nutrients": "Calcium (High)", "benefits": "Strong bones, diabetes management." },
    { "name": "Oats", "category": "grain", "icon": "fas fa-bowl-food", "color": "#fffdd0", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Mar", "tip": "Avoid waterlogging.", "nutrients": "Beta-glucan, Protein", "benefits": "Lowers cholesterol, skin health." },
    { "name": "Quinoa", "category": "grain", "icon": "fas fa-dot-circle", "color": "#f4a460", "soil": "Sandy Loam.", "climate": "Cool.", "sowing": "Nov", "harvest": "Mar", "tip": "Remove saponin.", "nutrients": "Complete Protein", "benefits": "Metabolism, high antioxidants." },
    { "name": "Buckwheat (Kuttu)", "category": "grain", "icon": "fas fa-spa", "color": "#a0522d", "soil": "Poor soil.", "climate": "Cool.", "sowing": "July", "harvest": "Oct", "tip": "Suppress weeds.", "nutrients": "Rutin, Magnesium", "benefits": "Blood pressure, heart health." },

    # --- VEGETABLES ---
    { "name": "Tomato", "category": "veg", "icon": "fas fa-apple-alt", "color": "#ff6347", "soil": "Sandy Loam.", "climate": "Warm.", "sowing": "Aug/Feb", "harvest": "60 days", "tip": "Stake plants.", "nutrients": "Lycopene, Vit C", "benefits": "Skin health, cancer prevention." },
    { "name": "Potato", "category": "veg", "icon": "fas fa-cloud-meatball", "color": "#d2b48c", "soil": "Loose Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "90 days", "tip": "Earth up soil.", "nutrients": "Potassium, Vit B6", "benefits": "Brain function, energy." },
    { "name": "Onion", "category": "veg", "icon": "fas fa-bullseye", "color": "#dda0dd", "soil": "Friable Loam.", "climate": "Cool/Warm.", "sowing": "Oct/Jun", "harvest": "110 days", "tip": "Stop water before harvest.", "nutrients": "Quercetin, Sulfur", "benefits": "Immunity, hair health." },
    { "name": "Brinjal", "category": "veg", "icon": "fas fa-egg", "color": "#4b0082", "soil": "Silt Loam.", "climate": "Warm.", "sowing": "Feb/July", "harvest": "60 days", "tip": "Check shoot borer.", "nutrients": "Nasunin, Fiber", "benefits": "Brain cells, weight loss." },
    { "name": "Okra (Bhindi)", "category": "veg", "icon": "fas fa-pepper-hot", "color": "#228b22", "soil": "Sandy Loam.", "climate": "Hot.", "sowing": "Feb-July", "harvest": "45 days", "tip": "Check YVMV virus.", "nutrients": "Folate, Magnesium", "benefits": "Pregnancy health, digestion." },
    { "name": "Cauliflower", "category": "veg", "icon": "fas fa-brain", "color": "#fffacd", "soil": "Rich Loam.", "climate": "Cool.", "sowing": "Sept", "harvest": "90 days", "tip": "Blanch curds.", "nutrients": "Choline, Fiber", "benefits": "Liver detox, brain health." },
    { "name": "Cabbage", "category": "veg", "icon": "fas fa-circle-notch", "color": "#98fb98", "soil": "Well Drained.", "climate": "Cool.", "sowing": "Sept", "harvest": "80 days", "tip": "Consistent water.", "nutrients": "Vit K, Sulfur", "benefits": "Ulcer healing, digestion." },
    { "name": "Spinach", "category": "veg", "icon": "fas fa-leaf", "color": "#006400", "soil": "Fertile.", "climate": "Cool.", "sowing": "Sep-Nov", "harvest": "30 days", "tip": "Cut & regrow.", "nutrients": "Iron, Vit A", "benefits": "Eyesight, anemia cure." },
    { "name": "Carrot", "category": "veg", "icon": "fas fa-carrot", "color": "#ff8c00", "soil": "Deep Sandy.", "climate": "Cool.", "sowing": "Aug-Nov", "harvest": "80 days", "tip": "No fresh manure.", "nutrients": "Beta-carotene", "benefits": "Vision, skin glow." },
    { "name": "Radish", "category": "veg", "icon": "fas fa-candy-cane", "color": "#fff", "soil": "Sandy.", "climate": "Cool.", "sowing": "Sep-Jan", "harvest": "40 days", "tip": "Fast crop.", "nutrients": "Potassium, Fiber", "benefits": "Liver detox, blood pressure." },
    { "name": "Green Chilli", "category": "veg", "icon": "fas fa-pepper-hot", "color": "#008000", "soil": "Loam.", "climate": "Warm.", "sowing": "May", "harvest": "60 days", "tip": "Control thrips.", "nutrients": "Capsaicin, Vit C", "benefits": "Metabolism, pain relief." },
    { "name": "Bottle Gourd", "category": "veg", "icon": "fas fa-wine-bottle", "color": "#90ee90", "soil": "Sandy Loam.", "climate": "Hot.", "sowing": "Feb", "harvest": "60 days", "tip": "Use trellis.", "nutrients": "Water, Zinc", "benefits": "Cooling, weight loss." },
    { "name": "Bitter Gourd", "category": "veg", "icon": "fas fa-cookie-bite", "color": "#006400", "soil": "Loam.", "climate": "Warm.", "sowing": "Feb", "harvest": "60 days", "tip": "Hand pollinate.", "nutrients": "Charantin", "benefits": "Diabetes control, blood purity." },
    { "name": "Cucumber", "category": "veg", "icon": "fas fa-hotdog", "color": "#3cb371", "soil": "Sandy Loam.", "climate": "Hot.", "sowing": "Feb", "harvest": "45 days", "tip": "Frequent water.", "nutrients": "Silica, Water", "benefits": "Hydration, joint health." },
    { "name": "Pumpkin", "category": "veg", "icon": "fas fa-pumpkin", "color": "#ff7518", "soil": "Rich Loam.", "climate": "Warm.", "sowing": "Jan", "harvest": "100 days", "tip": "Protect fruit from soil.", "nutrients": "Vit A, Zinc", "benefits": "Immunity, prostate health." },
    { "name": "Peas", "category": "veg", "icon": "fas fa-dot-circle", "color": "#32cd32", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "60 days", "tip": "Fixes nitrogen.", "nutrients": "Protein, Vit K", "benefits": "Muscle health, bones." },
    { "name": "Beans", "category": "veg", "icon": "fas fa-grip-lines-vertical", "color": "#228b22", "soil": "Loam.", "climate": "Mild.", "sowing": "Aug", "harvest": "45 days", "tip": "Keep leaves dry.", "nutrients": "Folate, Iron", "benefits": "Heart health, sugar control." },
    { "name": "Garlic", "category": "veg", "icon": "fas fa-skull", "color": "#fffaf0", "soil": "Fertile.", "climate": "Cool.", "sowing": "Oct", "harvest": "130 days", "tip": "Plant cloves.", "nutrients": "Allicin, Sulfur", "benefits": "Antibiotic, immunity." },
    { "name": "Ginger", "category": "veg", "icon": "fas fa-bacterium", "color": "#deb887", "soil": "Sandy Loam.", "climate": "Humid.", "sowing": "May", "harvest": "8 months", "tip": "Mulch heavily.", "nutrients": "Gingerol", "benefits": "Nausea, muscle pain." },
    { "name": "Sweet Potato", "category": "veg", "icon": "fas fa-potato", "color": "#fa8072", "soil": "Sandy.", "climate": "Warm.", "sowing": "Feb", "harvest": "100 days", "tip": "Low nitrogen.", "nutrients": "Vit A, Fiber", "benefits": "Gut health, vision." },
    { "name": "Capsicum", "category": "veg", "icon": "fas fa-bell", "color": "#2e8b57", "soil": "Loam.", "climate": "Cool.", "sowing": "Aug", "harvest": "70 days", "tip": "Needs support.", "nutrients": "Vit C (High)", "benefits": "Metabolism, stress." },
    { "name": "Coriander", "category": "veg", "icon": "fas fa-leaf", "color": "#228b22", "soil": "Loam.", "climate": "Cool.", "sowing": "All year", "harvest": "30 days", "tip": "Split seeds.", "nutrients": "Vit K", "benefits": "Detox, digestion." },
    { "name": "Methi", "category": "veg", "icon": "fas fa-leaf", "color": "#9acd32", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "25 days", "tip": "Harvest young.", "nutrients": "Iron, Fiber", "benefits": "Diabetes, lactation." },
    { "name": "Beetroot", "category": "veg", "icon": "fas fa-heart", "color": "#8b0000", "soil": "Sandy.", "climate": "Cool.", "sowing": "Aug", "harvest": "60 days", "tip": "Thin plants.", "nutrients": "Nitrates", "benefits": "Lower BP, stamina." },
    { "name": "Turnip", "category": "veg", "icon": "fas fa-circle", "color": "#ff00ff", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "45 days", "tip": "Don't let woody.", "nutrients": "Vit C", "benefits": "Low calorie, immunity." },

    # --- FRUITS ---
    { "name": "Mango", "category": "fruit", "icon": "fas fa-lemon", "color": "#ffcc00", "soil": "Alluvial.", "climate": "Tropical.", "sowing": "July", "harvest": "Summer", "tip": "Prune branches.", "nutrients": "Vit A, C", "benefits": "Digestion, skin glow." },
    { "name": "Banana", "category": "fruit", "icon": "fas fa-moon", "color": "#ffe135", "soil": "Rich Loam.", "climate": "Humid.", "sowing": "All year", "harvest": "12 months", "tip": "Support bunches.", "nutrients": "Potassium, B6", "benefits": "Energy, cramps." },
    { "name": "Apple", "category": "fruit", "icon": "fas fa-apple-alt", "color": "#dc143c", "soil": "Loam.", "climate": "Cold.", "sowing": "Jan", "harvest": "Aug", "tip": "Cross pollinate.", "nutrients": "Pectin", "benefits": "Heart, weight loss." },
    { "name": "Guava", "category": "fruit", "icon": "fas fa-lemon", "color": "#98fb98", "soil": "Any.", "climate": "Tropical.", "sowing": "June", "harvest": "Winter", "tip": "Bend branches.", "nutrients": "Vit C", "benefits": "Immunity, constipation." },
    { "name": "Papaya", "category": "fruit", "icon": "fas fa-football-ball", "color": "#ff8c00", "soil": "Well Drained.", "climate": "Tropical.", "sowing": "Feb", "harvest": "9 months", "tip": "No waterlog.", "nutrients": "Papain", "benefits": "Digestion, periods." },
    { "name": "Pomegranate", "category": "fruit", "icon": "fas fa-bomb", "color": "#dc143c", "soil": "Sandy.", "climate": "Semi-arid.", "sowing": "July", "harvest": "6 months", "tip": "Prune shoots.", "nutrients": "Punicalagins", "benefits": "Cancer fight, BP." },
    { "name": "Grapes", "category": "fruit", "icon": "fas fa-wine-glass", "color": "#800080", "soil": "Sandy.", "climate": "Dry.", "sowing": "Jan", "harvest": "Mar", "tip": "Pruning key.", "nutrients": "Resveratrol", "benefits": "Anti-aging, heart." },
    { "name": "Orange", "category": "fruit", "icon": "fas fa-circle", "color": "#ffa500", "soil": "Loam.", "climate": "Sub-tropical.", "sowing": "July", "harvest": "Nov", "tip": "No limestone.", "nutrients": "Vit C", "benefits": "Immunity, skin." },
    { "name": "Watermelon", "category": "fruit", "icon": "fas fa-bowling-ball", "color": "#006400", "soil": "Riverbed.", "climate": "Hot.", "sowing": "Jan", "harvest": "90 days", "tip": "Stop water late.", "nutrients": "Lycopene", "benefits": "Hydration, muscle." },
    { "name": "Muskmelon", "category": "fruit", "icon": "fas fa-basketball-ball", "color": "#f0e68c", "soil": "Sandy.", "climate": "Hot.", "sowing": "Feb", "harvest": "90 days", "tip": "Rotate fruit.", "nutrients": "Vit A", "benefits": "Vision, BP." },
    { "name": "Pineapple", "category": "fruit", "icon": "fas fa-chess-rook", "color": "#daa520", "soil": "Acidic.", "climate": "Humid.", "sowing": "July", "harvest": "18 months", "tip": "Use shade.", "nutrients": "Bromelain", "benefits": "Digestion, bones." },
    { "name": "Strawberry", "category": "fruit", "icon": "fas fa-heart", "color": "#ff0000", "soil": "Sandy.", "climate": "Cool.", "sowing": "Oct", "harvest": "Feb", "tip": "Plastic mulch.", "nutrients": "Vit C", "benefits": "Teeth, sugar control." },
    { "name": "Lychee", "category": "fruit", "icon": "fas fa-dot-circle", "color": "#ffb6c1", "soil": "Deep Loam.", "climate": "Moist.", "sowing": "Aug", "harvest": "May", "tip": "Protect wind.", "nutrients": "Copper", "benefits": "Blood flow." },
    { "name": "Custard Apple", "category": "fruit", "icon": "fas fa-cloud", "color": "#90ee90", "soil": "Rocky.", "climate": "Tropical.", "sowing": "July", "harvest": "Oct", "tip": "Hardy.", "nutrients": "Magnesium", "benefits": "Asthma, heart." },
    { "name": "Sapota", "category": "fruit", "icon": "fas fa-cookie", "color": "#8b4513", "soil": "Alluvial.", "climate": "Tropical.", "sowing": "June", "harvest": "All year", "tip": "Slow grow.", "nutrients": "Fiber", "benefits": "Energy, bones." },
    { "name": "Jackfruit", "category": "fruit", "icon": "fas fa-certificate", "color": "#006400", "soil": "Deep soil.", "climate": "Humid.", "sowing": "July", "harvest": "Summer", "tip": "Largest fruit.", "nutrients": "Protein", "benefits": "Meat sub, immunity." },
    { "name": "Lemon", "category": "fruit", "icon": "fas fa-lemon", "color": "#ffff00", "soil": "Loam.", "climate": "Sub-tropical.", "sowing": "July", "harvest": "All year", "tip": "Prune.", "nutrients": "Citric Acid", "benefits": "Alkalize, kidney." },
    { "name": "Amla", "category": "fruit", "icon": "fas fa-circle", "color": "#9acd32", "soil": "Alkaline ok.", "climate": "Tropical.", "sowing": "July", "harvest": "Jan", "tip": "Hardy.", "nutrients": "Vit C (High)", "benefits": "Hair, liver." },
    { "name": "Coconut", "category": "fruit", "icon": "fas fa-bowling-ball", "color": "#8b4513", "soil": "Coastal.", "climate": "Tropical.", "sowing": "May", "harvest": "All year", "tip": "Salt tolerant.", "nutrients": "MCT Fats", "benefits": "Hydration, brain." },
    { "name": "Dragon Fruit", "category": "fruit", "icon": "fas fa-fire", "color": "#ff1493", "soil": "Sandy.", "climate": "Tropical.", "sowing": "June", "harvest": "Aug", "tip": "Support cactus.", "nutrients": "Prebiotics", "benefits": "Gut, iron." },

    # --- PULSES ---
    { "name": "Chickpea", "category": "pulse", "icon": "fas fa-cookie", "color": "#f4a460", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Mar", "tip": "Nip tips.", "nutrients": "Protein", "benefits": "Muscle, sugar." },
    { "name": "Pigeon Pea", "category": "pulse", "icon": "fas fa-seedling", "color": "#ffd700", "soil": "Loam.", "climate": "Warm.", "sowing": "June", "harvest": "Jan", "tip": "Drought ok.", "nutrients": "Folic Acid", "benefits": "Energy, heart." },
    { "name": "Green Gram", "category": "pulse", "icon": "fas fa-circle", "color": "#228b22", "soil": "Loam.", "climate": "Warm.", "sowing": "Feb", "harvest": "60 days", "tip": "Short crop.", "nutrients": "Antioxidants", "benefits": "Digestion, cool." },
    { "name": "Black Gram", "category": "pulse", "icon": "fas fa-circle", "color": "#000", "soil": "Clay.", "climate": "Humid.", "sowing": "June", "harvest": "90 days", "tip": "Intercrop.", "nutrients": "Iron", "benefits": "Skin, nerves." },
    { "name": "Lentil", "category": "pulse", "icon": "fas fa-circle", "color": "#fa8072", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Mar", "tip": "Hardy.", "nutrients": "Polyphenols", "benefits": "Heart, cancer." },
    { "name": "Soybean", "category": "pulse", "icon": "fas fa-circle", "color": "#f0e68c", "soil": "Fertile.", "climate": "Warm.", "sowing": "June", "harvest": "Oct", "tip": "Oil+Pulse.", "nutrients": "Omega-3", "benefits": "Bones, menopause." },
    { "name": "Kidney Bean", "category": "pulse", "icon": "fas fa-jedi", "color": "#800000", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Feb", "tip": "Stake.", "nutrients": "Molybdenum", "benefits": "Detox, brain." },
    { "name": "Cowpea", "category": "pulse", "icon": "fas fa-eye", "color": "#fff", "soil": "Sandy.", "climate": "Warm.", "sowing": "Feb", "harvest": "70 days", "tip": "Cover crop.", "nutrients": "Vit A", "benefits": "Vision, bones." },
    { "name": "Horse Gram", "category": "pulse", "icon": "fas fa-horse", "color": "#a52a2a", "soil": "Poor.", "climate": "Dry.", "sowing": "Aug", "harvest": "Dec", "tip": "Kidney stones.", "nutrients": "Calcium", "benefits": "Fat burn, cold." },
    { "name": "Peanut", "category": "pulse", "icon": "fas fa-peanut", "color": "#d2691e", "soil": "Sandy.", "climate": "Warm.", "sowing": "June", "harvest": "Oct", "tip": "Pegging moist.", "nutrients": "Biotin", "benefits": "Brain, skin." },

    # --- SPICES ---
    { "name": "Turmeric", "category": "spice", "icon": "fas fa-vial", "color": "#ffa500", "soil": "Loam.", "climate": "Hot.", "sowing": "May", "harvest": "9 months", "tip": "Boil rhizome.", "nutrients": "Curcumin", "benefits": "Immunity, cancer." },
    { "name": "Black Pepper", "category": "spice", "icon": "fas fa-braille", "color": "#000", "soil": "Laterite.", "climate": "Humid.", "sowing": "June", "harvest": "Dec", "tip": "Support tree.", "nutrients": "Piperine", "benefits": "Digestion, weight." },
    { "name": "Cardamom", "category": "spice", "icon": "fas fa-seedling", "color": "#90ee90", "soil": "Forest.", "climate": "Cool.", "sowing": "Sept", "harvest": "2 years", "tip": "Spice queen.", "nutrients": "Eucalyptol", "benefits": "Breath, BP." },
    { "name": "Cumin", "category": "spice", "icon": "fas fa-seedling", "color": "#8b4513", "soil": "Loam.", "climate": "Dry.", "sowing": "Nov", "harvest": "Feb", "tip": "Wilt sensitive.", "nutrients": "Iron", "benefits": "Anemia, sleep." },
    { "name": "Mustard", "category": "spice", "icon": "fas fa-circle", "color": "#ffff00", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Feb", "tip": "Oilseed too.", "nutrients": "Selenium", "benefits": "Sinus, muscle." },
    { "name": "Fennel", "category": "spice", "icon": "fas fa-leaf", "color": "#32cd32", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Mar", "tip": "Harvest brown.", "nutrients": "Fiber", "benefits": "Bloating, periods." },
    { "name": "Clove", "category": "spice", "icon": "fas fa-thumbtack", "color": "#8b4513", "soil": "Rich.", "climate": "Humid.", "sowing": "June", "harvest": "7 years", "tip": "Flower bud.", "nutrients": "Eugenol", "benefits": "Toothache, liver." },
    { "name": "Cinnamon", "category": "spice", "icon": "fas fa-scroll", "color": "#d2691e", "soil": "Sandy.", "climate": "Tropical.", "sowing": "June", "harvest": "4 years", "tip": "Bark.", "nutrients": "Calcium", "benefits": "Sugar, heart." },
    { "name": "Red Chilli", "category": "spice", "icon": "fas fa-pepper-hot", "color": "#ff0000", "soil": "Black.", "climate": "Warm.", "sowing": "May", "harvest": "Oct", "tip": "Dry it.", "nutrients": "Capsaicin", "benefits": "Pain, sinus." },
    { "name": "Saffron", "category": "spice", "icon": "fas fa-fan", "color": "#ff4500", "soil": "Karewa.", "climate": "Cold.", "sowing": "Aug", "harvest": "Oct", "tip": "Expensive.", "nutrients": "Crocin", "benefits": "Mood, eyes." },

    # --- FLOWERS & CASH ---
    { "name": "Rose", "category": "flower", "icon": "fas fa-fan", "color": "#ff0000", "soil": "Loam.", "climate": "Cool.", "sowing": "Oct", "harvest": "Year round", "tip": "Prune hard.", "nutrients": "Vit C", "benefits": "Stress, skin." },
    { "name": "Marigold", "category": "flower", "icon": "fas fa-sun", "color": "#ffa500", "soil": "Any.", "climate": "Warm.", "sowing": "June", "harvest": "60 days", "tip": "Repels pests.", "nutrients": "Lutein", "benefits": "Eyes, wounds." },
    { "name": "Jasmine", "category": "flower", "icon": "fas fa-star", "color": "#fff", "soil": "Loam.", "climate": "Warm.", "sowing": "June", "harvest": "Summer", "tip": "Prune.", "nutrients": "Antioxidants", "benefits": "Sleep, mood." },
    { "name": "Cotton", "category": "cash", "icon": "fas fa-tshirt", "color": "#fff", "soil": "Black.", "climate": "Hot.", "sowing": "May", "harvest": "Nov", "tip": "White Gold.", "nutrients": "Fiber", "benefits": "Textile, oil." },
    { "name": "Sugarcane", "category": "cash", "icon": "fas fa-candy-cane", "color": "#32cd32", "soil": "Loam.", "climate": "Hot.", "sowing": "Feb", "harvest": "12 mo", "tip": "Water lover.", "nutrients": "Sucrose", "benefits": "Energy, jaundice." },
    { "name": "Tea", "category": "cash", "icon": "fas fa-mug-hot", "color": "#006400", "soil": "Acidic.", "climate": "Cool.", "sowing": "Sept", "harvest": "Years", "tip": "Slopes.", "nutrients": "Theanine", "benefits": "Focus, heart." },
    { "name": "Coffee", "category": "cash", "icon": "fas fa-coffee", "color": "#8b4513", "soil": "Loam.", "climate": "Shade.", "sowing": "Dec", "harvest": "Nov", "tip": "Arabica.", "nutrients": "Caffeine", "benefits": "Focus, liver." },
    { "name": "Jute", "category": "cash", "icon": "fas fa-shopping-bag", "color": "#d2b48c", "soil": "Alluvial.", "climate": "Hot.", "sowing": "Mar", "harvest": "July", "tip": "Golden fiber.", "nutrients": "N/A", "benefits": "Eco bags." },
    { "name": "Bamboo", "category": "cash", "icon": "fas fa-grip-lines-vertical", "color": "#006400", "soil": "Any.", "climate": "Tropical.", "sowing": "June", "harvest": "3 years", "tip": "Fast grass.", "nutrients": "Silica", "benefits": "Paper, food." },
    { "name": "Sesame", "category": "oil", "icon": "fas fa-cookie", "color": "#f5f5dc", "soil": "Loam.", "climate": "Warm.", "sowing": "June", "harvest": "Sept", "tip": "Oil queen.", "nutrients": "Calcium", "benefits": "Bones, hair." }
]

def render_guide():
    cards_html = ""
    for crop in GUIDE_DATA:
        cid = crop['name'].replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
        
        cards_html += f"""
        <div class="crop-card" data-category="{crop['category']}" data-name="{crop['name'].lower()}">
            <div class="card-header" onclick="toggleCard('{cid}')">
                <div class="icon-box" style="color:{crop['color']};">
                    <i class="{crop['icon']}"></i>
                </div>
                <div class="header-text">
                    <h3>{crop['name']}</h3>
                    <span class="badge {crop['category']}">{crop['category'].upper()}</span>
                </div>
            </div>
            
            <div class="card-body" id="body-{cid}">
                <div class="details-grid">
                    <div class="detail-item"><i class="fas fa-layer-group"></i> <span>{crop['soil']}</span></div>
                    <div class="detail-item"><i class="fas fa-cloud-sun"></i> <span>{crop['climate']}</span></div>
                    <div class="detail-item"><i class="fas fa-calendar-alt"></i> <span>{crop['sowing']}</span></div>
                    <div class="detail-item"><i class="fas fa-sickle"></i> <span>{crop['harvest']}</span></div>
                </div>
                
                <div class="health-box">
                    <div class="benefit"><i class="fas fa-heartbeat"></i> {crop['benefits']}</div>
                    <div class="nutrient"><i class="fas fa-capsules"></i> {crop['nutrients']}</div>
                </div>

                <div class="pro-tip">
                    <i class="fas fa-lightbulb"></i> <strong>Pro Tip:</strong> {crop['tip']}
                </div>
            </div>
        </div>
        """

    return f"""
    {get_header("Agricultural Encyclopedia")}
    {get_navbar(back_link="/")}

    <style>
        /* 1. SOFT ORGANIC BACKGROUND */
        body {{
            background: linear-gradient(to bottom right, #e0f7fa, #e8f5e9, #fdfbf7);
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
            min-height: 100vh;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; padding-bottom: 80px; }}
        
        /* 2. GLASS SEARCH BAR */
        .search-area {{
            position: sticky; top: 80px; z-index: 100;
            background: rgba(255,255,255,0.85);
            backdrop-filter: blur(15px);
            padding: 20px; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-bottom: 40px;
            border: 1px solid rgba(255,255,255,0.5);
        }}
        
        .search-input {{
            width: 100%; padding: 15px 20px; border-radius: 50px;
            border: 2px solid rgba(25, 135, 84, 0.2); font-size: 1rem; outline: none;
            transition: 0.3s; padding-left: 45px;
            background: white url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="%23198754" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>') no-repeat 15px center;
        }}
        .search-input:focus {{ border-color: #198754; box-shadow: 0 0 15px rgba(25, 135, 84, 0.2); }}

        .filter-chips {{ display: flex; gap: 12px; margin-top: 15px; overflow-x: auto; padding-bottom: 5px; scrollbar-width: none; }}
        .chip {{
            padding: 10px 20px; border-radius: 30px; font-size: 0.9rem;
            cursor: pointer; border: 1px solid rgba(0,0,0,0.1); 
            background: rgba(255,255,255,0.9); color: #555;
            transition: 0.3s; white-space: nowrap; font-weight: 600;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .chip:hover {{ transform: translateY(-3px); background: white; }}
        .chip.active {{ background: linear-gradient(135deg, #198754, #20c997); color: white; border-color: transparent; box-shadow: 0 5px 15px rgba(32, 201, 151, 0.4); }}

        /* 3. GRID LAYOUT FOR CARDS */
        .crop-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
        }}

        /* 4. FLOATING CARD DESIGN */
        .crop-card {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.03);
            border: 1px solid rgba(255,255,255,0.6);
            overflow: hidden; transition: all 0.4s ease;
            position: relative;
        }}
        .crop-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); background: white; }}

        .card-header {{
            padding: 20px; display: flex; align-items: center; gap: 15px;
            cursor: pointer;
        }}
        .icon-box {{
            width: 55px; height: 55px;
            background: #f8f9fa; border-radius: 15px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.8rem; box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        }}
        .header-text h3 {{ margin: 0; font-size: 1.2rem; color: #333; }}
        
        .badge {{ 
            font-size: 0.75rem; padding: 4px 10px; border-radius: 6px; 
            font-weight: 700; display: inline-block; margin-top: 5px; letter-spacing: 0.5px;
        }}
        /* Pastel Badge Colors */
        .badge.grain {{ background: #fff8e1; color: #fec107; }}
        .badge.veg {{ background: #e8f5e9; color: #2e7d32; }}
        .badge.fruit {{ background: #fce4ec; color: #d81b60; }}
        .badge.cash {{ background: #e0f7fa; color: #0097a7; }}
        .badge.pulse {{ background: #eceff1; color: #546e7a; }}
        .badge.spice {{ background: #fbe9e7; color: #d84315; }}
        .badge.flower {{ background: #f3e5f5; color: #8e24aa; }}
        .badge.oil {{ background: #fff3e0; color: #ef6c00; }}

        /* 5. EXPANDABLE BODY */
        .card-body {{
            max-height: 0; overflow: hidden; transition: max-height 0.5s cubic-bezier(0, 1, 0, 1);
            background: rgba(255,255,255,0.5);
        }}
        .open .card-body {{ max-height: 600px; transition: max-height 0.5s ease-in-out; }}

        .details-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 20px;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }}
        .detail-item {{ font-size: 0.9rem; color: #666; display: flex; align-items: center; gap: 8px; }}
        .detail-item i {{ color: #198754; opacity: 0.8; }}

        .health-box {{ padding: 20px; display: flex; flex-direction: column; gap: 10px; }}
        .benefit {{ font-size: 0.9rem; color: #d63384; display: flex; align-items: center; gap: 8px; }}
        .nutrient {{ font-size: 0.9rem; color: #0d6efd; display: flex; align-items: center; gap: 8px; }}

        .pro-tip {{
            margin: 0 20px 20px 20px; background: #fffde7; color: #fbc02d;
            padding: 12px; border-radius: 12px; font-size: 0.9rem;
            border: 1px dashed #fbc02d;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .crop-grid {{ grid-template-columns: 1fr; }}
            .search-area {{ top: 70px; padding: 15px; }}
        }}
    </style>

    <div class="container">
        <div style="text-align:center; margin: 30px 0;">
            <h1 style="color:#198754; font-weight:800; font-size: 2.5rem; text-shadow: 2px 2px 0 white;">Agricultural Encyclopedia</h1>
            <p style="color:#666; font-size: 1.1rem;">Explore farming techniques & health benefits for 100+ crops.</p>
        </div>

        <div class="search-area">
            <input type="text" id="searchInput" class="search-input" placeholder="Search crops, nutrients, or benefits..." onkeyup="filterCrops()">
            
            <div class="filter-chips">
                <div class="chip active" onclick="setFilter('all', this)">All</div>
                <div class="chip" onclick="setFilter('fruit', this)">🍎 Fruits</div>
                <div class="chip" onclick="setFilter('veg', this)">🥕 Veggies</div>
                <div class="chip" onclick="setFilter('grain', this)">🌾 Grains</div>
                <div class="chip" onclick="setFilter('pulse', this)">🥣 Pulses</div>
                <div class="chip" onclick="setFilter('spice', this)">🌶️ Spices</div>
                <div class="chip" onclick="setFilter('flower', this)">🌻 Flowers</div>
                <div class="chip" onclick="setFilter('cash', this)">💰 Cash</div>
                <div class="chip" onclick="setFilter('oil', this)">🛢️ Oilseeds</div>
            </div>
        </div>

        <div id="cropList" class="crop-grid">
            {cards_html}
        </div>
        
        <div id="noResult" style="text-align:center; padding:50px; color:#aaa; display:none;">
            <i class="fas fa-seedling" style="font-size:3rem; margin-bottom:15px; opacity:0.5;"></i><br>
            No crops found matching your search.
        </div>
    </div>

    <script>
        let currentCategory = 'all';

        function toggleCard(id) {{
            const body = document.getElementById('body-' + id);
            const parent = body.parentElement;
            
            // Close others (Optional: makes it cleaner)
            // document.querySelectorAll('.crop-card').forEach(c => c.classList.remove('open'));
            
            parent.classList.toggle('open');
        }}

        function setFilter(cat, btn) {{
            currentCategory = cat;
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            filterCrops();
        }}

        function filterCrops() {{
            const search = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.crop-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const name = card.getAttribute('data-name');
                const cat = card.getAttribute('data-category');
                
                // Search logic (Checks Name OR Category)
                const matchesSearch = name.includes(search);
                const matchesCat = (currentCategory === 'all') || (cat === currentCategory);

                if (matchesSearch && matchesCat) {{
                    card.style.display = "block";
                    visibleCount++;
                }} else {{
                    card.style.display = "none";
                }}
            }});

            document.getElementById('noResult').style.display = (visibleCount === 0) ? "block" : "none";
        }}
    </script>
    </body></html>
    """