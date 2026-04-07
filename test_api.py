import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# Model "gemma-4-31b-it" 
llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it")

response = llm.invoke("Xin chào?")
print(response.content)