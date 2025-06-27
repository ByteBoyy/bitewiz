from api_request_schemas import (LanguageEnum)
from lib_llm.helpers.prompts import (english , french , chinese , japanese , spanish)

class PromptGenerator:
    def __init__(self , language : LanguageEnum = LanguageEnum.english):
        self.language = language
        # Add Logic to load prompt based on language
        self.prompts = {
            LanguageEnum.english: english, 
            LanguageEnum.french: french, 
            LanguageEnum.chinese: chinese, 
            LanguageEnum.japanese: japanese, 
            LanguageEnum.spanish: spanish
            }
        self.raw_prompt = self.prompts.get(self.language.value , None)
        if self.raw_prompt is None:
            raise ValueError(f"Prompt not found for language: {self.language}")
        self.prompt = self.raw_prompt.prompt.strip()
        print(f"<< System Prompt loaded >>")
            
        self.serialize_prompt()

    def serialize_prompt(self):
        return self.prompt.strip()

    def __repr__(self):
        return self.prompt