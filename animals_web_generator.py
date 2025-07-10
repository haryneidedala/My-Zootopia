import json
import requests


def get_user_input():
    """Prompt user for animal name.
    
    Returns:
        str: Animal name entered by user
    """
    return input("Enter a name of an animal: ").strip()


def fetch_animal_data(animal_name):
    """Fetch animal data from API.
    
    Args:
        animal_name (str): Name of animal to search for
        
    Returns:
        tuple: (list of animal dictionaries, error message if any)
    """
    try:
        # Using Wikipedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{animal_name}"
        response = requests.get(url)
        
        # Handle 404 - Not Found
        if response.status_code == 404:
            return None, f'The animal "{animal_name}" doesn\'t exist.'
        
        response.raise_for_status()
        
        data = response.json()
        
        # Sometimes Wikipedia returns disambiguation pages or other non-animal content
        if data.get("type") not in ["standard", None]:
            return None, f'"{animal_name}" doesn\'t refer to a specific animal.'
        
        # Format the data
        animal = {
            "name": data.get("title", animal_name),
            "diet": data.get("diet", "Unknown"),
            "locations": [data.get("locations", "Various")],
            "type": data.get("type", "Unknown"),
            "description": data.get("extract", "No description available")
        }
        
        return [animal], None
    
    except requests.exceptions.RequestException as e:
        return None, f'Error fetching information about "{animal_name}": {str(e)}'


def load_template(template_path):
    """Load HTML template from file.
    
    Args:
        template_path (str): Path to HTML template file
        
    Returns:
        str: Template content
    """
    with open(template_path, "r") as file:
        return file.read()


def create_error_message(animal_name, message):
    """Create HTML error message for when animal isn't found.
    
    Args:
        animal_name (str): Name of animal that wasn't found
        message (str): Error message to display
        
    Returns:
        str: HTML error message
    """
    return f'''
    <div class="error-message">
        <h2 class="error-title">Oops! {message}</h2>
        <div class="error-content">
            <p>We couldn't find information about "{animal_name}".</p>
            <p>Try searching for a different animal name.</p>
            <div class="error-image">🦄🔍</div>
        </div>
    </div>
    '''


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
    
    if "description" in animal:
        html.append(f'    <p>{animal["description"]}</p>')
    
    html.append('  </div>')
    html.append('</li>')
    
    return "\n".join(html)


def generate_animals_html(animals_data, error_message=None):
    """Generate HTML content.
    
    Args:
        animals_data (list): List of animal dictionaries
        error_message (str): Error message if any
        
    Returns:
        str: Combined HTML content
    """
    if error_message:
        return error_message
    if not animals_data:
        return create_error_message("", "No animal information found.")
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
        # Get user input
        animal_name = get_user_input()
        
        # Fetch data from API
        animals_data, error_message = fetch_animal_data(animal_name)
        
        # Load template
        template_content = load_template("animals_template.html")
        
        # Generate HTML content
        if error_message:
            animals_html = create_error_message(animal_name, error_message)
        else:
            animals_html = generate_animals_html(animals_data)
            
        final_html = template_content.replace("__REPLACE_ANIMALS_INFO__", animals_html)
        
        # Save output
        save_html("animals.html", final_html)
        print(f"Website was successfully generated to the file animals.html.")
        
    except FileNotFoundError as e:
        print(f"Error: Template file not found - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
