from pathlib import Path
from os.path import exists
import json

from openai import OpenAI

from utils import load_json, dump_json

# VARS

CUR_DIR = Path(__file__).parent
KEY_FILE = CUR_DIR / "keys" / "openai.key"
SETTINGS_FILE = CUR_DIR / "settings.json"
MESSAGES_FILE = CUR_DIR / "messages.json"

with open(SETTINGS_FILE, "r") as f:
  SETTINGS = json.load(f)
  SYSTEM_PROMPT: str = SETTINGS["system"]
  MODEL: str = SETTINGS["model"]

client = OpenAI(api_key=KEY_FILE.read_text())
messages = []

messages.append({"role": "system", "content": SYSTEM_PROMPT})

if exists(MESSAGES_FILE) and MESSAGES_FILE.read_text().startswith("["):
  for message in load_json(MESSAGES_FILE):
    messages.append(message)


# FUNCTIONS
def generate_message(user_message: str): 
  if not exists(MESSAGES_FILE) or len(MESSAGES_FILE.read_text()) <= 1:
    MESSAGES_FILE.touch()
    with open(MESSAGES_FILE, "w") as f:
      f.write("[]")

  messages.append({"role": "user", "content": user_message})
  
  response = client.chat.completions.create(
                  model=MODEL,
                  messages=messages,
                  max_tokens=4096,
                  temperature=0.6)

  bot_message: str = str(response.choices[0].message.content)
  messages.append({"role": "assistant", "content": bot_message})
  
  save_messages(messages)
  
  return bot_message

def save_messages(messages):
  dump_json(MESSAGES_FILE, messages[1:])
  

# TESTS
if __name__ == "__main__":
  while True:
    demand = input("User : ")

    if demand.lower() == "-quit":
      break

    print(generate_message(user_message=demand))
