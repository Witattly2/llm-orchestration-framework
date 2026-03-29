import os
from typing import List, Dict
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class LLMOrchestrator:
    def __init__(self, model_name: str = 'gpt-3.5-turbo'):
        self.llm = OpenAI(model_name=model_name)
        self.prompts: Dict[str, PromptTemplate] = {}

    def add_prompt(self, name: str, template: str, input_variables: List[str]):
        self.prompts[name] = PromptTemplate(template=template, input_variables=input_variables)

    def run_chain(self, prompt_name: str, inputs: Dict[str, str]) -> str:
        if prompt_name not in self.prompts:
            raise ValueError(f'Prompt {prompt_name} not found')
        chain = LLMChain(llm=self.llm, prompt=self.prompts[prompt_name])
        return chain.run(**inputs)

# Example usage
if __name__ == '__main__':
    orchestrator = LLMOrchestrator()
    orchestrator.add_prompt('summary', 'Summarize the following text: {text}', ['text'])
    # result = orchestrator.run_chain('summary', {'text': 'Large language models are powerful tools...'})