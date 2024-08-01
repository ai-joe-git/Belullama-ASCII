import os
import sys
import requests
import json
import time
from colorama import init, Fore, Style

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    header = "Belullama Terminal Chat"
    print(Fore.CYAN + "=" * 80)
    print(Fore.CYAN + header.center(80))
    print(Fore.CYAN + "=" * 80)

def get_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = response.json()['models']
        return [model['name'] for model in models]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {str(e)}")
        return []

def select_model():
    available_models = get_available_models()
    
    while True:
        print("\nAvailable models:")
        for i, model in enumerate(available_models, 1):
            print(f"  {i}. {model}")
        print(f"  {len(available_models) + 1}. Pull a new model")
        
        choice = input("\nSelect a model number or enter a new model name to pull: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(available_models):
            return available_models[int(choice) - 1]
        elif choice.isdigit() and int(choice) == len(available_models) + 1:
            new_model = input("Enter the name of the model to pull: ").strip()
            if new_model and not new_model.isspace():
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
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return ""

def print_help():
    print(Fore.YELLOW + "\nAvailable commands:")
    print("/bye - Exit the chat")
    print("/models - List available models")
    print("/reset - Clear the conversation history")
    print("/clear - Clear the screen")
    print("/help - Show this help message")
    print("/change - Change the current model")

def main():
    clear_screen()
    print_header()
    
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
            else:
                print(f"Unknown command: {user_input}")
            continue
        
        conversation_history.append(f"Human: {user_input}")
        full_prompt = "\n".join(conversation_history)
        
        try:
            ai_response = get_model_response(full_prompt, model)
            print_message(model, ai_response)
            conversation_history.append(f"Assistant: {ai_response}")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Unable to generate response. You may want to change the model.")
        print(Fore.CYAN + "-" * 80)

if __name__ == "__main__":
    main()