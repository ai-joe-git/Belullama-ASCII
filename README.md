# Belullama-ASCII

Belullama Terminal Chat is a Python-based terminal chat application that allows users to interact with AI models served by the Ollama server. It provides functionalities to manage the Ollama server, select models, and chat interactively.

## Features

- Automatic connection to Ollama server with the option to start the server if not running.
- Ability to manually start and stop the Ollama server.
- Listing and selecting available AI models.
- Pulling new models by specifying their names.
- Interactive chat interface with a typewriter effect for AI responses.
- Command-based control to manage the chat session and server.

## Requirements

- Python 3.6+
- `requests` library
- `colorama` library

You can install the required libraries using pip:

```bash
pip install requests colorama
```

## Usage

1. Clone the repository:

```bash
git clone <repository-url>
cd belullama_terminal_chat
```

2. Ensure the Ollama server is installed and accessible.

3. Run the chat application:

```bash
python belullama_terminal_chat.py
```

### Available Commands

- `/bye` - Exit the chat
- `/models` - List available models
- `/reset` - Clear the conversation history
- `/clear` - Clear the screen
- `/help` - Show help message
- `/change` - Change the current model
- `/status` - Check Ollama server status
- `/start` - Start the Ollama server
- `/stop` - Stop the Ollama server

## Shell Script for One-click Start

A shell script `start_chat.sh` is provided for convenience. It ensures the necessary libraries are installed and starts the chat application.

### `start_chat.sh`

```bash
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
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Shell Script (`start_chat.sh`)

```bash
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
```

### Usage Instructions for the Shell Script

1. Ensure the shell script `start_chat.sh` is executable. You can make it executable with the following command:

```bash
chmod +x start_chat.sh
```

2. Run the shell script to start the chat application:

```bash
./start_chat.sh
```

These instructions and files should provide a comprehensive guide for setting up and running the Belullama Terminal Chat application from your GitHub repository.