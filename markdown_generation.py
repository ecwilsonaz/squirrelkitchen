def process_recipe_into_markdown(title, ingredients, instructions):
    ingredients, instructions = map(string_to_array, [ingredients, instructions])
    recipe_summary = generate_recipe_summary(ingredients, instructions)

    markdown_parts = [
        generate_title_markdown(title, recipe_summary),
        generate_shopping_list_markdown(json.loads(generate_shopping_list(ingredients))),
        generate_mise_en_place_markdown(json.loads(generate_mise_en_place(ingredients, split_instructions(clean_instructions(instructions))[1]))),
        format_markdown_instructions(generate_instructions_markdown(split_instructions(clean_instructions(instructions))[0]))
    ]

    return combine_markdown(*markdown_parts)

def combine_markdown(*markdown_vars):
    return '\n\n'.join('\n'.join(line.strip() for line in markdown_content.split('\n') if line.strip()) for markdown_content in markdown_vars).rstrip('\n')

def generate_shopping_list_markdown(shopping_list):
    staples, aisles = organize_ingredients_by_aisle(shopping_list["ingredients"])
    markdown_output = "## Shopping List\n\n"
    markdown_output += generate_staples_markdown(staples) if staples else ""
    markdown_output += generate_aisles_markdown(aisles) if aisles else ""
    return markdown_output

def organize_ingredients_by_aisle(ingredients):
    staples, aisles = [], {}
    for item in ingredients:
        (staples if item["isStaple"] else aisles.setdefault(item["aisle"], [])).append(item["ingredient"])
    return staples, aisles

def generate_staples_markdown(staples):
    return f"### Staples\n{''.join(f'- [ ] {staple}\n' for staple in staples)}\n"

def generate_aisles_markdown(aisles):
    return ''.join(f"### Main Ingredients\n#### {aisle}\n{''.join(f'- [ ] {ingredient}\n' for ingredient in ingredients)}\n" for aisle, ingredients in aisles.items())

def generate_mise_en_place_markdown(mise_en_place_steps):
    return "## Mise-en-place\n\n" + ''.join(generate_bowl_markdown(step) for step in mise_en_place_steps)

def generate_bowl_markdown(step):
    return f"### Bowl {step['prepBowlNumber']}\n{''.join(f'- [ ] {ingredient}\n' for ingredient in step['ingredients'])}\n"

def generate_instructions_markdown(instructions):
    return "## Step by Step Instructions\n" + ''.join(f"- [ ] {instruction}\n" for instruction in instructions)

def generate_title_markdown(title, recipe_summary):
    return f"# {title}\n{recipe_summary}"