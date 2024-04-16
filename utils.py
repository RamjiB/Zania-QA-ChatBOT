import requests
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import os
from constants import (
    DOCUMENT_CHUNK_SIZE, 
    DOCUMENT_OVERLAP_SIZE, 
    RETRIVER_SEARCH_TYPE, 
    RETRIVER_SEARCH_VALUE_K,
    CHAIN_TYPE
)

def download_file(url, save_path="file.pdf"):
    """Downlload the file uploaded in Slack, to Embed and store in Chorma DB

    Args:
        url: Provate URL for file from SLACK
        save_path: Defaults to "file.pdf".

    Returns:
       download status code and message
    """
    # Send a GET request to the URL
    response = requests.get(url, headers={'Authorization': 'Bearer %s' % os.environ.get("SLACK_BOT_TOKEN")})
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the file in binary write mode and write the content from the response
        with open(save_path, 'wb+') as file:
            file.write(bytearray(response.content))
        return 200, "File downloaded successfully."
    else:
        return 400, f"Failed to download file. Status code: {response.status_code}"


def llm_chatbot_response(query, download_status, message):
    """Preprocess the document, store embeeddings in chromadb and return the response.

    Args:
        query: user query
        download_status: document_download status code
        message: document_download message

    Returns:
        A string on failure or output json on success
    """
    questions = query.split("\n")

    if download_status == 400 and not os.path.exists("file.pdf"):
        return message
    try:
        # load document
        loader = PyPDFLoader("file.pdf")
        documents = loader.load()
        # split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=DOCUMENT_CHUNK_SIZE, chunk_overlap=DOCUMENT_OVERLAP_SIZE)
        texts = text_splitter.split_documents(documents)
        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        # create the vectorestore to use as the index
        db = Chroma.from_documents(texts, embeddings)
        # expose this index in a retriever interface
        retriever = db.as_retriever(search_type=RETRIVER_SEARCH_TYPE, search_kwargs={"k":RETRIVER_SEARCH_VALUE_K})
        # create a chain to answer questions 
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name=os.environ.get("GPT_MODEL_NAME")), 
            chain_type=CHAIN_TYPE, 
            retriever=retriever, 
            return_source_documents=True)
    except Exception as exce:
        return f"Failed in data preprocessing: {exce}"
    
    final_output = {}
    for question in questions:
        if question.strip() != "":
            output = qa({"query": f'{question}, If you could not find the answer send response as "Data not available""'})
            final_output[question] = output["result"]
    return final_output