import json
from tools.weather_tool import WeatherTool

class AgentOrchestrator:
    def __init__(self, knowledge_base, llm_client):
        self.knowledge_base = knowledge_base
        self.llm_client = llm_client
        # Tool registry: add more tools as needed
        self.tools = {
            'weather': WeatherTool(),
        }

    def handle_prompt(self, prompt: str) -> str:
        # Weather tool trigger: simple keyword check
        weather_keywords = ["weather", "temperature", "rain", "forecast", "sunny", "cloudy", "humidity"]
        if any(word in prompt.lower() for word in weather_keywords):
            tool = self.tools.get('weather')
            if not tool:
                return '[Weather tool not found]'
            result = tool.run({})
            return f"[WeatherTool]: {result['weather']}"
        # Normal flow: retrieve context and call LLM
        context = self.knowledge_base.retrieve(prompt)
        response = self.llm_client.generate_response(prompt, context)
        return response 