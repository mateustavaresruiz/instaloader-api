from flask import Flask, request, jsonify
import instaloader
import os

app = Flask(__name__)

# Carrega usuário e senha do Instagram das variáveis de ambiente
INSTAGRAM_USER = os.getenv('INSTAGRAM_USER')
INSTAGRAM_PASS = os.getenv('INSTAGRAM_PASS')

@app.route('/followers', methods=['GET'])
def get_followers():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username é obrigatório!"}), 400

    try:
        L = instaloader.Instaloader()

        # Login opcional se variáveis existirem
        if INSTAGRAM_USER and INSTAGRAM_PASS:
            L.login(INSTAGRAM_USER, INSTAGRAM_PASS)

        profile = instaloader.Profile.from_username(L.context, username)
        followers_count = profile.followers
        return jsonify({
            "username": username,
            "followers": followers_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))  # Default 5001
    app.run(host='0.0.0.0', port=port)
