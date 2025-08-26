#!/bin/bash

# Harry Potter Invisibility Cloak - Setup Script
# Automatically installs dependencies and sets up the project

echo "🪄 Welcome to Harry Potter Invisibility Cloak Setup!"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment (optional but recommended)
echo "🔧 Creating virtual environment..."
python3 -m venv invisibility_cloak_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source invisibility_cloak_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing required packages..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Quick Start Guide:"
echo "===================="
echo "1. Activate virtual environment: source invisibility_cloak_env/bin/activate"
echo "2. Run GUI version: python invisibility_cloak_gui.py"
echo "3. Or run simple version: python simple_cloak.py"
echo "4. Or calibrate colors first: python color_calibrator.py"
echo ""
echo "🎬 Enjoy your magical invisibility cloak experience!"
echo ""
echo "Need help? Check the README.md file for detailed instructions."
