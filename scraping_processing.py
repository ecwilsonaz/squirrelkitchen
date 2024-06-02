from recipe_scrapers import scrape_me
import re

def scrape_recipe(url):
    scraper = scrape_me(url, wild_mode=True)
    return scraper.title(), scraper.ingredients(), scraper.instructions().split('\n')

def process_recipe_text_input(ingredients_text, instructions_text):
    ingredients = clean_text(ingredients_text)
    instructions = clean_instructions(clean_text(instructions_text))
    return ingredients, instructions

def clean_text(text):
    return [line.strip() for line in text.split('\n') if line.strip()]

def clean_instructions(instructions):
    cleaned_instructions = []

    # Define a set of common introductory headers to remove
    intro_headers = {
        'cooking instructions', 'instructions', 'steps', 'directions', 'cooking directions', 'preparation', 'preparations'
    }

    for instruction in instructions:
        # Join instruction sentences into a single string if necessary
        if isinstance(instruction, list):
            instruction = ' '.join(instruction)

        # Convert instruction to lowercase and strip whitespace for comparison
        instruction_lower = instruction.lower().strip()

        # Check if the instruction is a common introductory header or is empty
        if instruction_lower in intro_headers or not instruction.strip():
            continue

        # Remove common prefixes such as "Step 1", "1.", "1)", "Step 1:"
        cleaned_instruction = re.sub(r'^(Step\s+)?\d+[\.\)]?\s*', '', instruction, flags=re.IGNORECASE)

        # Add the cleaned instruction to the list if it's not empty
        if cleaned_instruction.strip():
            cleaned_instructions.append(cleaned_instruction.strip())

    return cleaned_instructions

def display_recipe(title, ingredients, instructions):
    print(f"Recipe Title: {title}\n")
    print_list("Ingredients:", ingredients)
    print_list("Instructions:", instructions, numbered=True)

def print_list(title, items, numbered=False):
    print(f"{title}")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}" if numbered else f"- {item}")
    print()  # Add an empty line for better readability

def string_to_array(text):
    return [text]