# agent_gemini.py

import os
import google.generativeai as genai
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Connect to MCP server
client = Client(PythonStdioTransport("server.py"))
tools = client.describe_tools()

# Gemini setup
model = genai.GenerativeModel(
    model_name="gemini-pro",
    tools=tools
)

# Sample resume
resume_text = """
John Doe is a backend developer with 5 years of experience in Python and SQL.
He has worked on microservices, Docker deployments, and team-based agile environments.
"""

job_title = "Backend Developer"

# Create chat session with Gemini
chat = model.start_chat(history=[])

response = chat.send_message(
    content=[
        {
            "role": "user",
            "parts": [
                f"Please analyze this resume for the role of {job_title}.",
                {"function_call": {
                    "name": "screen_cv",
                    "args": {
                        "cv_text": resume_text,
                        "job_title": job_title
                    }
                }}
            ]
        }
    ]
)

# Handle response
print("=== Gemini Agent Response ===")
print(response.text)