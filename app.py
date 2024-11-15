# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import asyncio
from dotenv import load_dotenv
from scraper import scrape_website
from filter import filter_with_gemini, synthesize_document

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

#example

class ScrapeRequest(BaseModel):
    url: str
    instructions: str
    depth: int = 1
    keywords: list = []

def synthesize_document(data):
    # Return the data directly as a dictionary
    return data

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    url = request.url
    instructions = request.instructions
    depth = request.depth
    keywords = request.keywords

    if not url or not instructions:
        raise HTTPException(status_code=400, detail="URL and instructions are required")

    try:
        data = await scrape_website(url, depth, keywords)
        filtered_data = filter_with_gemini(data, instructions)
        document = synthesize_document(filtered_data)
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
