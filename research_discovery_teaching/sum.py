import google.generativeai as genai
import pandas as pd
import os
import time

GEMINI_API_KEY = os.getenv(GEMINI_API_KEY)


import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(prompt_text, max_retries=3, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            print(f"Sending prompt to Gemini (Attempt {attempt + 1}/{max_retries})...")
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                print("Max retries reached. Skipping this item.")
                return f"ERROR: Could not get response - {e}"

def process_csv_with_gemini():
    csv_file_path = "COM212_question4_file.csv"
    # COM214_question4_file.csv
    input_column_name = "question_response"
    output_column_name = "summary"

    try:
        df = pd.read_csv(csv_file_path)
        print(f"Successfully loaded '{csv_file_path}'.")
        print(f"Columns found: {df.columns.tolist()}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if input_column_name not in df.columns:
        print(f"Error: Input column '{input_column_name}' not found in the CSV.")
        print(f"Available columns are: {df.columns.tolist()}")
        return
    df[output_column_name] = ""
    print("\nStarting Gemini API processing...")
    for index, row in df.iterrows():
        column_value = str(row[input_column_name])
        full_prompt = f"""You are analyzing classroom feedback data.

        Summarize the following student's response in a concise sentence of 5–40 words. 
        Preserve the first-person voice and tone (e.g., "I think...", "I feel...", etc.). 
        Keep the summary faithful to the original intent. Make summary is meaningful.

        If the response is blank, meaningless, or not understandable, just return: NA

        Student response: {column_value}"""

        print(f"\nProcessing row {index + 1}: Value = '{column_value}'")
        print(f"Full prompt: '{full_prompt}'")

        gemini_response = get_gemini_response(full_prompt)
        df.at[index, output_column_name] = gemini_response
        print(f"Gemini response recorded for '{column_value}'.")
        time.sleep(0.5) #delay for hit rate

    base_name, ext = os.path.splitext(csv_file_path)
    output_csv_file_path = f"{base_name}_gemini_processed{ext}"

    try:
        df.to_csv(output_csv_file_path, index=False)
        print(f"\nProcessing complete! Modified data saved to '{output_csv_file_path}'")
    except Exception as e:
        print(f"Error saving output CSV file: {e}")


process_csv_with_gemini()