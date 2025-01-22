import os
import json
from dotenv import load_dotenv
import os
load_dotenv()
def load_prompt_file(prompt_file):
    if os.path.exists(prompt_file):
        with open(prompt_file) as json_file:
           return json.load(json_file)
    else :
        chaine="a so nicely cat"
    return chaine


def load_desc_file(text_file):
    file_path = os.path.join(os.getenv('YOUR_ENV_VARIABLE_NAME'), text_file)
   
    if os.path.exists(text_file):
        with open(text_file, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return "File does not exist"

def save_prt_to_json(filepath,prompt):
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(prompt, json_file, ensure_ascii=False, indent=4)