#!/usr/bin/env python3
"""
Script to run the crawler locally without Docker.
"""
import os
import sys
import subprocess
import platform

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the config
from config.config import CRAWLER_CONFIG, DB_CONFIG

def main():
    """Run the crawler locally."""
    print("Starting crawler locally...")
    
    # Set environment variables
    env = os.environ.copy()
    env["DB_HOST"] = DB_CONFIG["host"]
    env["DB_PORT"] = DB_CONFIG["port"]
    env["DB_NAME"] = DB_CONFIG["dbname"]
    env["DB_USER"] = DB_CONFIG["user"]
    env["DB_PASS"] = DB_CONFIG["password"]
    env["NIMA_MODEL_PATH"] = CRAWLER_CONFIG["nima_model_path"]
    
    # Determine the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_exe = os.path.join("venv", "Scripts", "python")
        scrapy_exe = os.path.join("venv", "Scripts", "scrapy")
    else:
        python_exe = os.path.join("venv", "bin", "python")
        scrapy_exe = os.path.join("venv", "bin", "scrapy")
    
    # Check if we're in the crawler directory
    if not os.path.exists("scrapy.cfg"):
        print("Error: This script should be run from the crawler directory.")
        print("Please run: cd crawler && ../run_crawler.py")
        sys.exit(1)
    
    # Run the crawler using scrapy
    try:
        cmd = [scrapy_exe, "crawl", "general"]
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\nCrawler stopped.")
    except Exception as e:
        print(f"Error starting crawler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 