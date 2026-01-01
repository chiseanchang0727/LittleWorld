from enum import StrEnum, auto

    
class Provider(StrEnum):
    OPENAI = auto()
    GOOGLE = auto()
    VLLM = auto()
            