from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

# Twitter API credentials
CONSUMER_KEY = 'BK3pCwZ4Yy2fSNzY0opq3AMZw'
CONSUMER_SECRET = 'hisdCz0jSKlS0fER6X2x7pedY2WiXq44B64aqxzRcu7VxSIm3f'

def generate_bearer_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        data = 'grant_type=client_credentials'

        response = requests.post('https://api.twitter.com/oauth2/token', headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            print(f'Token generation error: {response.text}')
            return None
    except Exception as e:
        print(f'Error generating token: {str(e)}')
        return None

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Generate fresh bearer token for each request
        bearer_token = generate_bearer_token()
        if not bearer_token:
            return jsonify({'error': 'Failed to generate bearer token'}), 500

        url = f'https://api.twitter.com/2/users/by/username/{username}?user.fields=public_metrics'
        headers = {'Authorization': f'Bearer {bearer_token}'}
        
        response = requests.get(url, headers=headers)
        print(f"Twitter API response for {username}: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            follower_count = data['data']['public_metrics']['followers_count']
            return jsonify({'followers_count': follower_count})
        else:
            return jsonify({'error': f'Twitter API error: {response.status_code}'}), response.status_code

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)