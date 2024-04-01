from openai import OpenAI
import json
from langchain_community.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import pinecone

open_ai_key ="" #os.getenv("OPENAI_API_KEY")

def get_note(voice_input, token_path, folder_id):
    loader = GoogleDriveLoader(
        folder_id,
        token_path,
        recursive=True,
    )
    
    docs = loader.load()
    
        
    
    
    


def create_note(voice_input):
    #TODO
    pass