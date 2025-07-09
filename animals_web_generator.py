import json

def load_data(file_path):
    """Loads a JSON file"""
    with open(file_path, "r") as handle:
        return json.load(handle)

def load_template(template_path):
    """Loads the HTML template"""
    with open(template_path, "r") as handle:
        return handle.read()

def generate_animals_html(animals_data):
    """Generates HTML cards for all animals"""
    html_cards = ""
    for animal in animals_data:
        # Start each card
        card_html = '<li class="cards__item">\n'
        card_html += '  <div class="card">\n'
        card_html += f'    <h2 class="card__title">{animal.get("name", "")}</h2>\n'
        card_html += '    <div class="card__text">\n'
        
        # Add animal details
        if "diet" in animal:
            card_html += f'      <p><strong>Diet:</strong> {animal["diet"]}</p>\n'
            
        if "locations" in animal and animal["locations"]:
            card_html += f'      <p><strong>Location:</strong> {animal["locations"][0]}</p>\n'
            
        if "type" in animal:
            card_html += f'      <p><strong>Type:</strong> {animal["type"]}</p>\n'
        
        # Close card tags
        card_html += '    </div>\n'
        card_html += '  </div>\n'
        card_html += '</li>\n\n'
        
        html_cards += card_html
    
    return html_cards

def save_html(output_path, content):
    """Saves the HTML content to a file"""
    with open(output_path, "w") as handle:
        handle.write(content)

# Main execution
animals_data = load_data("animals_data.json")
template_content = load_template("animals_template.html")

# Generate animals HTML cards and replace the placeholder
animals_html = generate_animals_html(animals_data)
final_html = template_content.replace("__REPLACE_ANIMALS_INFO__", animals_html)

# Save the result
save_html("animals.html", final_html)

print("HTML file generated successfully as animals.html")
