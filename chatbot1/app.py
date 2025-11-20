# from langchain_openai import ChatOPenAi
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output.parsers import StrOutputParser# this is default output parser we can also create our custom output parser like if we want the results isto the all caps and all kind of things can be doen

# import streamlit as st
# import os
# from dotenv import load_dotenv

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# #PROMPT TEMPLATE
# prompt = ChatPromptTemplate.from_messages(

#     [
#         ("system", "you are best in the field and an important asset to the company your response can make the company grow help me with the following query best you can .")
#         ("user", "question{question}")

#     ]
# )
# #streamlit frame work
# st.title("Langchain demo with gemma api")
# input_text = st.text_input("search the topic u want ")

# #ai llm 
# llm = ChatOpenAI(model = "grp_3.5-turbo")# calling the model you want
# outout_parser = StrOutputParser()
# chain = prompt|llm|outout_parser

# if input_text:
#     st.write(chain.invoke({"question":input_text}))
from langchain_google_genai import ChatGoogleGenerativeAI # Import the Gemini Chat Model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# 1. Set Environment Variables
# Use GEMINI_API_KEY for the LLM
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY") 
# Use LANGSMITH keys for tracing (optional, but good practice)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") 

# PROMPT TEMPLATE
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "you are best in the field and an important asset to the company. Your response can make the company grow. Help me with the following query best you can."
        ),
        ("user", "question:{question}")
    ]
)

# Streamlit framework
st.title("Langchain Demo with Gemini API")
input_text = st.text_input("Search the topic you want:")

# 2. AI LLM (Using the Gemini Model)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") 

# 3. Chain Definition
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Execution
if input_text:
    st.write(chain.invoke({"question": input_text}))
    