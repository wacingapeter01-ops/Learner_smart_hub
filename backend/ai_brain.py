from google import genai
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def ask_gemini(prompt):
    # CHANGED: 1.5-flash is the most stable and light for your hardware
    model = genai.GenerativeModel('gemini-1.5-flash') 
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("Connecting to the Brain...")
    try:
        # Simple test to see if the connection is alive
        result = ask_gemini("Say: System Online")
        print(f"AI Response: {result}")
    except Exception as e:
        print(f"Error: {e}")