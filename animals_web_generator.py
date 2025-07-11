#!/usr/bin/env python
# -*- coding: utf-8 -*-

import data_fetcher
import os
from dotenv import load_dotenv

# Initialize environment
load_dotenv()

# Configuration
TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"

def get_user_input():
    """Get animal name from user."""
    return input("Enter an animal name: ").strip()

def load_template():
    """Load HTML template file."""
    with open(TEMPLATE_FILE, "r", encoding='utf-8') as f:
        return f.read()

def create_error_message(animal_name, error):
    """Generate user-friendly error HTML."""
    return f'''
    <div class="error-message">
        <h2>Error: {error}</h2>
        <p>Couldn't find information about "{animal_name}"</p>
        <p>Please try another animal name</p>
    </div>
    '''

def serialize_animal(animal):
    """Convert animal data to HTML."""
    characteristics = animal.get('characteristics', {})
    return f'''
    <li class="animal-card">
        <h2>{animal.get('name', 'Unknown')}</h2>
        <div class="animal-details">
            {f'<p><strong>Diet:</strong> {characteristics.get("diet")}</p>' if characteristics.get("diet") else ''}
            {f'<p><strong>Location:</strong> {animal["locations"][0]}</p>' if animal.get("locations") else ''}
            {f'<p><strong>Type:</strong> {characteristics.get("type")}</p>' if characteristics.get("type") else ''}
            {f'<p>{characteristics.get("description")}</p>' if characteristics.get("description") else ''}
        </div>
    </li>
    '''.strip()

def generate_html(animals, error=None):
    """Generate complete HTML content."""
    if error:
        return create_error_message("", error)
    if not animals:
        return create_error_message("", "No animals found")
    return "\n".join(serialize_animal(a) for a in animals)

def save_html(content):
    """Save HTML to file."""
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(content)

def main():
    """Main program flow."""
    try:
        # Get input and fetch data
        animal = get_user_input()
        animals, error = data_fetcher.fetch_data(animal)
        
        # Generate and save HTML
        template = load_template()
        animals_html = generate_html(animals, error)
        output = template.replace("__REPLACE_ANIMALS_INFO__", animals_html)
        save_html(output)
        
        print(f"Success! Website saved to {OUTPUT_FILE}")
        
    except FileNotFoundError:
        print(f"Error: Could not find template file {TEMPLATE_FILE}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
