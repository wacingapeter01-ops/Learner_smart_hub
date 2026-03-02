import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def ask_gemini(prompt):
    # UPDATED to the model your key actually supports:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("Connecting to the Brain...")
    try:
        # Final test with the correct model
        result = ask_gemini("Confirm system status for HP 840 G2.")
        print(f"AI Response: {result}")
    except Exception as e:
        print(f"Error: {e}")