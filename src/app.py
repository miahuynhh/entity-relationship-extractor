"""
Flask Web Server for Entity Relationship Visualizer

This module provides a web interface for the entity relationship extraction system.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_relationship_extractor import EnhancedRelationshipExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize the relationship extractor
try:
    relationship_extractor = EnhancedRelationshipExtractor()
    logger.info("Enhanced relationship extractor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize relationship extractor: {e}")
    relationship_extractor = None


@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        return f"Error loading page: {str(e)}", 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        return jsonify({
            'status': 'ok',
            'message': 'Entity Relationship Visualizer API is running',
            'extractor_ready': relationship_extractor is not None
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze text and return entities and relationships."""
    try:
        # Check if extractor is available
        if relationship_extractor is None:
            return jsonify({
                'error': 'Relationship extractor not available'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400
        
        # Extract text from request
        text = data.get('text', '').strip()
        if not text:
            return jsonify({
                'error': 'No text provided'
            }), 400
        
        # Validate text length
        if len(text) > 10000:  # Reasonable limit
            return jsonify({
                'error': 'Text too long (maximum 10,000 characters)'
            }), 400
        
        logger.info(f"Analyzing text: {text[:100]}...")
        
        # Extract relationships using existing backend
        relationships = relationship_extractor.extract_relationships(text)
        
        # Format response
        response_data = {
            'success': True,
            'text': text,
            'relationships': relationships,
            'count': len(relationships)
        }
        
        logger.info(f"Analysis complete: {len(relationships)} relationships found")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info("Starting Entity Relationship Visualizer web server...")
    logger.info("Server will be available at: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
