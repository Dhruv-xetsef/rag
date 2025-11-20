from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
#from langchain_google_genai import ChatGoogleGemerativeAI # import the gemini api fro the web

from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()
#os.environ['OPEN_API_KEY'] = os.getenv("OPEN_API_KEY")
app = FastAPI(
    title = "langchain server",
    version = "1.0",
    description = "a simple api server learning"

)
# add_routes(
#     app,
#     ChatGoogleGenerativeAI(),
#     path= "/openai"
# )
#model = ChatGoogleGenerativeAI()
llm = Ollama(model = "gemma3:1b")

#prompt_1 = ChatPromptTemplate.from_template("write me an essay about {topic} with 100 words")# thi sprompt will be given to the gemini model with api key he gemini is hosted on the cloud
prompt_2 = ChatPromptTemplate.from_template("writw mw an poem about {topic} with 100 words")# this prompt will be given to th eollama gemma model 3 1b
# add_routes(
#     app,
#     prompt_1|model,
#     path = "/essay"# responsible for interacting with the gemini model thet is host3d on the cloud
# )
add_routes(
    app,
    prompt_2|llm,
    path = "/poem"# responsible for interacting with the gemma3:1b model thet is host3d on the system, locally

)

if __name__ == "main":
    uvicorn.run(app,host = "localhost", port = 8000)# in place of local host we can add anythingf like the webserver making it easily integratable to the website that is premade
