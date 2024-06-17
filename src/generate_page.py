import os
from pathlib import Path

from block_markdown import (
     markdown_to_html_node
)

def extract_title(markdown: str) -> str:
    """
        Extracts the title from a markdown string
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise ValueError("No title found. Please add a title to your markdown document.")
    
    
def generate_page(from_path: str, template_path: str, dest_path: Path) -> None:
    """
        Generates a page from a markdown document and a template
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
        Generates pages in a directory recursively
    """
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
