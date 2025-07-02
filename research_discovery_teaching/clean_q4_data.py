from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
# Initialize client
client = OpenAI(api_key=OPEN_API_KEY)
# Choose model
OPENAI_MODEL = "gpt-4.1"  


def get_openai_response(prompt_text, max_retries=3, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            print(f"Sending prompt to OpenAI (Attempt {attempt + 1}/{max_retries})...")
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for summarizing student feedback."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                print("Max retries reached. Skipping this item.")
                return f"ERROR: Could not get response - {e}"

def process_csv_with_openai():
    csv_file_path = "COM212_question4_file.csv"
    input_column_name = "question_response"
    output_column_name = "clean_q4"

    try:
        df = pd.read_csv(csv_file_path)
        print(f"Successfully loaded '{csv_file_path}'.")
        print(f"Columns found: {df.columns.tolist()}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_file_path}'. Please check path.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if input_column_name not in df.columns:
        print(f"Error: Input column '{input_column_name}' not found in the CSV.")
        print(f"Available columns are: {df.columns.tolist()}")
        return

    df[output_column_name] = ""
    print("\nStarting OpenAI API processing...")

    for index, row in df.iterrows():
        column_value = str(row[input_column_name])
        full_prompt = f"""You are analyzing student reponses to the following question: Anything that I should know about or do to make you more comfortable and able to succeed in this course? (challenges, ideas for improvement, issues outside of class, etc.)
        Now I want you to just return NA if the student response is not relevant or useful to the question, otherwise return the response as it is without changing anything. Keep in mind that one class was help outside and students were very happy so don't ignore that.

        Student response: {column_value}"""

        print(f"\nProcessing row {index + 1}: Value = '{column_value}'")
        print(f"Full prompt: '{full_prompt}'")

        openai_response = get_openai_response(full_prompt)
        df.at[index, output_column_name] = openai_response
        print(f"OpenAI response recorded for '{column_value}'.")
        time.sleep(1)  # delay to respect rate limits

    base_name, ext = os.path.splitext(csv_file_path)
    output_csv_file_path = f"{csv_file_path}_cleaned{ext}"

    try:
        df.to_csv(output_csv_file_path, index=False)
        print(f"\nProcessing complete! Modified data saved to '{output_csv_file_path}'")
    except Exception as e:
        print(f"Error saving output CSV file: {e}")

process_csv_with_openai()
