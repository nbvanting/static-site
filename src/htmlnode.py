class HTMLNode:
    """
        Represents an HTML node.
    """
    def __init__(
            self,
            tag: None | str = None,
            value: None | str = None,
            children: None | list = None,
            props: None | dict = None
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """
            Converts the HTMLNode to a string of HTML
        """
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        """
            Converts the props dictionary to a string of HTML attributes
        """
        if self.props:
            return ' ' + ' '.join([f'{key}="{value}"' for key, value in self.props.items()])
        else:
            return ''

    def __repr__(self) -> str:
        """
            Returns a string representation of the HTMLNode
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props



class LeafNode(HTMLNode):
    """
        Represents a leaf node in the HTML tree.
    """
    def __init__(self, value: str, tag: None | str = None, props: None | dict = None) -> None:
        super().__init__(tag=tag, value=value, props=props)
        self.value = value
        self.tag = tag
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """
        Represents a parent node in the HTML tree.
    """
    def __init__(self,  children: list, tag: None | str = None, props: None | dict = None) -> None:
        super().__init__(children=children, tag=tag, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
