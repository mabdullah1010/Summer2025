import os
import time
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=OPEN_API_KEY)

OPENAI_MODEL = "gpt-4.1"

themes = [
    "Pace, Content Coverage and In-Class Practice",
    "Workload, Stress and Well-being",
    "Assignments and Grading",
    "Confidence and Support Needs",
    "Technical Difficulties",
    "Appreciation and Classroom Environment",
    "Other",
    "NA"
]

csv_path = "COM212_q4_emotions.csv"
column_name = "clean"  
df = pd.read_csv(csv_path)

def classify_theme(response_text):
    if pd.isna(response_text) or response_text.strip() == "":
        return "No response"
    
    prompt = f"""You are a helpful assistant. Classify the following student feedback into ONE of the given themes below. 
Respond with the exact name of the most appropriate theme from this list:

{themes}

Feedback: \"{response_text}\"
Theme:"""
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You classify short feedback into appropriate course-related themes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error:", e)
        return "API Error"

classified_themes = []
for i, response in enumerate(df[column_name]):
    print(f"Classifying row {i+1}/{len(df)}...")
    theme = classify_theme(response)
    classified_themes.append(theme)
    time.sleep(1.5)  

df["theme"] = classified_themes
df.to_csv(f"{csv_path}", index=False)
print(f"Classification complete and saved to '{csv_path}'")
