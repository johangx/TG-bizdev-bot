#!/usr/bin/env python3
"""
Quick Start Script for Telegram Business Development Bot

This script helps you get started quickly with the bot by:
1. Checking dependencies
2. Setting up credentials
3. Testing basic functionality
4. Providing usage examples

The bot is designed to help business development teams by:
- Finding channel administrators and owners
- Discovering associated community chats and discussion groups
- Extracting contact information from Telegram channels
- Automating outreach to discovered contacts
- Exporting data to Google Sheets for organized tracking

Author: Johan
License: MIT
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def print_banner():
    """Print the bot banner"""
    print("=" * 60)
    print("🚀 TELEGRAM BUSINESS DEVELOPMENT BOT")
    print("=" * 60)
    print("🤖 Automate your Telegram outreach for business development")
    print("🔍 Find channel admins and associated community chats")
    print("📱 Send direct messages to discovered contacts")
    print("📊 Export data to Google Sheets for organized tracking")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_credentials():
    """Check if credentials are set up"""
    print("\n🔑 Checking credentials...")
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Load and check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        telegram_api_id = os.getenv('TELEGRAM_API_ID')
        telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
        
        if telegram_api_id and telegram_api_hash:
            print("✅ Telegram API credentials found")
        else:
            print("❌ Telegram API credentials missing from .env file")
            print("   Please add TELEGRAM_API_ID and TELEGRAM_API_HASH")
            return False
    else:
        print("❌ .env file not found")
        print("   Please create .env file with your credentials")
        return False
    
    # Check for Google Sheets credentials
    service_account_file = Path("service_account.json")
    if service_account_file.exists():
        print("✅ Google Sheets service account file found")
    else:
        print("⚠️  Google Sheets service account file not found")
        print("   You can still use the bot without Google Sheets integration")
    
    return True

def show_usage_examples():
    """Show usage examples"""
    print("\n📖 USAGE EXAMPLES")
    print("=" * 40)
    
    print("\n🔍 Scan channels for admins and community chats:")
    print("   python telegram_admin_dm_bot.py")
    
    print("\n💬 Find community chats for specific channels:")
    print("   python community_chat_finder.py")
    
    print("\n📱 Send messages to users:")
    print("   python send_gm_message_to_users.py")
    
    print("\n📊 Update Google Sheets:")
    print("   python sheets_update_final.py")
    
    print("\n🔍 Scan specific channels:")
    print("   python scan_yoo_stars.py")

def show_capabilities():
    """Show bot capabilities"""
    print("\n🚀 BOT CAPABILITIES")
    print("=" * 40)
    
    capabilities = [
        "🔍 Admin Detection - Find channel administrators and owners",
        "💬 Community Chat Discovery - Identify linked discussion groups",
        "📱 Direct Messaging - Send personalized outreach messages",
        "📊 Google Sheets Integration - Export data in organized format",
        "🌐 Multi-language Support - Process content in various languages",
        "⚡ Smart Contact Mapping - Map contacts to correct channels",
        "🔄 Rate Limit Handling - Built-in delays for API compliance"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print("\n🎯 Perfect for business development teams who need to:")
    print("   • Find decision-makers in target industries")
    print("   • Discover community engagement opportunities")
    print("   • Map out the full ecosystem around channels")
    print("   • Identify multiple contact points for outreach")

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check credentials
    if not check_credentials():
        print("\n📝 SETUP INSTRUCTIONS:")
        print("1. Create a .env file with your Telegram API credentials")
        print("2. Get API credentials from https://my.telegram.org/")
        print("3. For Google Sheets integration, add service_account.json")
        print("4. Run this script again")
        return
    
    print("\n🎉 SETUP COMPLETE!")
    print("Your bot is ready to use!")
    
    # Show capabilities and usage
    show_capabilities()
    show_usage_examples()
    
    print("\n" + "=" * 60)
    print("🚀 Ready to automate your Telegram business development!")
    print("=" * 60)

if __name__ == "__main__":
    main()
