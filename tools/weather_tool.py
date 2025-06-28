import requests
from tools.base import Tool

class WeatherTool(Tool):
    def __init__(self):
        self.api_url = "https://catfact.ninja/fact"  # Public weather API for demo

    def run(self, input: dict) -> dict:
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            weather = response.text.strip()
            return {"status": "success", "weather": weather}
        except Exception as e:
            # Fallback to static context if API fails
            return {
                "status": "error",
                "weather": "The weather in Bangalore is sunny and 28°C. (Static fallback)",
                "error": str(e)
            } 