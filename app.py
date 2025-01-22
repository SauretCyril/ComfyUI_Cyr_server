from flask import Flask, request, jsonify
import asyncio
import json
import os
import requests

app = Flask(__name__)

prt = {
    'qualité': {
        "scores": "(((score_9)), score_8_up, score_7_up, score_6_up), rating_explicit"
    },
    'sujets': {
        "sujet": "warrior nordic 1girl (viking:1.5)",
        'hair': 'short red hair, fluttering in the wind',
        'breast': 'tiny breast',
        'corpulence': 'skinny',
        'tatoos': 'golden intricite runes tattoos on the neck:1.9 and all over the breast:1.5',
        'face': 'pointed facial feathers',
    },
    'clothes': {
        "description": "she wears vicking style panties and crop top",
    },
    'human_poses': {
        "main_action": "walking towards the camera"
    },
    'background': {
        "background": "forest dark background:0.3",
        "light": "bokeh, gold highlights",
        "effet": "particle effects",
    },
    'camera': {
        "focused": "full length body focus",
    },
    'image': {
        "image": "voluptuous, vivid colors, cinematic still"
    }
}

def set_prompt(sub):
    chaine = ""
    for col in sub.values():
        for key, value in col.items():
            chaine += f"{value},"
    return chaine

def load_prompt_file(prompt_file):
    if os.path.exists(prompt_file):
        with open(prompt_file) as json_file:
           return json.load(json_file)
    else :
        chaine="a so nicely cat"
    return chaine


def save_prt_to_json(filepath):
    with open(filepath, 'w') as json_file:
        json.dump(prt, json_file, indent=4)

@app.route('/prompt', methods=['POST'])
async def get_prompt():
    data = request.json
    name = data.get('name', 'default')  # Default to 'default' if name is not provided
    is_file = data.get('is_file', False)
    chaines = []
    if not is_file: 
        chaine = set_prompt(prt)
    else:
       chaine = load_prompt_file(name + ".json")
        
    
    return jsonify({"prompt": chaine, "name": name})

if __name__ == '__main__':
    #save_prt_to_json('prt.json')
    app.run(debug=True)
    # Example of calling get_prompt with parameters name and is_file



