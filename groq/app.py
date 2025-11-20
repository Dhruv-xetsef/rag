import streamlit as st
import os
#api access of groq play ground creat api
from langchain_groq import ChatGroq 
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
load_dotenv()
##load the groq apikey
groq_api_key = os.environ["GROQ_API_KEY"]
if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model = )
    st.sessio_state.laader


