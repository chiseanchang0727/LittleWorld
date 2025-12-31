from typing import Any, Protocol, Dict, List, runtime_checkable, Self, Type
from pydantic import BaseModel
from langchain_core.prompt_values import PromptValue

     
@runtime_checkable
class LLMBase(Protocol):
    """
    Base interface for all chat engine implementations (OpenAI, Gemini, vLLM...).

    The fluent self-returning methods use TypeVar[Self] for correct typing.
    """

    async def ainvoke(self, messages: PromptValue) -> Any:
        ...

    def with_structured_output(self, schema: Type[BaseModel]) -> Self:
        ...

    def bind_tools(self, tools: List[Dict[str, Any]]) -> Self:
        ...


