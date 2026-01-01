# km/language_model/providers/llm_provider_factory.py

import os
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import Runnable
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from src.config.enum import Provider

def create_llm_instance(config) -> Runnable:
    load_dotenv()
    provider = config.type.lower()
    model_name = config.version

    if provider == Provider.OPENAI:
        api_key = os.getenv("OPENAI_API_KEY")   
        return ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=None,
            max_retries=2,
            api_key=api_key
        )

    # elif provider == Provider.GOOGLE:
    #     api_key = os.getenv("GOOGLE_API_KEY")
    #     return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

    elif provider == Provider.VLLM:
        api_key = "thekey" # put into env
        openai_api_base = "http://localhost:8000/v1" # put into env

        return AsyncOpenAI(
            api_key=api_key,
            base_url=openai_api_base,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
