from langchain_sarvam import ChatSarvam
import os 
from dotenv import load_dotenv

class SarvamLLM:
    def __init__(self):
        load_dotenv()


    def get_llm(self):
        try:
            # print(os.getenv("SARVAM_API_KEY"))
            os.environ["SARVAM_API_KEY"]=self.sarvam_api_key=os.getenv("SARVAM_API_KEY")
            llm=ChatSarvam(api_key=self.sarvam_api_key,model="sarvam-105b")
            return llm
        except Exception as e:
            raise ValueError("Error occurred with exception : {e}")