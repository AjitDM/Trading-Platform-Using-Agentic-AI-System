from langchain_gemini import ChatGemini
import os 
from dotenv import load_dotenv

class GeminiLLM:
    def __init__(self):
        load_dotenv()


    def get_llm(self):
        try:
            print(os.getenv("GEMINI_API_KEY"))
            os.environ["GEMINI_API_KEY"]=self.gemini_api_key=os.getenv("GEMINI_API_KEY")
            llm=ChatGemini(api_key=self.gemini_api_key,model="gemini-3.8-flash")
            return llm
        except Exception as e:
            raise ValueError("Error occurred with exception : {e}")