# client.py

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

# Path to the MCP server script
SERVER_PATH = "server.py"  # Make sure this file exists and contains your screen_cv tool

# Start a connection to the server
client = Client(PythonStdioTransport(SERVER_PATH))

# Sample CV/resume text
cv_text = """
Jane Doe is a backend developer with 6 years of experience in Python, SQL, and distributed systems.
She has designed REST APIs, worked with Docker and Kubernetes, and led agile teams across multiple projects.
Strong communicator and team collaborator.
"""

# Optional: specify a job title
job_title = "Backend Developer"

# Call the tool
result = client.call_tool("screen_cv", {
    "cv_text": cv_text,
    "job_title": job_title
})

# Print the result
print("=== CV Screening Result ===")
print(result)