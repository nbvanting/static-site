from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
class TextNode:
    def __init__(self, text: str, text_type: str, url: None | str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    """
    Convert a text node to an HTML node based on its text type, and return the corresponding LeafNode.
    
    Args:
        text_node: The text node to be converted to an HTML node.
    
    Returns:
        A LeafNode representing the HTML node corresponding to the text node.
    
    Raises:
        ValueError: If the text type of the text node is invalid.
    """
    if text_node.text_type == text_type_text:
        return LeafNode(text_node.text, None)
    if text_node.text_type == text_type_bold:
        return LeafNode(text_node.text, "b")
    if text_node.text_type == text_type_italic:
        return LeafNode(text_node.text, "i")
    if text_node.text_type == text_type_code:
        return LeafNode(text_node.text, "code")
    if text_node.text_type == text_type_link:
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

