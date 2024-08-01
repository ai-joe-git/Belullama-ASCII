import os
import sys
import requests
import time
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

OLLAMA_URL = "http://localhost:11434"
LOG_FILE = "/tmp/ollama_server.log"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    header = "Belullama Terminal Chat"
    print(Fore.CYAN + "=" * 80)
    print(Fore.CYAN + header.center(80))
    print(Fore.CYAN + "=" * 80)

def check_ollama_connection():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_ollama():
    try:
        with open(LOG_FILE, "w") as log_file:
            subprocess.Popen(["ollama", "start"], stdout=log_file, stderr=log_file)
        print(Fore.GREEN + "Ollama service started.")
    except subprocess.SubprocessError as e:
        print(Fore.RED + f"Failed to start Ollama service: {str(e)}")

def stop_ollama():
    try:
        with open(LOG_FILE, "w") as log_file:
            subprocess.Popen(["ollama", "stop"], stdout=log_file, stderr=log_file)
        print(Fore.RED + "Ollama service stopped.")
    except subprocess.SubprocessError as e:
        print(Fore.RED + f"Failed to stop Ollama service: {str(e)}")

def get_available_models():
    if not check_ollama_connection():
        print(Fore.YELLOW + "Warning: Unable to connect to Ollama server.")
        return []
    
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        response.raise_for_status()
        models = response.json()['models']
        return [model['name'] for model in models]
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"Error fetching models: {str(e)}")
        return []

def pull_model(model_name):
    try:
        response = requests.post(f"{OLLAMA_URL}/api/models/pull", json={"model_name": model_name})
        response.raise_for_status()
        print(Fore.GREEN + f"Model '{model_name}' pulled successfully.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to pull model '{model_name}': {str(e)}")

def select_model():
    available_models = get_available_models()
    
    while True:
        if not available_models:
            print("\nNo available models. Please enter a custom model name.")
            new_model = input("Enter the name of the model: ").strip()
            if new_model and not new_model.isspace():
                pull_model(new_model)
                return new_model
        else:
            print("\nAvailable models:")
            for i, model in enumerate(available_models, 1):
                print(f"  {i}. {model}")
            print(f"  {len(available_models) + 1}. Enter custom model name")
            
            choice = input("\nSelect a model number or enter a new model name: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(available_models):
                return available_models[int(choice) - 1]
            elif choice.isdigit() and int(choice) == len(available_models) + 1:
                new_model = input("Enter the name of the model: ").strip()
                if new_model and not new_model.isspace():
                    pull_model(new_model)
                    return new_model
            elif choice:
                return choice
            
            print("Invalid choice. Please try again.")

def print_message(role, message):
    if role == "You":
        print(Fore.GREEN + f"{role}: {message}")
    else:
        print(Fore.BLUE + f"{role}: ", end="")
        sys.stdout.flush()
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        print()

def get_model_response(prompt, model):
    if not check_ollama_connection():
        return f"[Error] Unable to get response from Ollama. Check server connection."
    
    url = f"{OLLAMA_URL}/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"Error: {str(e)}")
        return f"[Error] Unable to get response from Ollama. Check server connection."

def print_help():
    print(Fore.YELLOW + "\nAvailable commands:")
    print("/bye - Exit the chat")
    print("/models - List available models")
    print("/reset - Clear the conversation history")
    print("/clear - Clear the screen")
    print("/help - Show this help message")
    print("/change - Change the current model")
    print("/status - Check Ollama server status")
    print("/start - Start the Ollama server")
    print("/stop - Stop the Ollama server")

def main():
    clear_screen()
    print_header()
    
    if not check_ollama_connection():
        print(Fore.YELLOW + "Warning: Unable to connect to Ollama server. Trying to start the server...")
        start_ollama()
        time.sleep(5)  # Wait for a few seconds to allow the server to start

    if not check_ollama_connection():
        print(Fore.RED + "Error: Unable to connect to Ollama server after attempting to start it.")
        return
    
    model = select_model()
    print(f"\nUsing model: {model}")
    
    conversation_history = []
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.startswith('/'):
            command = user_input[1:].lower()
            if command in ['bye', 'exit', 'quit']:
                print("Goodbye!")
                break
            elif command == 'models':
                print("\nAvailable models:")
                for model in get_available_models():
                    print(f"  - {model}")
            elif command == 'reset':
                conversation_history = []
                print("Conversation history cleared.")
            elif command == 'clear':
                clear_screen()
                print_header()
            elif command == 'help':
                print_help()
            elif command == 'change':
                model = select_model()
                print(f"\nSwitched to model: {model}")
            elif command == 'status':
                status = "Connected" if check_ollama_connection() else "Disconnected"
                print(f"Ollama server status: {status}")
            elif command == 'start':
                start_ollama()
                time.sleep(5)  # Wait for a few seconds to allow the server to start
                if not check_ollama_connection():
                    print(Fore.RED + "Error: Unable to connect to Ollama server after attempting to start it.")
            elif command == 'stop':
                stop_ollama()
            else:
                print(f"Unknown command: {user_input}")
            continue
        
        conversation_history.append(f"Human: {user_input}")
        full_prompt = "\n".join(conversation_history)
        
        ai_response = get_model_response(full_prompt, model)
        print_message(model, ai_response)
        conversation_history.append(f"Assistant: {ai_response}")
        print(Fore.CYAN + "-" * 80)

if __name__ == "__main__":
    main()