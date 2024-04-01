from dotenv import load_dotenv
load_dotenv()
import json
from scraping_processing import scrape_recipe, process_recipe_text_input, clean_instructions, string_to_array
from markdown_generation import process_recipe_into_markdown, combine_markdown, generate_shopping_list_markdown, generate_mise_en_place_markdown, generate_instructions_markdown, generate_title_markdown
from openai_prompts import get_completion, generate_recipe_summary, format_markdown_instructions, split_instructions, generate_mise_en_place, generate_shopping_list

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

