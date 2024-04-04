import json
from openai import OpenAI
from googleapiclient.discovery import build

open_ai_key ="" #os.getenv("OPENAI_API_KEY")
with open('main.json', 'r') as file:
  data = json.load(file)

llm_model_name = data.get('llm_model_name', 'gpt-3.5-turbo')
    
def create_contact(voice_input, creds):
  data = get_contact_obj(voice_input)
  service = build('people', 'v1', credentials=creds)
  
  try: 
    contact = service.people().createContact(body=data).execute()
    contact = f"Contact : {data['names'][0]['givenName']},\n Number : {data['numbers'][0]['value']},\n"
    return contact
  except Exception as error:
      print(f"An error occurred: {error}")
      return f"An error occurred: {error}"

def get_contact_obj(voice_input):
  client = OpenAI(
    api_key=open_ai_key
  )
  
  query = "The transcripted voice recording is: "+ voice_input + \
      "Based on the transcripted voice recording, fill in the JSON format specified" \
      "Return the JSON format specified, do not return anything else."

  functions = [
    {
      "name": "add_contact",
      "description": "Creates a new contact in the contact list",
      "parameters": {
        "type": "object",
        "properties": {
          "given_name": {
            "type": "string",
            "description": "name of the person"
          },
          "phone_number": {
            "type": "string",
            "description": "The phone number of the person"
          },
        },
        "required": ["given_name", "phone_number"]
      }
    },
  ]

  completion = client.chat.completions.create(
    model=llm_model_name,
    messages=[
      {"role": "user", "content": query}
      ],
    functions=functions,
    stream=False,
  )

  data = json.loads(completion.choices[0].message.function_call.arguments)
  data = get_google_contact_obj(data)
  return data
    
def get_google_contact_obj(data):
  contact = {
    "names": [
      {
        "givenName": data['given_name']
      }
    ],
    "phoneNumbers": [
      {
        "value": data['phone_number']
      }
    ]
  }
  return contact