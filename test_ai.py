import google.generativeai as genai

# PASTE YOUR KEY HERE
KEY = "AIzaSyBjyoKI3gyigMLOUWnVZGfhgY72MH2or_w"

genai.configure(api_key=KEY)

print("Checking available models for your Key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
except Exception as e:
    print(f"Error: {e}")