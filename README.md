# Squirrel Kitchen
Use OpenAI's GPT-4 to make recipes ADHD-friendly

# What it does
1. Accepts a recipe URL or plaintext input
2. Rewrites the recipe to include a shopping list, mise-en-place bowls, and step by step instructions with formatting for times and temps.
3. Exports as markdown.

# Requirements
- python 3
- streamlit
- openai
- recipe_scrapers
- dotenv
- markdown
- json

# How to run
1. Set up your OpenAI key as an env variable if you haven't already.
2. To run, type "streamlit run streamlit.py"
