#TODO use the phrase "keyword" to search for the exact word in all the notes

# remember to set the environment variables & port on the langchain impl of get_creds

import json
import time
import os
from pinecone import Pinecone, PodSpec

from langchain_community.document_loaders import googledrive
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import Tool
from langchain.agents import initialize_agent

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


def parse_gdrive_folder(folder_id, pinecone_index_name, llm_model_name, openai_api_key, pinecone_api_key):
    # pc = Pinecone(api_key=pinecone_api_key)
    # index_name = pinecone_index_name
    
    # existing_indexes = [
    #     index_info["name"] for index_info in pc.list_indexes()
    # ]   
    
    # if index_name not in existing_indexes:
    #     spec = PodSpec(
    #     )

    #     pc.create_index(
    #         index_name,
    #         dimension=1536,  # TODO dimensionality of ada 002
    #         metric='dotproduct',
    #         spec=spec
    #     )
    
    #     while not pc.describe_index(index_name).status['ready']:
    #         time.sleep(1)
    
    # index = pc.Index(index_name)

    loader = googledrive.GoogleDriveLoader(
        folder_id=folder_id,
        recursive=True,
        credentials_path=".credentials/credential.json",
        token_path=".credentials/token.json"
    )

    docs = loader.load()
    
    embed_model_name = 'text-embedding-ada-002'  # TODO
    
    embeddings = OpenAIEmbeddings(  
        model=embed_model_name,  
        openai_api_key = openai_api_key,
    )

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name=llm_model_name,
        chunk_size=100,
        chunk_overlap=0,
    )

    texts = text_splitter.split_documents(docs)
    vectorstore = PineconeVectorStore.from_documents(documents=texts, embedding=embeddings, index_name= pinecone_index_name) # this only works for the first time
    
    #TODO move this to a separate file called ask_question.py
    # llm = ChatOpenAI(  
    #     openai_api_key=openai_api_key,  
    #     model_name=llm_model_name,  
    #     temperature=0.0  
    # )

    # conversational_memory = ConversationBufferWindowMemory(
    #     memory_key='chat_history',
    #     k=5, # TODO modify this
    #     return_messages=True
    # )

    # qa = RetrievalQA.from_chain_typ(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectorstore.as_retriever()
    # )

    # tools = [
    #     Tool(
    #         name='Knowledge Base',
    #         func=qa.run,
    #         description=(
    #             'use this tool when answering general knowledge queries to get '
    #             'more information about the topic'
    #         )
    #     )
    # ]

    # agent = initialize_agent(
    #     agent='chat-conversational-react-description',
    #     tools=tools,
    #     llm=llm,
    #     verbose=True,
    #     max_iterations=3,
    #     early_stopping_method='generate',
    #     memory=conversational_memory
    # )

    # agent(voice_input)
    
parse_gdrive_folder("15pM3XrA7dfoS5Tekkk9-vtAmiDjZ5fBA", "test" , "gpt-3.5-turbo", openai_api_key, pinecone_api_key)
print("done")