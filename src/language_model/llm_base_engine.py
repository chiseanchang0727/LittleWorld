from typing import Optional, Type
from pydantic import BaseModel
from language_model.llm_base_chatmodel import LLMChatModel
from config.models.character_config import LLMConfig
from langchain_core.prompts.chat import ChatPromptTemplate

class BaseAIModelEngine(LLMChatModel):
    """Base AI model engine with personality prompt support."""
    
    def __init__(
        self, 
        config: LLMConfig, 
        personality_prompt: str, 
        input_blocks: Optional[list[str]] = ["{world_state}, {input_messages}"],
        structured_output_schema: Type[BaseModel] = None,
    ):
        """
        Initialize base AI model engine.
        
        Args:
            config: LLM configuration
            personality_prompt: Personality prompt text
        """
        super().__init__(config=config)
        self.personality_prompt = personality_prompt
        self.input_blocks = input_blocks
        self.template = self._compose_template(input_blocks)  
        self.structured_output_schema = structured_output_schema

    def _compose_template(self, input_blocks):
        messages = [("system", self.personality_prompt)]
        if input_blocks:
            messages += [("human", block) for block in input_blocks]
        return ChatPromptTemplate.from_messages(messages)


    async def _call_llm(self, messages):
      
        if self.structured_output_schema:
            self.llm = self.llm.with_structured_output(self.structured_output_schema)
            
        response = await self.llm.ainvoke(messages)
        return response

    async def basic_answering(self, messages):
        return await self._call_llm(self.template.invoke(messages))

