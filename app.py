from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        print(f"Received request for username: {username}")  # Debug log 1

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        cdn_url = f'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={username}'
        print(f"Requesting URL: {cdn_url}")  # Debug log 2
        
        response = requests.get(cdn_url)
        print(f"Raw CDN response: {response.text}")  # Debug log 3
        print(f"Response status code: {response.status_code}")  # Debug log 4

        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON data: {data}")  # Debug log 5
            
            if data and len(data) > 0:
                follower_count = data[0]['followers_count']
                print(f"Extracted follower count: {follower_count}")  # Debug log 6
                return jsonify({'followers_count': follower_count})
            
        return jsonify({'error': 'Failed to fetch follower count'}), response.status_code

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)