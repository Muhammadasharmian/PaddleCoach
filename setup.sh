#!/bin/bash
# Setup script for PaddleCoach

echo "=========================================="
echo "PaddleCoach Setup"
echo "=========================================="

# Check Python version
python3 --version

# Create virtual environment
echo -e "\n1. Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo -e "\n2. Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\n3. Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo -e "\n4. Installing dependencies..."
pip install ultralytics opencv-python numpy Pillow

echo -e "\n=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To process the video, run:"
echo "  python process_video.py"
echo ""
echo "=========================================="
