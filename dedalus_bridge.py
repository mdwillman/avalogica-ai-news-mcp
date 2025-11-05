from fastapi import FastAPI, Request
import uvicorn
import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/weather")
async def weather(request: Request):
    body = await request.json()
    latitude = body.get("latitude", 40.7128)
    longitude = body.get("longitude", -74.0060)
    days = body.get("days", 3)

    print(f"🌦️ Received request: lat={latitude}, lon={longitude}, days={days}")

    client = AsyncDedalus(api_key=os.getenv("DEDALUS_API_KEY"))
    runner = DedalusRunner(client)

    result = await runner.run(
    	input=(
        	"You **must** use the `get_forecast` tool from the `avalogica-weather-mcp` MCP server "
        	f"to fetch the forecast for latitude={latitude}, longitude={longitude}, and days={days}. "
        	"Do not query any external APIs directly. Return the result **exactly** as provided by that MCP server, "
        	"and append the signature [served by avalogica-weather-mcp] at the end."
    	),
    	model="openai/gpt-5-mini",
    	mcp_servers=["mdwillman/avalogica-weather-mcp"],
    	stream=False
    )

    return {"forecast": result.final_output}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)