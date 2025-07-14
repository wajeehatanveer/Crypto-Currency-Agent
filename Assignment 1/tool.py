from agents import Agent, Runner, function_tool
from main import config
import os 
from dotenv import load_dotenv
import requests 

# --- Tool 1: Get price by coin symbol ---
@function_tool
def get_crypto_price(symbol: str) -> str:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data.get("price", "N/A")
        return f"The current price of {symbol.upper()} is ${price}"
    else:
        return f"Error: Could not fetch price for {symbol.upper()}"

# --- Tool 2: Get all coins (limited) ---
@function_tool
def get_all_coins(limit: int = 5) -> str:
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = ""
        for coin in data[:limit]:
            result += f"{coin['symbol']}: ${coin['price']}\n"
        return f"Here are the top {limit} coins:\n{result}"
    else:
        return "Error: Could not fetch coin list."

#Create Crypto Agent
agent = Agent(
    name="Crypto Currency Agent",
    instructions="You are a helpful assistant. Use Binance API to give current crypto prices and coin listings.",
    tools=[get_crypto_price, get_all_coins]
)

#Run the Agent
response = Runner.run_sync(
    agent,
    input='What is the current price of BTCUSDT and show me list of Top 5 coins',
    run_config=config
)

print("\n🤖 AI Response:")
print(response.final_output)


