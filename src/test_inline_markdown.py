import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
    )

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        test_cases = [
            {
                "old_nodes": [TextNode("This is a **bold** text.", text_type_text)],
                "delimiter": "**",
                "text_type": text_type_bold,
                "expected_nodes": [
                    TextNode("This is a ", text_type_text),
                    TextNode("bold", text_type_bold),
                    TextNode(" text.", text_type_text),
                ],
            },
            {
                "old_nodes": [TextNode("This is an _italic_ text.", text_type_text)],
                "delimiter": "_",
                "text_type": text_type_italic,
                "expected_nodes": [
                    TextNode("This is an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" text.", text_type_text),
                ],
            },
            {
                "old_nodes": [TextNode("This is a `code`", text_type_text)],
                "delimiter": "`",
                "text_type": text_type_code,
                "expected_nodes": [
                    TextNode("This is a ", text_type_text),
                    TextNode("code", text_type_code),
                ],
            },
            {
                "old_nodes": [TextNode("This is a **bold** text. With **another**.", text_type_text)],
                "delimiter": "**",
                "text_type": text_type_bold,
                "expected_nodes": [
                    TextNode("This is a ", text_type_text),
                    TextNode("bold", text_type_bold),
                    TextNode(" text. With ", text_type_text),
                    TextNode("another", text_type_bold),
                    TextNode(".", text_type_text)
                ],
            },
        ]
        for test_case in test_cases:
            actual_nodes = split_nodes_delimiter(
                test_case["old_nodes"],
                test_case["delimiter"],
                test_case["text_type"],
            )
            self.assertEqual(actual_nodes, test_case["expected_nodes"])

    def test_extract_markdown_images(self):
        test_cases = [
            {
                "text": "This is text with an ![image](https://i.imgur.com/image1.png) and ![another](https://i.imgur.com/image2.png)",
                "expected_images": [
                    ("image", "https://i.imgur.com/image1.png"),
                    ("another", "https://i.imgur.com/image2.png"),
                ],
            },
        ]
        for test_case in test_cases:
            actual_images = extract_markdown_images(test_case["text"])
            self.assertEqual(actual_images, test_case["expected_images"])

    def test_extract_markdown_links(self):
        test_cases = [
            {
                "text": "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
                "expected_links": [
                    ("link", "https://www.example.com"),
                    ("another", "https://www.example.com/another"),
                ]
            }
]
        for test_case in test_cases:
            actual_links = extract_markdown_links(test_case["text"])
            self.assertEqual(actual_links, test_case["expected_links"])

    def test_split_nodes_link(self):
        test_cases = [
            {
                "old_nodes": [
                    TextNode(
                        "This text contains a [link](https://youtube.com) and [another link](https://twitch.tv) with some words at the end",
                        text_type_text,
                    )
                ],
                "expected_nodes": [
                    TextNode("This text contains a ", text_type_text),
                    TextNode("link", text_type_link, "https://youtube.com"),
                    TextNode(" and ", text_type_text),
                    TextNode("another link", text_type_link, "https://twitch.tv"),
                    TextNode(" with some words at the end", text_type_text)
                ],
            },
        ]
        for test_case in test_cases:
            actual_nodes = split_nodes_link(test_case["old_nodes"])
            self.assertEqual(actual_nodes, test_case["expected_nodes"])

    def test_split_nodes_image(self):
        test_cases = [
            {
                "old_nodes": [
                    TextNode(
                        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                        text_type_text,
                    )
                ],
                "expected_nodes": [
                    TextNode("This is text with an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and another ", text_type_text),
                    TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ],
            },
        ]
        for test_case in test_cases:
            actual_nodes = split_nodes_image(test_case["old_nodes"])
            self.assertEqual(actual_nodes, test_case["expected_nodes"])

    def test_text_to_testnodes(self):
        test_cases = [
            {
                "text": 
                    "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
                ,
                "expected_nodes": [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                    ]
            }
        ]
        for test_case in test_cases:
            actual_nodes = text_to_textnodes(test_case["text"])
            self.assertEqual(actual_nodes, test_case["expected_nodes"])

if __name__ == "__main__":
    unittest.main()
