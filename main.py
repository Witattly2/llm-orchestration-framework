import os
import json
from datetime import datetime
from typing import List, Dict, Any
import time

class LLMOrchestrator:
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.llm_provider = self.config.get("llm_provider", "openai")
        self.api_key = os.getenv(f"{self.llm_provider.upper()}_API_KEY")
        if not self.api_key:
            # In a real scenario, this would be a proper error or a fallback
            print(f"Warning: API key for {self.llm_provider} not found in environment variables. Using dummy key.")
            self.api_key = "DUMMY_API_KEY"
        print(f"Initialized LLMOrchestrator with provider: {self.llm_provider}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        if not os.path.exists(config_path):
            print(f"Config file not found at {config_path}. Using default settings.")
            return {"llm_provider": "openai", "model": "gpt-3.5-turbo", "temperature": 0.7}
        with open(config_path, "r") as f:
            return json.load(f)

    def _call_llm_api(self, prompt: str, model: str, temperature: float) -> str:
        # This is a placeholder for actual LLM API calls (e.g., OpenAI, Gemini)
        # In a real scenario, this would involve using the respective SDKs
        print(f"Calling {self.llm_provider} API with model {model} and temperature {temperature}...")
        print(f"Prompt: {prompt[:50]}...")
        # Simulate API response
        time.sleep(1) # Simulate network latency
        return f"Simulated response for \'{prompt[:20]}...\' from {model}"

    def generate_response(self, prompt: str, model: str = None, temperature: float = None) -> str:
        model = model or self.config.get("model", "gpt-3.5-turbo")
        temperature = temperature or self.config.get("temperature", 0.7)
        return self._call_llm_api(prompt, model, temperature)

    def orchestrate_workflow(self, steps: List[Dict[str, Any]]) -> List[str]:
        results = []
        for i, step in enumerate(steps):
            print(f"\nExecuting step {i+1}: {step.get("name", "Unnamed Step")}")
            prompt = step.get("prompt")
            if not prompt:
                print("Skipping step due to missing prompt.")
                continue
            
            model = step.get("model", self.config.get("model"))
            temperature = step.get("temperature", self.config.get("temperature"))
            
            response = self.generate_response(prompt, model, temperature)
            results.append(response)
            print(f"Step {i+1} Result: {response[:50]}...")
        return results

if __name__ == "__main__":
    # Example Usage
    orchestrator = LLMOrchestrator()

    # Simple generation
    print("\n--- Simple Generation ---")
    response = orchestrator.generate_response("Explain quantum computing in simple terms.")
    print(f"Final Response: {response}")

    # Workflow orchestration
    print("\n--- Workflow Orchestration ---")
    workflow_steps = [
        {
            "name": "Initial Idea Generation",
            "prompt": "Brainstorm 5 unique ideas for a new mobile app.",
            "model": "gpt-4",
            "temperature": 0.8
        },
        {
            "name": "Feature Expansion",
            "prompt": "Expand on the first idea with 3 key features.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.6
        }
    ]
    workflow_results = orchestrator.orchestrate_workflow(workflow_steps)
    print("\n--- Workflow Summary ---")
    for i, res in enumerate(workflow_results):
        print(f"Step {i+1} Summary: {res[:70]}...")

    # Example with a custom config file
    print("\n--- Custom Config Example ---")
    custom_config = {"llm_provider": "gemini", "model": "gemini-pro", "temperature": 0.9}
    with open("custom_config.json", "w") as f:
        json.dump(custom_config, f)
    
    try:
        custom_orchestrator = LLMOrchestrator(config_path="custom_config.json")
        custom_response = custom_orchestrator.generate_response("Write a short poem about AI.")
        print(f"Custom Config Response: {custom_response}")
    except ValueError as e:
        print(f"Error with custom config: {e}")
    finally:
        if os.path.exists("custom_config.json"):
            os.remove("custom_config.json")
