# client.py
import asyncio
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from hack.generate_cv_text_injections import generate_cv_text_injections

# Path to the MCP server script
SERVER_PATH = "server.py"  # Path to your MCP server that defines screen_cv

# Define one secure, normal CV input
secure_cv = """
Alice Johnson is a backend engineer with 4 years of experience in Go, PostgreSQL, and cloud infrastructure.
She has deployed scalable microservices, built CI/CD pipelines, and collaborated with cross-functional teams.
She is passionate about clean code, system design, and backend architecture.
"""

job_title = "Backend Developer"
client = Client(PythonStdioTransport(SERVER_PATH))

async def main():
    injected_cvs = generate_cv_text_injections()
    test_cases = [("Secure input", secure_cv)] + [(f"Injection #{i+1}", cv) for i, cv in enumerate(injected_cvs)]

    async with client:
        for i, (label, cv_text) in enumerate(test_cases):
            print(f"\n=== Test #{i} — {label} ===\n{cv_text.strip()[:120]}...")

            result = await client.call_tool("screen_cv", {
                "cv_text": cv_text,
                "job_title": job_title
            })

            print(f"\n--- Result #{i} ---")
            print(result.data)

            print(f"Status: {'✅ Safe' if not result.is_error else '❌ Blocked'}")
            print("-" * 50)

asyncio.run(main())
