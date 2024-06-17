import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)

class TestBlockMarkdown(unittest.TestCase):
    """
        Test Block Markdown Case
    """
    def test_markdown_to_blocks(self):
        """
            Test markdown_to_blocks
        """
        test_cases = [
            {
                "document": """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
""",

                "expected": 
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items",
                ]
            },
            {
                "document": """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line





* This is a list
* with items
""",

                "expected": 
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items",
                ]
            }
        ]
        for test_case in test_cases:
            actual = markdown_to_blocks(test_case["document"])
            self.assertEqual(actual, test_case["expected"])

    def test_block_to_block_type(self):
        """
            Test block_to_block_type
        """
        test_cases = [
            {
                "block": block_to_block_type("This is a text node"),
                "expected": block_type_paragraph
            },
            {
                "block": block_to_block_type("### This is a heading"),
                "expected": block_type_heading
            },
            {
                "block": block_to_block_type("```\nThis is a code block\n```"),
                "expected": block_type_code
            },
            {
                "block": block_to_block_type("> This is a quote\n> more quotes"),
                "expected": block_type_quote
            },
            {
                "block": block_to_block_type("* This is an unordered list\n* with items"),
                "expected": block_type_unordered_list
            },
            {
                "block": block_to_block_type("1. This is an ordered list\n2. with items"),
                "expected": block_type_ordered_list
            }
        ]
        for test_case in test_cases:
            actual = test_case["block"]
            self.assertEqual(actual, test_case["expected"])


    def test_markdown_to_html_node(self):
        """
            Test markdown_to_html_node
        """
        test_cases = [
            {
                "document": """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items
""",
                "expected": 
                """<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"""
            },
            {
                "document": """
This is a paragraph
```
This is a code block
```
This is another paragraph
""",
                "expected": 
                """<div><p>This is a paragraph <code> This is a code block </code> This is another paragraph</p></div>"""
            }
        ]
        for test_case in test_cases:
            actual = markdown_to_html_node(test_case["document"])
            self.assertEqual(actual.to_html(), test_case["expected"])

if __name__ == "__main__":
    unittest.main()
