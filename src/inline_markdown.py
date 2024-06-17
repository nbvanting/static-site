import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: str
    ) -> list[TextNode]:
    """
    Splits a list of nodes based on a delimiter and returns a new list of 
    nodes with markdown formatted based on the text type.
    """
    new_nodes = []
    for old_node in old_nodes:
        if isinstance(old_node, TextNode):
            if old_node.text_type != text_type_text:
                new_nodes.append(old_node)
                continue
            split_nodes = []
            split_string = old_node.text.split(delimiter)
            if len(split_string) % 2 == 0:
                raise ValueError("Invalid delimiter usage. Formatted section not closed.")
            for i, value in enumerate(split_string):
                if value == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(value, text_type_text))
                else:
                    split_nodes.append(TextNode(value, text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of nodes based on an image and returns a new list of TextNodes with images split
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes
    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits a list of nodes based on a link and returns a new list of TextNodes with links split
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def extract_markdown_images(text: str) -> list:
    """
    Extracts markdown formatted images from a string and returns a list of tuples
    containing the image source and alt text.
    """
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    images = re.findall(image_regex, text)
    return images

def extract_markdown_links(text: str) -> list:
    """
    Extracts markdown formatted links from a string and returns a list of tuples
    containing the link source and alt text.
    """
    link_regex = r"\[(.*?)\]\((.*?)\)"
    links = re.findall(link_regex, text)
    return links

def text_to_textnodes(text: str) -> list[TextNode]:
    """
        Converts a string to a list of TextNodes based on the text type
    """
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes