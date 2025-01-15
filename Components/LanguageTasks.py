import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API'))

def GetHighlight(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in identifying the most engaging part of a video transcript. Your task is to return the start and end timestamps of the most interesting segment."
                },
                {
                    "role": "user",
                    "content": f"From this transcript, identify the most engaging 15-30 second segment and return ONLY the start and end timestamps in the format 'start_time end_time'. Here's the transcript:\n\n{text}"
                }
            ]
        )
        
        # Extract timestamps from response
        result = response.choices[0].message.content.strip()
        try:
            start_time, end_time = map(float, result.split())
            return start_time, end_time
        except Exception as e:
            print(f"Error parsing timestamps: {str(e)}")
            return 0, 0
            
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return 0, 0