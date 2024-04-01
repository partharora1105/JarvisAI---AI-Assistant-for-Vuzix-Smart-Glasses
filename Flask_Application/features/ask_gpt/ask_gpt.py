from openai import OpenAI

open_ai_key ="" #os.getenv("OPENAI_API_KEY")

def ask_gpt(voice_input):
  #TODO parse through memory vector db to see if there is a match
  client = OpenAI(
    api_key=open_ai_key
  ) 
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant Jarvis who responds in less than 20 words"},
    {"role": "user", "content": voice_input}
    ]
  ) 
  return completion.choices[0].message.content  