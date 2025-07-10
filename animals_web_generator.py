import json


def load_data(file_path):
    """Load JSON data from file.
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        dict: Parsed JSON data
    """
    with open(file_path, "r") as file:
        return json.load(file)


def load_template(template_path):
    """Load HTML template from file.
    
    Args:
        template_path (str): Path to HTML template file
        
    Returns:
        str: Template content
    """
    with open(template_path, "r") as file:
        return file.read()


def serialize_animal(animal):
    """Serialize a single animal object to HTML.
    
    Args:
        animal (dict): Animal data dictionary
        
    Returns:
        str: HTML representation of the animal
    """
    html = []
    html.append('<li class="cards__item">')
    html.append(f'  <h2 class="card__title">{animal.get("name", "")}</h2>')
    html.append('  <div class="card__text">')
    
    if "diet" in animal:
        html.append(f'    <p><strong>Diet:</strong> {animal["diet"]}</p>')
        
    if "locations" in animal and animal["locations"]:
        html.append(f'    <p><strong>Location:</strong> {animal["locations"][0]}</p>')
        
    if "type" in animal:
        html.append(f'    <p><strong>Type:</strong> {animal["type"]}</p>')
    
    html.append('  </div>')
    html.append('</li>')
    
    return "\n".join(html)


def generate_animals_html(animals_data):
    """Generate HTML for all animals.
    
    Args:
        animals_data (list): List of animal dictionaries
        
    Returns:
        str: Combined HTML for all animals
    """
    return "\n".join(serialize_animal(animal) for animal in animals_data)


def save_html(output_path, content):
    """Save HTML content to file.
    
    Args:
        output_path (str): Path to output file
        content (str): HTML content to save
    """
    with open(output_path, "w") as file:
        file.write(content)


def main():
    """Main execution function."""
    try:
        # Load data and template
        animals_data = load_data("animals_data.json")
        template_content = load_template("animals_template.html")
        
        # Generate HTML content
        animals_html = generate_animals_html(animals_data)
        final_html = template_content.replace("__REPLACE_ANIMALS_INFO__", animals_html)
        
        # Save output
        save_html("animals.html", final_html)
        print("Successfully generated animals.html")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
