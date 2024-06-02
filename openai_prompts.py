from openai import OpenAI
import re
import json

client = OpenAI()

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def generate_recipe_summary(ingredients,instructions):
    prompt = f"""
    You are trying to help someone who is deciding whether to do a recipe. They would \
    like to understand what's involved in the recipe without having to read through \
    it fully. Summarize what what's involved in making this recipe in 2-3 sentences \
    and keep it high level and easy to understand. \
    INGREDIENTS: ```{ingredients}``` \
    INSTRUCTIONS: ```{instructions}``` \
    Your response should only be the summary and no extra text beyond that.
    """
    response = get_completion(prompt)
    return response

def format_markdown_instructions(markdown_instructions):
 
    example1 = f"""'Preheat oven to 300°.' would become 'Preheat oven to 🔥 **300°**.'"""

    example2 = f"""''Heat 2 Tbsp. oil in a large ovenproof skillet over medium-high.' \
    would become 'Heat `2 Tbsp. oil` in a large ovenproof skillet over 🔥 **medium-high**.'"""
    
    example3 = f"""'Add Swiss chard ribs and stems, shallot, and ginger and cook, \
    stirring occasionally, until shallot is softened but not browned, about 3 minutes.' \
    would become 'Add `Swiss chard ribs and stems`, `shallot`, and `ginger` and cook, \
    stirring occasionally, until `shallot` is softened but not browned, about ⏳ **3 minutes**.'"""
 
    prompt=f"""Your goal is to take the set of markdown cooking instructions, \
    denoted within <cooking_instructions> tags, and apply the following formatting \
    to them: \
    For any ingredient mentioned, apply code backticks formatting. \
    For any cooking time OR temperature mentioned, apply bold formatting. \
    For any temperature mentioned (whether in degrees, °, or low/medium/high), \
    prepend a fire moji (🔥). \
    For any cooking time mentioned, prepend an hourglass emoji (⏳). \
    Follow the examples denoted within the <example1>,<example2>, and <example3>tags. \
    <cooking_instructions>{markdown_instructions}</cooking_instructions> \
    <example1>{example1}</example1> \
    <example2>{example2}</example2> \
    <example3>{example3}</example3> \
    Do not include any tags in your response -- only provide the edited markdown with \
    no other text.
    """

    response = get_completion(prompt)
    return response

def split_instructions(instructions):
    instructions_sentences = []
    instructions_json = []

    for instruction in instructions:
        
        prompt = f"""Split the following recipe instructions into sentences, with each sentence on \
        a new line: ```{instruction}```\
        Do not include any backticks in your response; only the content itself."""
        
        response = get_completion(prompt)
        split_instruction = response.strip().split('\n')
        instructions_sentences.extend(split_instruction)
        
        # For each sentence, create an object and add it to the instructions_json list
        for sentence in split_instruction:
            instruction_object = {"instruction": sentence}
            instructions_json.append(instruction_object)

    # Optionally, convert the instructions_json list to a JSON string
    instructions_json_str = json.dumps(instructions_json, indent=4)
    
    return instructions_sentences, instructions_json_str

def generate_mise_en_place(ingredients, instructions):
    # Join the ingredients and instructions into a single string
    prompt= f"""Based on the following recipe, enumerate the 'mise en place' steps, \
    organizing the ingredients into prep bowls. Each cooking step is an object in a JSON \
    array. Where a cooking step involves multiple ingredients, those ingredients can be \
    prepped into the same bowl.\
    ```INGREDIENTS: \
    {ingredients} \
     INSTRUCTIONS in JSON format: \
     {instructions}``` \
     Respond only in JSON. Do not include the word JSON nor any backticks. \
     Your JSON array should contain objects, each representing a \
     prep bowl, with the following keys: 'prepBowlNumber' which holds a numeric value \
     indicating the sequence number of the prep bowl, and 'ingredients' which has an \
     array of strings, each representing an ingredient included in the 'prep bowl'."""
    
    response = get_completion(prompt)
    return response

def generate_shopping_list(ingredients):
    prompt=f"""Categorize this ingredient list into “staples” and “non-staples” \
    and then within the non-staples group, categorize by grocery store aisle, using \
    the best fit from the list of aisles provided. In your final output, make sure \
    to include the full ingredient with measurements. \
    It should be in JSON dictionary with a key 'ingredients' that points to a list \
    of 'ingredient' dictionaries, each with keys of “ingredient” and “isStaple” \
    (true or false) and “aisle”. Do not include anything else in your answer besides \
    the JSON itself. Do not include the word JSON nor any triple backticks. Just the JSON content.\
    Categorize as staples any of the following: Salt, pepper, seasonings, olive oil, butter, \
    vegetable oil, soy sauce, fish sauce, flour, sugar, baking soda, baking powder. \
    DO NOT categorize as staples anything that is a vegetable or protein.\
    POSSIBLE AISLES (delimited by single backticks): \
    `Chips, Crackers, & Oils`, `Produce`, `Cheese`, `Eggs & Non-Cheese Dairy`, \
    `Meat`, `Baking`, `Canned Food`, `Nuts, Spices, & Bulk`, `Alcohol` \
    ```INGREDIENTS: {ingredients}```"""

    response = get_completion(prompt)
    return response


    from recipe_scrapers import scrape_me