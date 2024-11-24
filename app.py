from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Use Twitter's CDN syndication API to get real follower count
        cdn_url = f'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={username}'
        response = requests.get(cdn_url)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                follower_count = data[0]['followers_count']
                print(f"Found real follower count for {username}: {follower_count}")
                return jsonify({'followers_count': follower_count})
            
        return jsonify({'error': 'Failed to fetch follower count'}), response.status_code

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500