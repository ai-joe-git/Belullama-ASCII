#!/bin/bash

# Define virtual environment directory
VENV_DIR=".venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

pip install requests
pip install colorama
pip install prompt_toolkit
pip install tqdm
# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Check if required Python packages are installed
REQUIRED_PKG="requests colorama prompt_toolkit tqdm"
PKG_OK=$(pip freeze | grep -E "requests|colorama|prompt_toolkit|tqdm")
if [ "" = "$PKG_OK" ]; then
  echo "Installing required packages..."
  pip install $REQUIRED_PKG
fi

# Run the chat application
python belullama_terminal_chat.py

