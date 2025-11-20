from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama  # 1. Correct import for Ollama

import streamlit as st
import os
from dotenv import load_dotenv


load_dotenv() 

if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    
st.set_page_config(page_title="Rag tutorial 1 local RAG", layout="centered") # Updated title
st.title("🧠 LangChain RAG local RAG gemma ") # Updated title
#st.markdown("---")

# User input field
input_text = st.text_input(
    "Enter your query:",
    placeholder="Ask me anything...",
    key="input_query"
)

llm = Ollama(model="gemma3:4b")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a helpful and knowledgeable assistant, specializing in providing concise and professional answers. Your response can make the company grow. Help the user with the following query best you can."
        ),
        ("user", "question: {question}")
    ]
)


output_parser = StrOutputParser()
chain = prompt | llm | output_parser


if input_text:
    with st.spinner("Generating response..."):
        try:
            response = chain.invoke({"question": input_text})
            st.markdown("### Answer")
            st.info(response)

        except Exception as e:

            st.error(f"An error occurred during model call. Is the Ollama server running? Error: {e}") 

# st.markdown("---")
# st.caption("Using local Ollama model (gemma3:1b) via LangChain.")



# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_community.llms import Ollama  # 1. Correct import for Ollama

# import streamlit as st
# import os
# from dotenv import load_dotenv

# # --- 1. CONFIGURATION AND ENVIRONMENT SETUP (Switched to Ollama/OpenAI keys) ---
# load_dotenv() 

# # CHECK FOR API KEY: We now check for a local environment variable, 
# # although Ollama typically does not require one.
# # If migrating to Ollama, we remove the strict API key check for Gemini.
# # If using the original code as a template, we assume user is setting OpenAI keys 
# # for LangSmith/other components.

# # Set LangSmith tracing keys (optional)
# if os.getenv("LANGCHAIN_API_KEY"):
#     os.environ["LANGCHAIN_TRACING_V2"] = "true"
#     # LangChain will automatically read LANGCHAIN_API_KEY and PROJECT from os.getenv()

# # --- 2. STREAMLIT FRAMEWORK SETUP ---
# st.set_page_config(page_title="Ollama/Gemma Chatbot Demo", layout="centered") # Updated title
# st.title("🧠 LangChain Chatbot Demo with Ollama (Gemma)") # Updated title
# st.markdown("---")

# # User input field
# input_text = st.text_input(
#     "Enter your query:",
#     placeholder="Ask me anything...",
#     key="input_query"
# )

# # --- 3. LLM AND CHAIN DEFINITION ---

# # LLM (Using the local Ollama Model)
# # FIX: Added 'verbose=True' to enable console logging for input/output and simple timing.
# llm = Ollama(model="gemma3:1b", verbose=True) # Using gemma:7b as gemma3:1b is often referred to as gemma:7b or similar

# # PROMPT TEMPLATE
# # 3. Fixing prompt template syntax (need commas and correct user message format)
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system", 
#             "You are a helpful and knowledgeable assistant, specializing in providing concise and professional answers. Your response can make the company grow. Help the user with the following query best you can."
#         ),
#         ("user", "question: {question}")
#     ]
# )

# # Chain Definition
# output_parser = StrOutputParser()
# chain = prompt | llm | output_parser

# # --- 4. EXECUTION ---
# if input_text:
#     with st.spinner("Generating response..."):
#         try:
#             # Invoke the chain with the user's question
#             response = chain.invoke({"question": input_text})
            
#             # Display the result to the Streamlit app
#             st.markdown("### Answer")
#             st.info(response)

#         except Exception as e:
#             # Ollama errors often relate to the service not running
#             st.error(f"An error occurred during model call. Is the Ollama server running? Error: {e}") 

# st.markdown("---")
# st.caption("Using local Ollama model (gemma3:1b) via LangChain.")
