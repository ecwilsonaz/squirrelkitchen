from dotenv import load_dotenv
from recipe_scrapers import scrape_me
import streamlit as st
from scraping_processing import scrape_recipe, process_recipe_text_input
from main import process_recipe_into_markdown 

load_dotenv()


def main():
    st.title("Squirrel Kitchen")

    # Radio button for user to choose input type
    input_type = st.radio("Choose your input method:", ('URL', 'Manual Input'))

    if input_type == 'URL':
        # User inputs a URL
        url = st.text_input("Enter a recipe URL:")
        # Submit button for URL input
        submit_url = st.button("Make it ADHD-friendly!", key='submit_url')

        if submit_url:
            with st.spinner("Processing... Please wait up to 2 minutes"):
                title, ingredients, instructions = scrape_recipe(url)
                markdown_content = process_recipe_into_markdown(title, ingredients, instructions)
                st.code(markdown_content, language='markdown')

    elif input_type == 'Manual Input':
        # User inputs for manual entry
        title = st.text_input("Recipe Title:")
        ingredients = st.text_area("Ingredients (one per line):")
        instructions = st.text_area("Instructions (step by step):")
        # Submit button for manual input
        submit_manual = st.button("Make it ADHD-friendly!", key='submit_manual')

        if submit_manual:
            with st.spinner("Processing... Please wait up to 2 minutes"):
                ingredients, instructions = process_recipe_text_input(ingredients, instructions)
                markdown_content = process_recipe_into_markdown(title, ingredients, instructions)
                st.code(markdown_content, language='markdown')

if __name__ == "__main__":
    main()