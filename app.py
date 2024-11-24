from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': 'Text required'}), 400

        # Analyze sentiment using TextBlob
        analysis = TextBlob(text)
        
        # Get polarity score (-1 to 1)
        score = analysis.sentiment.polarity
        
        # Get subjectivity
        subjectivity = analysis.sentiment.subjectivity
        
        # Generate analysis text
        analysis_text = self.generate_analysis_text(score, subjectivity)
        
        return jsonify({
            'score': score,
            'subjectivity': subjectivity,
            'analysis': analysis_text
        })

    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return jsonify({'error': str(e)}), 500

def generate_analysis_text(score, subjectivity):
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    confidence = "high" if abs(score) > 0.6 else "moderate" if abs(score) > 0.3 else "low"
    tone = "very subjective" if subjectivity > 0.8 else "somewhat subjective" if subjectivity > 0.4 else "objective"
    
    return f"This tweet appears {sentiment} with {confidence} confidence. The tone is {tone}."

if __name__ == '__main__':
    app.run(debug=True)