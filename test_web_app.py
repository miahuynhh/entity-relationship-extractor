#!/usr/bin/env python3
"""
Test script for the web application
"""

import sys
import os
sys.path.append('src')

from app import app
import json

def test_web_app():
    """Test the web application functionality."""
    print("Testing Entity Relationship Visualizer Web App")
    print("=" * 50)
    
    with app.test_client() as client:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = client.get('/api/health')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        print()
        
        # Test main page
        print("2. Testing main page...")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.data)} bytes")
        print()
        
        # Test analyze endpoint with sample text
        print("3. Testing analyze endpoint...")
        sample_text = "Alan Turing was a pioneering mathematician and computer scientist from the United Kingdom."
        
        response = client.post('/api/analyze', 
                             data=json.dumps({'text': sample_text}),
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Success: {data['success']}")
            print(f"   Relationships found: {data['count']}")
            print(f"   Sample relationship: {data['relationships'][0] if data['relationships'] else 'None'}")
        else:
            print(f"   Error: {response.get_json()}")
        print()
        
        # Test analyze endpoint with empty text
        print("4. Testing analyze endpoint with empty text...")
        response = client.post('/api/analyze', 
                             data=json.dumps({'text': ''}),
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        print()
        
        print("All tests completed!")

if __name__ == "__main__":
    test_web_app()
