import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"First few characters of API key: {api_key[:7]}...")
    print(f"Length of API key: {len(api_key)}")
