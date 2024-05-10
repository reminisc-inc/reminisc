from langchain_openai import ChatOpenAI
import os
import logging
from reminisc.config.config import Config
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class MemoryCreator:
    def __init__(self):
        self.model_name = Config.MEMORY_CREATOR_MODEL_NAME
        self.system_prompt = (
            f"Today is {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}. "
            "You are an AI assistant tasked with generating concise memories based on user input. "
            "Create a memory that captures the key information provided by the user, as if you were storing it for future reference. "
            "The memory should be a brief, third-person statement that encapsulates the most important aspect of the user's input, without adding any extraneous details. "
            "Consider the current date and time when generating the memory, as it may provide important context for future interactions. "
            "Your goal is to create a memory that can be effectively used to enhance the user's experience in subsequent conversations."
        )
        self.llm = ChatOpenAI(model=self.model_name,
                              api_key=os.getenv("OPENAI_API_KEY"))

    def create_memory(self, user_input: str) -> str:
        messages = [
            ("system", self.system_prompt),
            ("human", user_input)
        ]
        try:
            ai_message = self.llm.invoke(messages)
            memory = ai_message.content.strip()
            logger.info(
                f"Generated memory from user input '{user_input}': {memory}")
            return memory
        except Exception as e:
            logger.error(f"Error in creating memory: {e}")
            raise e
