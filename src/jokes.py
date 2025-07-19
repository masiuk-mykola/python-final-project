import requests
from colorama import Fore, init
import constants
init(autoreset=True)

def get_joke():
    try:
        response = requests.get(constants.random_joke_url)
        response.raise_for_status() 
        data = response.json()
        print(f"⚠️{Fore.RED} \033[1m{data['setup']}\033[1m⚠️")
        print(f"🤣{Fore.LIGHTMAGENTA_EX}\033[1m{data['punchline']}\033[1m🤣")
        
    except requests.RequestException as e:
        print(f"Помилка при запиті: {e}")
    

