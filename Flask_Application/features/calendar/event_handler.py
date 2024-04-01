from datetime import datetime
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openai import OpenAI

open_ai_key ="" #os.getenv("OPENAI_API_KEY")


def get_calendar_event(voice_input, creds):
  data = get_desired_date_obj(voice_input)

  start_year = data['start_year']
  start_month = data['start_month']
  start_day = data['start_day']
  start_time = data['start_time']

  end_year = data['start_year']
  end_month = data['start_month']
  end_day = data['start_day']
  end_time = data['start_time']

  start_timestamp = datetime(start_year, start_month, start_day, start_time).isoformat()
  end_timestamp = datetime(end_year, end_month, end_day, end_time).isoformat()
  output = f"Schedule for {start_timestamp}"

  try:
      service = build("calendar", "v3", credentials=creds)
      events_result = service.events().list(calendarId='primary', timeMin=start_timestamp, maxResults = 10, singleEvents=True, orderBy='startTime').execute()
      events = events_result.get('items', [])

      if not events:
          return "No events found within the specified time range."

      event_list = []
      for event in events:
          start = event['start'].get('dateTime', event['start'].get('date'))
          summary = event['summary']
          event_list.append(f"Event: {summary},\nWhen: {start}\n")

      output += "\n".join(event_list)
  except Exception as error:
      print(f"An error occurred: {error}")
      return f"An error occurred: {error}"
      
  return output


def create_calander_event(voice_input, creds):
  data = get_desired_date_obj(voice_input)

  start_year = data['start_year']
  start_month = data['start_month']
  start_day = data['start_day']
  start_time = data['start_time']

  end_year = data['start_year']
  end_month = data['start_month']
  end_day = data['start_day']
  end_time = data['start_time']

  start_timestamp = datetime(start_year, start_month, start_day, start_time).isoformat()
  end_timestamp = datetime(end_year, end_month, end_day, end_time).isoformat()

  try:
    service = build("calendar", "v3", credentials=creds)
    event = {
      'summary': data['name'],
      'description': data['event_description'],
      'start': {
          'dateTime': start_timestamp,
          'timeZone': 'America/New_York',
      },
      'end': {
          'dateTime': end_timestamp,
          'timeZone': 'America/New_York',
      },
      'attendees': [
          {'email': 'xxxxx@gmail.com'},
      ],
      }
    event = service.events().insert(calendarId='primary', body=event).execute()
    event = f"Event : {data['name']},\n When : {start_timestamp},\n"
    return event
  except HttpError as error:
    print(f"An error occurred: {error}")
    return f"An error occurred: {error}"
  
def get_desired_date_obj(voice_input):
    client = OpenAI(
      api_key=open_ai_key
    )
    
    mic_record = voice_input
    now = datetime.now()
    curr_details = now.strftime("%H:%M:%S %Y-%m-%d %A")
    query = "The date & time now is"+ curr_details + \
        "and the transcripted voice recording is: "+ mic_record + \
        "Based on the current date & time as well as the transcripted voice recording, fill in the JSON format specified" \
        "Return the JSON format specified, do not return anything else."

    functions = [
      {
        "name": "add_event",
        "description": "Adds a new event to the calendar",
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