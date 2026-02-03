"""
HTML export functionality for word search books.

This module provides functionality to generate HTML descriptions
for word search books.
"""

import os


def generate_html_description(output_path, title, description, categories=None, catchphrase="xxxxxx"):
    """
    Generates an HTML file with the title and description of the book using a template.
    
    Args:
        output_path: Path where the HTML file should be saved
        title: Title of the book
        description: Description of the book (can be a string or list of strings)
        categories: List of tuples [(category_title, [word1, word2, word3, word4]), ...]
                   First 7 categories from the input file with first 4 words each
    """
    print("Generating HTML description...")
    print(f"Title: {title}")
    print(f"Description: {description}")
    
    # Get the template path (relative to the project root)
    # Assuming this script is in src/wordsearch/, the template is at data/templates/description.html
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "templates",
        "description.html"
    )
    
    # Read the template file
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Warning: Template file not found at {template_path}")
        print("Using default HTML template")
        html_content = "<b>{TITLE}</b><p>{Descriptions}</p>"
    
    # Convert description to string if it's a list
    if isinstance(description, list):
        description_text = ", ".join(description)
    else:
        description_text = description
    
    # Replace placeholders
    html_content = html_content.replace("{TITLE}", title.upper())
    html_content = html_content.replace("{title}", title.lower())
    html_content = html_content.replace("{Descriptions}", description_text.title())
    html_content = html_content.replace("{catchphrase}", catchphrase)
    # Generate category list HTML
    if categories:
        category_list_html = ""
        for category_title, words in categories:
            # Join first 4 words with commas in Title Case
            words_text = ", ".join([word.title() for word in words[:4]])
            category_list_html += f'\t<li><b>{category_title.title()}</b>: {words_text}</li>\n'
        html_content = html_content.replace("{category_list}", category_list_html.rstrip('\n'))
    else:
        # If no categories provided, remove the placeholder
        html_content = html_content.replace("{category_list}", "")
    
    # Write the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML description generated: {output_path}")
