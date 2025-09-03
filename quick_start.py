#!/usr/bin/env python3
"""
Quick Start Script for Telegram Admin Outreach Bot
This script helps you set up and run the bot for the first time.
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def print_banner():
    """Print the welcome banner"""
    print("=" * 60)
    print("🚀 Welcome to Telegram Admin Outreach Bot!")
    print("=" * 60)
    print("This script will help you get started with the bot.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required. Current version:", sys.version)
        print("Please upgrade Python and try again.")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_credentials():
    """Check if credentials are set up"""
    print("\n🔐 Checking credentials...")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found!")
        return True
    
    # Check for environment variables
    required_vars = ["TELEGRAM_API_ID", "TELEGRAM_API_HASH"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if not missing_vars:
        print("✅ Environment variables are set!")
        return True
    
    print("❌ Missing credentials!")
    print("Please create a .env file with the following variables:")
    print("TELEGRAM_API_ID=your_api_id")
    print("TELEGRAM_API_HASH=your_api_hash")
    print("\nOr set them as environment variables.")
    print("\nYou can get these from: https://my.telegram.org/apps")
    return False

def create_env_file():
    """Create a .env file template"""
    print("\n📝 Creating .env file template...")
    
    env_content = """# Telegram API Credentials
# Get these from https://my.telegram.org/apps
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here

# Bot Token (optional - for bot functionality)
# Get this from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Google Sheets API (optional)
# Path to your service account JSON file
GOOGLE_SHEETS_CREDENTIALS=path/to/service_account.json

# Google Sheets ID (optional)
# The ID of the spreadsheet you want to update
GOOGLE_SHEET_ID=your_sheet_id_here

# Rate Limiting (optional)
# Messages per minute to avoid spam
MESSAGES_PER_MINUTE=5

# Logging Level (optional)
# DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created!")
        print("Please edit it with your actual credentials.")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def run_test_scan():
    """Run a test scan to verify everything works"""
    print("\n🧪 Running test scan...")
    try:
        # Import and run the scan function
        from scan_yoo_stars import main
        print("✅ Test scan completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Test scan failed: {e}")
        print("This might be due to missing credentials or network issues.")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check credentials
    if not check_credentials():
        print("\nWould you like me to create a .env file template? (y/n): ", end="")
        if input().lower().startswith('y'):
            create_env_file()
        print("\nPlease set up your credentials and run this script again.")
        return
    
    # Run test scan
    print("\n🎯 Everything is set up! Running a test scan...")
    if run_test_scan():
        print("\n🎉 Setup complete! Your bot is ready to use.")
        print("\nNext steps:")
        print("1. Edit .env file with your credentials")
        print("2. Run: python telegram_admin_dm_bot.py")
        print("3. Or run: python scan_yoo_stars.py")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("Please check your credentials and try again.")

if __name__ == "__main__":
    main()
