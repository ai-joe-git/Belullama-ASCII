import os
import sys
import requests
import time
import subprocess
import threading
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from tqdm import tqdm

init(autoreset=True)

OLLAMA_URL = "http://localhost:11434"
LOG_FILE = "/tmp/ollama_server.log"
TIMEOUT = 240  # Increased timeout duration

class OllamaTerminalChat:
    def __init__(self):
        self.model = None
        self.conversation_history = []
        self.stop_spinner = False
        self.command_completer = WordCompleter(
            ['/bye', '/models', '/reset', '/clear', '/help', '/change', '/status', '/start', '/stop'],
            ignore_case=True
        )
        self.command_history = InMemoryHistory()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        header = "Belullama Terminal Chat"
        print(Fore.CYAN + "=" * 80)
        print(Fore.CYAN + header.center(80))
        print(Fore.CYAN + "=" * 80)

    def check_ollama_connection(self):
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False

    def start_ollama(self):
        try:
            with open(LOG_FILE, "w") as log_file:
                subprocess.Popen(["ollama", "start"], stdout=log_file, stderr=log_file)
            print(Fore.GREEN + "Ollama service started.")
        except subprocess.SubprocessError as e:
            print(Fore.RED + f"Failed to start Ollama service: {str(e)}")

    def stop_ollama(self):
        try:
            with open(LOG_FILE, "w") as log_file:
                subprocess.Popen(["ollama", "stop"], stdout=log_file, stderr=log_file)
            print(Fore.RED + "Ollama service stopped.")
        except subprocess.SubprocessError as e:
            print(Fore.RED + f"Failed to stop Ollama service: {str(e)}")

    def get_available_models(self):
        if not self.check_ollama_connection():
            print(Fore.YELLOW + "Warning: Unable to connect to Ollama server.")
            return []
        
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
            models = response.json()['models']
            return [model['name'] for model in models]
        except requests.RequestException as e:
            print(Fore.YELLOW + f"Error fetching models: {str(e)}")
            return []

    def pull_model(self, model_name):
        try:
            with tqdm(total=100, desc=f"Pulling model {model_name}", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                for _ in range(100):
                    time.sleep(0.1)  # Simulate progress
                    pbar.update(1)

            response = requests.post(f"{OLLAMA_URL}/api/models/pull", json={"model_name": model_name})
            response.raise_for_status()
            print(Fore.GREEN + f"Model '{model_name}' pulled successfully.")
        except requests.RequestException as e:
            print(Fore.RED + f"Failed to pull model '{model_name}': {str(e)}")

    def select_model(self):
        available_models = self.get_available_models()
        
        while True:
            if not available_models:
                print("\nNo available models. Please enter a custom model name.")
                new_model = input("Enter the name of the model: ").strip()
                if new_model:
                    self.pull_model(new_model)
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
                    if new_model:
                        self.pull_model(new_model)
                        return new_model
                elif choice:
                    return choice
                
                print("Invalid choice. Please try again.")

    def print_message(self, role, message):
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

    def spinner(self):
        while not self.stop_spinner:
            for cursor in '|/-\\':
                sys.stdout.write(cursor)
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')

    def get_model_response(self, prompt, model):
        if not self.check_ollama_connection():
            return "[Error] Unable to get response from Ollama. Check server connection."
        
        url = f"{OLLAMA_URL}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        self.stop_spinner = False
        spinner_thread = threading.Thread(target=self.spinner)
        spinner_thread.start()

        try:
            response = requests.post(url, json=data, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()['response']
        except requests.Timeout:
            return "[Error] Response took too long. Please try again later."
        except requests.RequestException as e:
            print(Fore.YELLOW + f"Error: {str(e)}")
            return "[Error] Unable to get response from Ollama. Check server connection."
        finally:
            self.stop_spinner = True
            spinner_thread.join()
            sys.stdout.write('\b')  # Clear the spinner

    def print_help(self):
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

    def main(self):
        self.clear_screen()
        self.print_header()
        
        if not self.check_ollama_connection():
            print(Fore.YELLOW + "Warning: Unable to connect to Ollama server. Trying to start the server...")
            self.start_ollama()
            time.sleep(5)  # Wait for a few seconds to allow the server to start

        if not self.check_ollama_connection():
            print(Fore.RED + "Error: Unable to connect to Ollama server after attempting to start it.")
            return
        
        self.model = self.select_model()
        print(f"\nUsing model: {self.model}")

        while True:
            user_input = prompt("\nYou: ", completer=self.command_completer, history=self.command_history).strip()
            
            if user_input.startswith('/'):
                command = user_input[1:].lower()
                if command in ['bye', 'exit', 'quit']:
                    print("Goodbye!")
                    break
                elif command == 'models':
                    print("\nAvailable models:")
                    for model in self.get_available_models():
                        print(f"  - {model}")
                elif command == 'reset':
                    self.conversation_history = []
                    print("Conversation history cleared.")
                elif command == 'clear':
                    self.clear_screen()
                    self.print_header()
                elif command == 'help':
                    self.print_help()
                elif command == 'change':
                    self.model = self.select_model()
                    print(f"\nSwitched to model: {self.model}")
                elif command == 'status':
                    status = "Connected" if self.check_ollama_connection() else "Disconnected"
                    print(f"Ollama server status: {status}")
                elif command == 'start':
                    self.start_ollama()
                    time.sleep(5)  # Wait for a few seconds to allow the server to start
                    if not self.check_ollama_connection():
                        print(Fore.RED + "Error: Unable to connect to Ollama server after attempting to start it.")
                elif command == 'stop':
                    self.stop_ollama()
                else:
                    print(f"Unknown command: {user_input}")
                continue
            
            self.conversation_history.append(f"Human: {user_input}")
            full_prompt = "\n".join(self.conversation_history)
            
            ai_response = self.get_model_response(full_prompt, self.model)
            self.print_message(self.model, ai_response)
            self.conversation_history.append(f"Assistant: {ai_response}")
            print(Fore.CYAN + "-" * 80)

if __name__ == "__main__":
    OllamaTerminalChat().main()
