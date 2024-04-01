from features.ask_gpt.ask_gpt import ask_gpt
from features.calendar.event_handler import create_calander_event, get_calendar_event
from features.notes.note_handler import create_note, get_note
from features.remember.remember import remember, store_to_db
from flask import Flask


import os



from openai import OpenAI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow


from flask import Flask, jsonify
from google.oauth2 import service_account
import googleapiclient.discovery




app = Flask(__name__, static_folder="static")
localDomain = "http://localhost:5000"
publicDomain = "https://ccghwd.pythonanywhere.com/"
DOMAIN = localDomain

localPath = ""
publicPath = "/home/ccgHwd/mysite/"
PATH = localPath

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

credentials_path = PATH + "static/credential.json"
token_path = PATH + "static/token.json"



@app.route('/')
def hello_world():
    return 'Jarvis says Hello World!'


#"https://ccghwd.pythonanywhere.com/everyday/wear/rest/api/speech/output/<prefix>/<auth_code>/<voice_input>"
@app.route("/everyday/wear/rest/api/speech/output/<prefix>/<auth_code>/<voice_input>")
def analyze_command(prefix, auth_code, voice_input):
    # TODO manual parsing vs llm to decide which function to call
    
    auth_code = f"{prefix}/{auth_code}"
    creds = get_creds_from_auth_code(auth_code)

    if "event" in voice_input.lower():
       output = get_calendar_event(voice_input, creds)
    elif "schedule" in voice_input.lower():
       output = create_calander_event(voice_input, creds)
    elif "get note" in voice_input.lower():
       output = get_note(voice_input)
    elif "create note" in voice_input.lower():
       output = create_note(voice_input)
    elif "remember" in voice_input.lower():
       output = store_to_db(voice_input)
    else:
       output = ask_gpt(voice_input)
    
    return output


def get_creds_from_auth_code(auth_code):
  flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # This redirect URI is used for apps that do not have a web server
  )
  flow.fetch_token(code=auth_code)
  credentials = flow.credentials
  return credentials

if DOMAIN != publicDomain:
    if __name__ == '__main__':
        app.debug = True
        app.run()

