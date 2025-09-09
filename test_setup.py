#!/usr/bin/env python3
"""
Simple test script to verify bot configuration
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test environment setup"""
    print("🔍 Testing environment setup...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check required files
    required_files = [
        'main.py',
        'bot_runner.py',
        '../requirements.txt',
        '../.github/workflows/run-bot.yml',
        '../.github/workflows/keep-bot-alive.yml'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Check environment variables (if .env exists)
    if os.path.exists('.env'):
        print("✅ .env file found")
        with open('.env', 'r') as f:
            content = f.read()
            if 'DISCORD_TOKEN' in content:
                print("✅ DISCORD_TOKEN configured")
            else:
                print("⚠️  DISCORD_TOKEN not found in .env")
    else:
        print("⚠️  .env file not found (normal for production)")
    
    # Test imports
    try:
        import nextcord
        print(f"✅ nextcord available")
    except ImportError:
        print("❌ nextcord not installed")
        return False
    
    try:
        import flask
        print(f"✅ flask available")
    except ImportError:
        print("❌ flask not installed")
        return False
    
    print("\n🎉 Environment test completed!")
    return True

def test_bot_structure():
    """Test bot code structure"""
    print("\n🔍 Testing bot structure...")
    
    # Check directories
    required_dirs = ['cogs', 'dal', 'dto', 'bll', 'gui', 'utils']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False
    
    # Check main components
    try:
        import main
        print("✅ main.py can be imported")
    except Exception as e:
        print(f"❌ main.py import failed: {e}")
        return False
    
    print("\n🎉 Bot structure test completed!")
    return True

def main():
    """Run all tests"""
    print("🚀 ReadRSS Lite Setup Test")
    print("=" * 40)
    
    # Change to src directory if not already there
    if not os.path.exists('main.py'):
        if os.path.exists('src/main.py'):
            os.chdir('src')
            print("📁 Changed to src directory")
        else:
            print("❌ Could not find main.py")
            sys.exit(1)
    
    env_ok = test_environment()
    structure_ok = test_bot_structure()
    
    if env_ok and structure_ok:
        print("\n🎉 All tests passed! Bot setup is ready.")
        print("\n📖 Next steps:")
        print("1. Set up environment variables (DISCORD_TOKEN, FIREBASE_CREDENTIALS)")
        print("2. Choose a hosting platform (GitHub Actions, Railway, Render, Replit)")
        print("3. Follow the hosting guide in HOSTING_GUIDE.md")
        return True
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)