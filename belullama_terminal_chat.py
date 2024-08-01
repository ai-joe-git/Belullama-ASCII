import os
import time
import requests
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    header = """
  ____  _ _                         
 / __ \| | |                        
| |  | | | | __ _ _ __ ___   __ _   
| |  | | | |/ _` | '_ ` _ \ / _` |  
| |__| | | | (_| | | | | | | (_| |  
 \____/|_|_|\__,_|_| |_| |_|\__,_|  
    (Using Qwen2 model)
    """
    print(header)

def print_chat_interface(chat_history, input_buffer):
    clear_screen()
    print_header()
    print("\n" + "=" * 60 + "\n")

    for sender, message in chat_history:
        if sender == "You":
            print(f"┌───── You ─────┐")
        else:
            print(f"┌───── Qwen2 ─────┐")
        
        words = message.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 58:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            print(f"│ {line:<58} │")
        print(f"└{'─' * 60}┘\n")

    print("\n" + "=" * 60)
    print("┌───── Input ─────┐")
    print(f"│ {input_buffer:<58} │")
    print("└" + "─" * 60 + "┘")

def get_qwen2_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2",
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            return f"Error: Unable to get response from Qwen2. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to connect to Ollama. Make sure it's running. Details: {str(e)}"

def main():
    chat_history = []
    input_buffer = ""
    
    while True:
        print_chat_interface(chat_history, input_buffer)
        
        char = input()
        if char == '\n':
            if input_buffer.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            
            chat_history.append(("You", input_buffer))
            
            print("\nQwen2 is thinking", end="", flush=True)
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print("\n")
            
            ai_response = get_qwen2_response(input_buffer)
            chat_history.append(("Qwen2", ai_response))
            
            input_buffer = ""
        else:
            input_buffer += char

if __name__ == "__main__":
    main()
