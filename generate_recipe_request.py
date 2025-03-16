def read_ingredients_from_file(file_path):
    with open(file_path, 'r') as file:
        ingredients = file.read().splitlines()
    return ingredients


def format_ingredients_for_chatbot(ingredients):
    return "Here are the ingredients I have: " + ", ".join(ingredients) + ". Can you suggest a recipe?"


# Main process
file_path = 'fridge_ingredient.txt'
ingredients = read_ingredients_from_file(file_path)
formatted_ingredients = format_ingredients_for_chatbot(ingredients)

# Output the formatted ingredients for chatbot
print(formatted_ingredients) 