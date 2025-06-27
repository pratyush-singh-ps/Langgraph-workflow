from openai import OpenAI

SYSTEM_PROMPT = (
    "You are CIQ Assistant, an expert technical support AI for CommerceIQ. "
    "Whenever you see an API endpoint mentioned in this system prompt, you must call that API, use the returned data, and provide a clear, actionable answer to the user.\n"
    "API to use: https://api.github.com/repos/psf/requests\n"
    "Instructions: "
    "- When a user asks for information related to the API above, call the API, extract relevant data, and include it in your response. "
    "- If the API call fails, inform the user gracefully. "
    "- Always be friendly, concise, and professional. "
    "- If the user's question is unrelated to the API, answer using your general knowledge and the knowledge base. "
    "If you don't know the answer or the API is not available, say so honestly."
)

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://ciq-litellm-proxy-service.prod-dbx.commerceiq.ai",
            api_key="sk-WRDSNGPePp-cHG5Q6WhRjA"
        )
        self.model = "openai/gpt-4o"

    def generate_response(self, prompt: str, context: str) -> str:
        # Combine prompt and context for the LLM
        user_input = f"Context: {context}\nUser: {prompt}"
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "[LLM returned no content]"
        except Exception as e:
            return f"[LLM Error: {str(e)}]" 