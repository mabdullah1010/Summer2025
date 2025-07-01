#pip install -q -U google-genai 
GEMINI_API_KEY = "AIzaSyDLiHM65fnVCyIGzdoCp6V0bEmohvOJRsE"


import google.generativeai as genai


# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

# Use a generative model
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Summarize this text: ...")

print(response.text)
