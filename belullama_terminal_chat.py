import os
import requests
import json
import time
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 50)
    print("Ollama Chat (Using Qwen2 model)")
    print("=" * 50)

def type_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_qwen2_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2",
        "prompt": prompt,
        "stream": True
    }
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()
        print("\nQwen2:", end=" ", flush=True)
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_line = json.loads(decoded_line)
                    if 'response' in json_line:
                        type_effect(json_line['response'], delay=0.01)
                    if json_line.get('done', False):
                        break
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {decoded_line}")
        print()  # Add a newline after the response
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def main():
    clear_screen()
    print_header()
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        get_qwen2_response(user_input)
        print("-" * 50)

if __name__ == "__main__":
    main()