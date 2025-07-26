# client.py
import asyncio
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

# Path to the MCP server script
SERVER_PATH = "server.py"  # Path to your MCP server that defines screen_cv

# Sample CV/resume text
cv_text = """
Jane Doe is a backend developer with 6 years of experience in Python, SQL, and distributed systems.
She has designed REST APIs, worked with Docker and Kubernetes, and led agile teams across multiple projects.
Strong communicator and team collaborator.
"""

job_title = "Backend Developer"
client = Client(PythonStdioTransport(SERVER_PATH))

async def main():
    async with client:
        result = await client.call_tool("screen_cv", {
            "cv_text": cv_text,
            "job_title": job_title
        })

        print(f"\n=== MCP Tool Result ===")
        print(result.data)

        print(f"\n--- Debug Info ---")
        print(f"Status: {'✅ Success' if not result.is_error else '❌ Error'}")
        print(f"Response type: {type(result.data)}")

asyncio.run(main())
