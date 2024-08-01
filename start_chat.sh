#!/bin/bash

# Check if required Python packages are installed
REQUIRED_PKG="requests colorama"
PKG_OK=$(python3 -m pip freeze | grep -E "requests|colorama")
if [ "" = "$PKG_OK" ]; then
  echo "Installing required packages..."
  python3 -m pip install $REQUIRED_PKG
fi

# Run the chat application
python3 belullama_terminal_chat.py
