import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from flask import Flask

from features.ask_gpt.ask_gpt import ask_gpt
from features.calendar.calendar_handler import create_calander_event, get_calendar_event
from features.contact.contact_handler import create_contact
from features.notes.note_handler import create_note, get_note
from features.remember.remember import store_to_db


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
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/drive"
    "openid"
]

with open('main.json', 'r') as file:
    data = json.load(file)

credentials_path = PATH + data.get('credentials_path', 'None')   
token_path = PATH + data.get('token_path', 'None')

#TODO store & get folder URL in a seperate db based on the user
gdrive_folder_url = data.get('gdrive_folder_url', 'None')
def extract_folder_id(url):
    parts = url.split('/')
    if "folders" in parts:
        folder_id_index = parts.index("folders") + 1
        if folder_id_index < len(parts):
            return parts[folder_id_index]
    return None

folder_id = extract_folder_id(gdrive_folder_url)


@app.route('/')
def hello_world():
    return 'Jarvis says Hello World!'


#"https://ccghwd.pythonanywhere.com/everyday/wear/rest/api/speech/output/<prefix>/<auth_code>/<voice_input>"
@app.route("/everyday/wear/rest/api/speech/output/<prefix>/<auth_code>/<voice_input>")
def analyze_command(prefix, auth_code, voice_input):
    # TODO manual parsing vs llm to decide which function to call
    # TODO pass llm_model_name & pinecone_index_name to functions
    try:
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
        elif "create contact" in voice_input.lower():
            output = create_contact(voice_input)
        elif "remember" in voice_input.lower():
            output = store_to_db(voice_input)
        else:
            output = ask_gpt(voice_input)
        
        return output
    except Exception as e:
        return str(e)

#TODO create route for parse_gdrive_folder(folder_id, pinecone_index_name, llm_model_name)

def get_creds_from_auth_code(auth_code=None):
    credentials = None

    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        elif auth_code:
            flow = Flow.from_client_secrets_file(
                credentials_path,
                scopes=SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # This redirect URI is used for apps that do not have a web server
            )
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            
            with open(token_path, 'w') as token:
                token.write(credentials.to_json())
        else:
            raise Exception("No valid authorization code or refresh token available.")

    return credentials

if DOMAIN != publicDomain:
    if __name__ == '__main__':
        app.debug = True
        app.run()

