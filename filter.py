# filter.py
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Load the API key from environment variables
api_key = os.getenv('GOOGLE_API_KEY')

# Set the environment variable for Google Application Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define a prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that extracts relevant information based on the instructions.",
        ),
        ("human", "{content}"),
    ]
)

# Create an LLMChain with the Gemini LLM and the prompt template
llm_chain = prompt_template | llm

def filter_with_gemini(data, instructions):
    # Combine content from the main page and relevant nested links
    combined_content = data['content']
    for nested in data.get('nested_links', []):
        combined_content += "\n" + nested.get('content', '')

    # Split the combined content into smaller chunks to avoid token limit
    max_token_limit = 1000000  # Model's token limit
    chunk_size = max_token_limit // 2  # Split content into smaller parts
    chunks = [combined_content[i:i+chunk_size] for i in range(0, len(combined_content), chunk_size)]

    filtered_content = ""
    for chunk in chunks:
        # Send each chunk to the model for processing
        response = llm_chain.invoke({
            "content": f"Instructions: {instructions}\n\nData: {chunk}\n\nExtract only the relevant information based on the instructions."
        })
        filtered_content += str(response.content)  # Append the result of each chunk

    return {
        'url': data['url'],
        'title': data['title'],
        'filtered_content': filtered_content
    }


def synthesize_document(data):
    import json
    return json.dumps(data, indent=2)  # Format as pretty-printed JSON
