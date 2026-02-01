
from pydantic import BaseModel
from language_model.base import LLMBase
from language_model.providers.provider_factory import create_llm_instance
from config.models.character_config import LLMConfig
from langchain_core.runnables import Runnable
from openai import AsyncOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

class OpenAIEngine(LLMBase):
    def __init__(self, llm):
        self.llm = llm
        
    async def ainvoke(self, messages):
        return await self.llm.ainvoke(messages)

    def bind_tools(self, tools):
        return self.llm.bind_tools(tools)
    
    def with_structured_output(self, schema):
        return self.llm.with_structured_output(schema)

class GeminiEngine(LLMBase):
    def __init__(self, llm):
        self.llm = llm
    
    async def ainvoke(self, messages):
        return await self.llm.ainvoke(messages)

    def bind_tools(self, tools):
        return GeminiEngine(self.llm.bind_tools(tools))
    
    def with_structured_output(self, schema):
        return self.llm.with_structured_output(schema)

class VLLMEngine(LLMBase):
    def __init__(self, client: AsyncOpenAI, config: LLMConfig, tools=None, schema=None):
        self.client = client
        self.config = config
        self.tools = tools
        self.schema = schema
    
    @staticmethod
    def lc_prompt_to_openai_messages(input_message):
        role_map = {
            "system": "system",
            "human": "user",
            "ai": "assistant",
            "tool": "tool",
        }

        # Normalize input into a flat message list
        if hasattr(input_message, "messages"):
            msgs = input_message.messages
        elif isinstance(input_message, list):
            msgs = input_message
        else:
            raise TypeError(f"Cannot process message container: {type(input_message)}")

        output = []
        for msg in msgs:
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            elif isinstance(msg, ToolMessage):
                role = "tool"
            else:
                raise TypeError(f"Unsupported message type: {type(msg)}")

            # Handle content variations
            content = (
                msg.content if isinstance(msg.content, str) 
                else str(msg.content)
            )

            entry = {
                "role": role,
                "content": content,
            }

            # Special handling for tool messages
            if role == "tool":
                if "tool_call_id" in msg.additional_kwargs:
                    entry["tool_call_id"] = msg.additional_kwargs["tool_call_id"]

            output.append(entry)

        return output
    
    @staticmethod
    def _normalize_schema(schema):
        if schema is None:
            return None

        # Pydantic model class
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            return schema.model_json_schema()

        # Already JSON schema
        if isinstance(schema, dict):
            return schema

        raise TypeError(f"Unsupported schema type: {type(schema)}")
    
    async def ainvoke(self, messages):
        
        openai_messages = self.lc_prompt_to_openai_messages(messages)

        # if self.tools:
        #     print(f"[The tool we have]: {self.tools}")
        payload = {
            "model": self.config.version,
            "messages":  openai_messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "presence_penalty": 1.5,   
            "tools": self.tools,
            "tool_choice": "auto" if self.tools else None,
            "extra_body": {
                "top_k": self.config.top_k,
                "chat_template_kwargs": {
                    "enable_thinking": self.config.enable_thinking
                },
                "guided_json":self._normalize_schema(self.schema)
            }
        }

        return await self.client.chat.completions.create(**payload)

    def bind_tools(self, tools)-> "VLLMEngine":
        self.tools = tools
        return VLLMEngine(self.client, self.config, tools, self.schema)

    def with_structured_output(self, schema: type[BaseModel]) -> "VLLMEngine":
        return VLLMEngine(
            client=self.client,
            config=self.config,
            tools=self.tools,
            schema=schema,
        )

def create_chat_engine(config: LLMConfig) -> LLMBase:
    if config.type == "openai":
        return OpenAIEngine(create_llm_instance(config))
    elif config.type == "gemini":
        return GeminiEngine(create_llm_instance(config))
        # add a tranformation layer to transffer msg 
    elif config.type == "vllm":
        return VLLMEngine(create_llm_instance(config), config)
    else:
        raise ValueError("Unsupported provider")

class LLMChatModel(LLMBase, Runnable):
    def __init__(self, config: LLMConfig):
        self.llm: LLMBase = create_chat_engine(config)
        
    def invoke(self, *args, **kwargs):
        raise NotImplementedError("OpenAIEngine is async-only. Use `await ainvoke()` instead.")

    async def ainvoke(self, messages):
        return await self.llm.ainvoke(messages)

    # self.__class__.__new__ is necessary to avoid LLMChatModel become RunnableBinding which cause no attr error
    def with_structured_output(self, schema):
        new_model = self.__class__.__new__(self.__class__)
        new_model.llm = self.llm.with_structured_output(schema)
        return new_model

    def bind_tools(self, tools):
        new_model = self.__class__.__new__(self.__class__)
        new_model.llm = self.llm.bind_tools(tools)
        return new_model
    

