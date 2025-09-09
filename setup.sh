#!/bin/bash

# ReadRSS Lite Quick Setup Script
# Hướng dẫn thiết lập nhanh ReadRSS Lite

echo "🚀 ReadRSS Lite - Quick Setup Script"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the repository root directory"
    exit 1
fi

# Function to ask yes/no questions
ask_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

echo "📋 This script will help you set up ReadRSS Lite for free hosting"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" 2>/dev/null; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

# Install dependencies
if ask_yes_no "📦 Install Python dependencies?"; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        echo "💡 Try running: pip3 install --user -r requirements.txt"
    fi
fi

# Create .env file
if ask_yes_no "⚙️  Create .env configuration file?"; then
    if [ -f "src/.env" ]; then
        echo "⚠️  .env file already exists"
        if ask_yes_no "Overwrite existing .env file?"; then
            rm src/.env
        else
            echo "Keeping existing .env file"
        fi
    fi
    
    if [ ! -f "src/.env" ]; then
        echo "Creating .env file..."
        echo "# ReadRSS Lite Configuration" > src/.env
        echo "# Get your Discord bot token from: https://discord.com/developers/applications" >> src/.env
        echo "DISCORD_TOKEN=your_bot_token_here" >> src/.env
        echo "" >> src/.env
        echo "# Firebase credentials (optional)" >> src/.env
        echo "FIREBASE_CREDENTIALS=your_firebase_json_here" >> src/.env
        echo "✅ Created src/.env file"
        echo "📝 Please edit src/.env and add your Discord bot token"
    fi
fi

# Test setup
if ask_yes_no "🧪 Run setup test?"; then
    echo "Running setup test..."
    python3 test_setup.py
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "📖 Next steps:"
echo "1. Edit src/.env and add your Discord bot token"
echo "2. Choose a hosting platform:"
echo "   - GitHub Actions (recommended for free hosting)"
echo "   - Railway (500 hours/month free)"
echo "   - Render (free tier available)"
echo "   - Replit (always-on with ping system)"
echo ""
echo "3. Read the detailed guide: HOSTING_GUIDE.md"
echo "4. For local testing, run: cd src && python main.py"
echo ""
echo "🔗 Useful links:"
echo "   - Discord Developer Portal: https://discord.com/developers/applications"
echo "   - Firebase Console: https://console.firebase.google.com/"
echo "   - Hosting Guide: ./HOSTING_GUIDE.md"
echo ""
echo "Happy hosting! 🤖✨"