from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_chat_completion():
    # Obtenir la clé API de l'environnement
    api_key = os.getenv('GROQ_API_KEY')

    # Obtenir la question posée via le paramètre 'ask' dans l'URL
    question = request.args.get('ask', default="Citer les différents types de paludisme avec explication détaillée")

    # Créer une instance du client Groq avec la clé API
    client = Groq(api_key=api_key)

    # Obtenir la réponse de l'IA
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collecter la réponse
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    # Ajouter le titre au début de la réponse
    response = "🧑‍🤝‍🧑 ⚾Bruno Rak⚾ 🧑‍🤝‍🧑\n\n" + response

    # Ajouter le lien Facebook à la fin de la réponse
    response += "\n\nSi vous êtes intéressé, voici le lien vers le profil Facebook du créateur de cette API de chat : https://www.facebook.com/bruno.rakotomalala.7549"

    # Renvoyer la réponse sous forme de JSON
    return jsonify({"response": response})

if __name__ == '__main__':
    # Démarrer l'application Flask sur 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
