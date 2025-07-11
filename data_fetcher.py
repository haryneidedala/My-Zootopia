#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
API_KEY = os.getenv('API_KEY')
WIKIPEDIA_API_URL = os.getenv('WIKIPEDIA_API_URL')

def fetch_data(animal_name):
    """
    Fetches animal data from API.
    
    Args:
        animal_name (str): Name of animal to search for
        
    Returns:
        tuple: (list of animal dicts, error message if any)
    """
    try:
        # Configure API request
        headers = {'Authorization': f'Bearer {API_KEY}'} if API_KEY else {}
        url = f"{WIKIPEDIA_API_URL}{animal_name}"
        
        # Make API call
        response = requests.get(url, headers=headers)
        
        # Handle responses
        if response.status_code == 404:
            return None, f'Animal "{animal_name}" not found'
        
        response.raise_for_status()
        data = response.json()
        
        # Validate response type
        if data.get("type") not in ["standard", None]:
            return None, f'"{animal_name}" is not a specific animal'
        
        # Format response
        animal = {
            'name': data.get('title', animal_name),
            'taxonomy': {
                'kingdom': 'Animalia',
                'phylum': 'Chordata',
                'class': 'Mammalia'
            },
            'locations': [data.get('locations', 'Various')],
            'characteristics': {
                'diet': data.get('diet', 'Unknown'),
                'type': data.get('type', 'Unknown'),
                'description': data.get('extract', 'No description available')
            }
        }
        
        return [animal], None
    
    except requests.exceptions.RequestException as e:
        return None, f'API error: {str(e)}'
