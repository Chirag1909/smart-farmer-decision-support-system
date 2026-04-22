import subprocess
import sys
from pathlib import Path

print("Installing deps...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart"])

print("Starting backend...")
subprocess.call(["uvicorn", "web_app.backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

