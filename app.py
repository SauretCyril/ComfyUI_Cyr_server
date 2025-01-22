from flask import Flask, request, jsonify
import json
import src.files as files
import src.default as default
import src.texte as texte
import src.ia_description as IA_desc
import warnings
import torch
import numpy as np
warnings.filterwarnings("ignore", category=UserWarning)
app = Flask(__name__)









class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, torch.Tensor):
            return obj.detach().cpu().numpy().tolist()
        return super(NumpyEncoder, self).default(obj)

app.json_encoder = NumpyEncoder  # Ajouter cette ligne après la création de l'app


@app.route('/alive')
def alive():
    return jsonify({'message': 'Im alive'}), 200





@app.route('/prompt', methods=['POST'])
async def get_prompt():
    data = request.json
    name = data.get('name', 'default')  # Default to 'default' if name is not provided
    is_file = data.get('is_file', False)
    chaine = []
    if not is_file: 
        chaine = texte.set_prompt(default.default_prompt())
    else:
       values_file = files.load_prompt_file(name + ".json")
       chaine = texte.set_prompt(values_file)
        
    
    return jsonify({"prompt": chaine, "name": name})

@app.route('/caracteriser', methods=['POST'])
async def description_brute():
    data = request.json
    desc = data.get('description')
    if not desc:
       return jsonify({'error': 'Missing file path'}), 400
    
    result = await IA_desc.convert(desc)
    return jsonify({'text': result})




if __name__ == '__main__':
    import requests
    import time

    # Example of calling get_prompt with parameters name and is_file
    #save_prt_to_json('prt.json')
    app.run(debug=True)

    # Wait for the server to start
    time.sleep(2)

    # Call the /caracteriser route with the parameter "une jolie femme"
    response = requests.post('http://localhost:5000/caracteriser', json={'brute': 'une jolie femme'})
    print(response.json())



