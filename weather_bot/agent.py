import os
import requests
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# 1. TOOL DEFINITION
def get_weather(city_name: str) -> str:
    """Fetches the current temperature for a given city."""
    try:
        # Step 1: Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        geo_res = requests.get(geo_url).json()
        if not geo_res.get('results'):
            return f"Could not find coordinates for {city_name}."
        
        location = geo_res['results'][0]
        lat, lon = location['latitude'], location['longitude']
        
        # Step 2: Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()
        temp = weather_res['current_weather']['temperature']
        
        return f"The current temperature in {city_name} is {temp}°C."
    except Exception as e:
        return f"Error: {str(e)}"

# 2. DIRECT OLLAMA CONFIGURATION
# We still use the LiteLlm class because it's the ADK's 
# generic bridge for local models.
model_config = LiteLlm(
    model="ollama_chat/minimax-m2.5:cloud", 
    api_base="http://localhost:11434",
    stream=True
)

# 3. AGENT DEFINITION
root_agent = Agent(
    model=model_config,
    name='weather_agent',
    description='A helpful assistant for user questions about weather.',
    instruction='''You are a weather expert. Use the get_weather tool 
    to provide accurate current temperatures.''',
    tools=[get_weather]
)

if __name__ == "__main__":
    # Test call
    print("Agent is thinking...")
    response = root_agent.run("What is the weather in New York?")
    print(f"Agent: {response.text}")