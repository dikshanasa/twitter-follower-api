from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from textblob import TextBlob

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["https://x.com", "https://twitter.com"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_analysis_text(score, subjectivity):
    # Determine sentiment level
    if score > 0.6:
        sentiment = "very positive"
    elif score > 0.2:
        sentiment = "positive"
    elif score > -0.2:
        sentiment = "neutral"
    elif score > -0.6:
        sentiment = "negative"
    else:
        sentiment = "very negative"

    # Determine confidence level
    confidence = "high" if abs(score) > 0.6 else "moderate" if abs(score) > 0.3 else "low"
    
    # Determine tone based on subjectivity
    if subjectivity > 0.8:
        tone = "very emotional"
    elif subjectivity > 0.5:
        tone = "somewhat emotional"
    elif subjectivity > 0.3:
        tone = "fairly neutral"
    else:
        tone = "very objective"

    return f"This tweet appears {sentiment} with {confidence} confidence. The tone is {tone}."

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_sentiment():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'Text required'}), 400

        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        return jsonify({
            'score': score,
            'subjectivity': subjectivity,
            'analysis': generate_analysis_text(score, subjectivity)
        })

    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)