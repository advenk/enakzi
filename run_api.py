import os
import sys
import subprocess
import platform
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from config.config import API_CONFIG, DB_CONFIG

def main():
    print("Starting API server locally...")
    env = os.environ.copy()
    env["DB_HOST"] = DB_CONFIG["host"]
    env["DB_PORT"] = DB_CONFIG["port"]
    env["DB_NAME"] = DB_CONFIG["dbname"]
    env["DB_USER"] = DB_CONFIG["user"]
    env["DB_PASS"] = DB_CONFIG["password"]
    if platform.system() == "Windows":
        python_exe = os.path.join("venv", "Scripts", "python")
        uvicorn_exe = os.path.join("venv", "Scripts", "uvicorn")
    else:
        python_exe = os.path.join("venv", "bin", "python")
        uvicorn_exe = os.path.join("venv", "bin", "uvicorn")

    if not os.path.exists("main.py"):
        print("Error: This script should be run from the api directory.")
        print("Please run: cd api && ../run_api.py")
        sys.exit(1)

    try:
        cmd = [uvicorn_exe, "main:app", "--host", API_CONFIG["host"], "--port", API_CONFIG["port"], "--reload"]
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\nAPI server stopped.")
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 