#!/usr/bin/env python3
"""
Setup script to prepare the local environment for running all components.
"""
import os
import sys
import subprocess
import platform
import shutil

def check_postgres():
    """Check if PostgreSQL is installed and running."""
    print("Checking PostgreSQL installation...")
    
    try:
        # Check if psql is available
        subprocess.run(["psql", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ PostgreSQL client is installed.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ PostgreSQL client not found. Please install PostgreSQL.")
        print("   macOS: brew install postgresql")
        print("   Ubuntu/Debian: sudo apt install postgresql postgresql-contrib")
        return False
    
    # Try to connect to PostgreSQL
    try:
        result = subprocess.run(
            ["psql", "-h", "localhost", "-U", "postgres", "-c", "SELECT 1;"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print("✅ PostgreSQL server is running and accessible.")
        return True
    except subprocess.SubprocessError:
        print("❌ Could not connect to PostgreSQL server.")
        print("   Please make sure PostgreSQL is running:")
        print("   macOS: brew services start postgresql")
        print("   Ubuntu/Debian: sudo service postgresql start")
        return False

def setup_database():
    """Create the database if it doesn't exist."""
    print("\nSetting up database...")
    
    try:
        # Check if database exists
        result = subprocess.run(
            ["psql", "-h", "localhost", "-U", "postgres", "-lqt"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        
        if "explorer" in result.stdout:
            print("✅ Database 'explorer' already exists.")
        else:
            # Create database
            subprocess.run(
                ["psql", "-h", "localhost", "-U", "postgres", "-c", "CREATE DATABASE explorer;"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            print("✅ Created database 'explorer'.")
        
        return True
    except subprocess.SubprocessError as e:
        print(f"❌ Failed to set up database: {e}")
        return False

def setup_api():
    """Set up the API component."""
    print("\nSetting up API component...")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("api/venv"):
        print("Creating virtual environment for API...")
        subprocess.run(
            [sys.executable, "-m", "venv", "api/venv"],
            check=True
        )
    
    # Install dependencies
    print("Installing API dependencies...")
    pip_cmd = "api/venv/bin/pip" if platform.system() != "Windows" else "api\\venv\\Scripts\\pip"
    subprocess.run(
        [pip_cmd, "install", "-r", "api/requirements.txt"],
        check=True
    )
    
    print("✅ API setup complete.")

def setup_crawler():
    """Set up the crawler component."""
    print("\nSetting up crawler component...")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("crawler/venv"):
        print("Creating virtual environment for crawler...")
        subprocess.run(
            [sys.executable, "-m", "venv", "crawler/venv"],
            check=True
        )
    
    # Install dependencies
    print("Installing crawler dependencies...")
    pip_cmd = "crawler/venv/bin/pip" if platform.system() != "Windows" else "crawler\\venv\\Scripts\\pip"
    subprocess.run(
        [pip_cmd, "install", "-r", "crawler/requirements.txt"],
        check=True
    )
    
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created images directory.")
    
    # Create nima_weights directory if it doesn't exist
    if not os.path.exists("crawler/nima_weights"):
        os.makedirs("crawler/nima_weights")
        print("Created nima_weights directory.")
        print("Note: You'll need to add the NIMA model weights file to crawler/nima_weights/model.pth")
    
    print("✅ Crawler setup complete.")

def setup_web():
    """Set up the web component."""
    print("\nSetting up web component...")
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Node.js is installed.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Node.js not found. Please install Node.js.")
        print("   Visit: https://nodejs.org/")
        return False
    
    # Install dependencies
    print("Installing web dependencies...")
    os.chdir("web")
    subprocess.run(["npm", "install"], check=True)
    os.chdir("..")
    
    print("✅ Web setup complete.")

def main():
    """Main setup function."""
    print("=== Local Setup for explorer Project ===\n")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("❌ Python 3.6 or higher is required.")
        sys.exit(1)
    
    # Check PostgreSQL
    if not check_postgres():
        print("\n❌ Please fix PostgreSQL issues before continuing.")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("\n❌ Failed to set up database. Please fix the issues before continuing.")
        sys.exit(1)
    
    # Setup components
    setup_api()
    setup_crawler()
    setup_web()
    
    print("\n✅ Setup complete! You can now run each component locally.")
    print("\nTo run the API:")
    print("  cd api && ../run_api.py")
    print("\nTo run the crawler:")
    print("  cd crawler && ../run_crawler.py")
    print("\nTo run the web app:")
    print("  cd web && npm start")

if __name__ == "__main__":
    main() 