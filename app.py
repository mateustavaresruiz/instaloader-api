from flask import Flask, request, jsonify
import requests
import re
import json

app = Flask(__name__)

def get_followers(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        match = re.search(r"window\._sharedData = (.*?);</script>", response.text)
        if match:
            data = json.loads(match.group(1))
            followers = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
            return followers
        else:
            raise Exception("Não foi possível extrair os dados da página.")
    else:
        raise Exception(f"Erro HTTP {response.status_code} acessando o perfil.")

@app.route('/followers', methods=['GET'])
def followers():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Parâmetro 'username' é obrigatório."}), 400

    try:
        followers_count = get_followers(username)
        return jsonify({"username": username, "followers": followers_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
