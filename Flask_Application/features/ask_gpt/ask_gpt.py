from openai import OpenAI
import json

open_ai_key ="" #os.getenv("OPENAI_API_KEY")

with open('main.json', 'r') as file:
  data = json.load(file)

llm_model_name = data.get('llm_model_name', 'gpt-3.5-turbo')

def ask_gpt(voice_input):
  #TODO see if this is necessary
  client = OpenAI(
    api_key=open_ai_key
  ) 
  completion = client.chat.completions.create(
  model=llm_model_name,
  messages=[
    {"role": "system", "content": "You are a helpful assistant Jarvis who responds in less than 20 words"},
    {"role": "user", "content": voice_input}
    ]
  ) 
  return completion.choices[0].message.content  