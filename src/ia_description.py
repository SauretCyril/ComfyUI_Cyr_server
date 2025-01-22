import torch
import numpy as np
from fpdf import FPDF
import json
from flask import Blueprint, request, jsonify
import logging
import src.files  as files
import src.default as default
from flask import Flask
from openai import OpenAI
IA = Blueprint('IA', __name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# get_answer
@IA.route('/get_answer', methods=['POST'])
def extract_job_text():
    try:
        logger.debug(f"dbg003.Request method: {request.method}")
        brute = request.json.get('brute')
        #RQ = request.json.get('RQ')
        logger.debug(f"dbg004.Received file path: {brute}")
        #logger.debug(f"dbg004.Received RQ: {RQ}")

        if not brute :
            logger.error("Er005.Missing description path or question")
            return jsonify({'Er005': 'Missing job file path or question'}), 400

        # Notify front-end that processing has started
        #yield jsonify({'message': 'Processing started'}), 202

        # Extraction rapide du texte
        #text1 = fil.load_desc_file(file)
        
        
      

        formated = convert( brute)
        logger.debug(f"dbg005.Generated answer: {formated}")

        return jsonify({
            'raw_text': brute,
            'formatted_text': formated
        })

    except Exception as e:
        logger.error(f"Er007.Error: {str(e)}")
        return jsonify({'Er007': str(e)}), 500
    
    
    
    
    
def convert( context=""):
    try:
        client = OpenAI()  # Assurez-vous que OPENAI_API_KEY est défini dans vos variables d'environnement
        full_context = f"""le Format json  : \n{default.default_prompt()} : la description doit être découpée en eléments correspondant au clé json : qualité,sujets,sujets.face, sujet.hair,clothes... 
                        par exemple pour 
                        - clothes il faut décrire quels vétements porte le sujet, 
                        - sujet : il faut dire si le sujet est une femme ou un homme ou plusieurs personnage.... 
                        - sujet.hair : il faut décrire la couleur des cheveux, la coupe de cheveux, si le sujet est chauve ou non...
                        - sujet.face : il faut décrire les oreilles, la bouche, la gorge, la tête...
                        - sujet.tatoos : il faut décrire les tatouages, leur couleur, leur forme, la date de création...
                        - sujet.jewelry : il faut décrire les bijoux, leur couleur, leur forme, leur matière...
                        - ainssi de suite pour chaque clé du fichier  : \n\nContexte:\n{context}"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en analyse morphologie et sociologique de photo, ton objectifs est de décomposer une image en description pour chaque élément la composant en fonction des clés qui te sont transmisent"},
                {"role": "user", "content": full_context}
            ],
            temperature=0.8,
            max_tokens=1100
        )
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Erreur lors de l'analyse: {str(e)}")
        return f"Une erreur s'est produite: {str(e)}"