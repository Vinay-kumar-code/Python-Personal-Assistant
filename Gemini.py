import google.generativeai as genai

genai.configure(api_key="api_key")
a=input("Type your prompt:- ")
model = genai.GenerativeModel("gemini-2.0-flash-exp")
response = model.generate_content(a)
print(response.text)
