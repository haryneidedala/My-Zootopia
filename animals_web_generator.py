import json


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def print_animal_info(animals_data):
    """ Prints information about each animal """
    for animal in animals_data:
        print("Name:", animal.get("name", ""))

        if "diet" in animal:
            print("Diet:", animal["diet"])

        if "locations" in animal and animal["locations"]:
            print("Location:", animal["locations"][0])

        if "type" in animal:
            print("Type:", animal["type"])

        print()  # Add empty line between animals


# Load and print the data
animals_data = load_data('animals_data.json')
print_animal_info(animals_data)
