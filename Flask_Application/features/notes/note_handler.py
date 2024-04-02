import json
import time
from langchain.vectorstores import pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import retrieval_qa
from langchain_community.vectorstores import PineconeVectorStore  
from pinecone import Pinecone

openai_api_key ="" #os.getenv("OPENAI_API_KEY")
pinecone_api_key = "" #os.getenv("PINECONE_API_KEY")

with open('main.json', 'r') as file:
    data = json.load(file)
    
pinecone_index_name = data.get('pinecone_index_name', 'None')
llm_model_name = data.get('llm_model_name', 'gpt-3.5-turbo')


def get_note(voice_input):
    pc = Pinecone(api_key=pinecone_api_key)
    index_name = pinecone_index_name
    
    existing_indexes = [
        index_info["name"] for index_info in pc.list_indexes()
    ]   
    
    if index_name not in existing_indexes:
        spec = pinecone.IndexSpec() #TODO
        pc.create_index(
            index_name,
            dimension=1536,  # TODO dimensionality of ada 002
            metric='dotproduct',
            spec=spec
        )
    
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    
    index = pc.Index(index_name)
    
    embed_model_name = 'text-embedding-ada-002'  # TODO
    
    embeddings = OpenAIEmbeddings(  
        model=embed_model_name,  
        openai_api_key = openai_api_key,
    )  
    
    llm = ChatOpenAI(  
        openai_api_key=openai_api_key,  
        model_name=llm_model_name,  
        temperature=0.0  
    ) 
    
    
    text_field = "text"  
    vectorstore = PineconeVectorStore(  
        index, embeddings, text_field  
    ) 
    
    qa = retrieval_qa.from_chain_type(  
        llm=llm,  
        chain_type="stuff",  
        retriever=vectorstore.as_retriever()  
    )  
    qa.run(voice_input)
    


def create_note(voice_input):
    #TODO
    pass