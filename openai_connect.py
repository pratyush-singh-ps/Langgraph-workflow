from openai import OpenAI
import json
def test_llm_connection():
    try:
        # Initialize client with your proxy URL
        client = OpenAI(
            base_url="https://ciq-litellm-proxy-service.prod-dbx.commerceiq.ai",
            api_key="sk-WRDSNGPePp-cHG5Q6WhRjA"             # Your proxy API key - MLE Team to provide
        )
        # Non-streaming response
        response = client.responses.create(
            model="openai/gpt-4o",
            input="Hi how are you."
        )
        print("✅ LLM connection successful!")
        print(f"Response: {response}")
    except Exception as e:
        print("❌ Error connecting to LLM:")
        print(str(e))
if __name__ == "__main__":
    test_llm_connection()