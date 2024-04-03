import requests
from openai import OpenAI

open_ai_key ="" #os.getenv("OPENAI_API_KEY")
    
def create_contact(voice_input, creds):
  data = get_contact_obj(voice_input)
  
  
  
def get_contact_obj(voice_input):
    client = OpenAI(
      api_key=open_ai_key
    )
    
    query = "The transcripted voice recording is: "+ voice_input + \
        "Based on the transcripted voice recording, fill in the JSON format specified" \
        "Return the JSON format specified, do not return anything else."

    functions = [
      {
        "name": "add_contactt",
        "description": "Adds a new contact to the contact list",
        "parameters": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "name of the event"
            },
            "event_description": {
              "type": "string",
              "description": "The description of the event"
            },
            "start_year": {
              "type": "integer",
              "description": "The year in which the event starts"
            },
            "end_year": {
              "type": "integer",
              "description": "The year in which the event ends"
            },
            "start_month": {
              "type": "integer",
              "description": "The month in which the event start"
            },
            "end_month": {
              "type": "integer",
              "description": "The month in which the event ends"
            },
            "start_day": {
              "type": "integer",
              "description": "The day in which the event starts"
            },
            "end_day": {
              "type": "integer",
              "description": "The day in which the event ends"
            },
            "start_time": {
              "type": "integer",
              "description": "The start time in 24hr format"
            },
            "end_time": {
              "type": "integer",
              "description": "The end time in 24hr format. If no time is specified, the end time should be one hour after the start"
            }
          },
          "required": ["name", "event_description", "start_year", "start_month", "start_day", "start_time", "end_year", "end_month", "end_day", "end_time"]
        }
      },
    ]

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo-0613",
      messages=[
        {"role": "user", "content": query}
        ],
      functions=functions,
      stream=False,
    )

    data = json.loads(completion.choices[0].message.function_call.arguments)
    return data
    
    