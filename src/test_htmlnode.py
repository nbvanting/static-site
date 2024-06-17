import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        """
        Generate a series of HTMLNodes and test their equality and inequality using assert methods.
        """
        node = HTMLNode("div", "hello", props={'class': 'bold'})
        node2 = HTMLNode("div", "hello", props={'class': 'bold'})
        self.assertEqual(node, node2)

        node3 = HTMLNode("div", "hello", props={'class': 'italic'})
        self.assertNotEqual(node, node3)

        node4 = HTMLNode("span", "hello", props={'class': 'bold'})
        self.assertNotEqual(node, node4)

        node5 = HTMLNode("div", "goodbye", props={'class': 'bold'})
        self.assertNotEqual(node, node5)

        node6 = HTMLNode("div", "hello", props={'class': 'bold'}, children=[HTMLNode("span", "world")])
        node7 = HTMLNode("div", "hello", props={'class': 'bold'}, children=[HTMLNode("span", "world")])
        self.assertEqual(node6, node7)

        node8 = HTMLNode("div", "hello", props={'class': 'bold'}, children=[HTMLNode("p", "world")])
        self.assertNotEqual(node6, node8)

        node9 = HTMLNode(None, None, None, props={"href": "https://www.boot.dev", "target": "_blank"}).props_to_html()
        test_string = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node9, test_string)


class TestLeafNode(unittest.TestCase):

    def test_init(self):
        node = LeafNode("hello")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.props, None)

        node2 = LeafNode("goodbye", "span", {"class": "bold"})
        self.assertEqual(node2.value, "goodbye")
        self.assertEqual(node2.tag, "span")
        self.assertEqual(node2.props, {"class": "bold"})

    def test_to_html(self):
        node = LeafNode("hello")
        self.assertEqual(node.to_html(), "hello")

        node2 = LeafNode("goodbye", "span", {"class": "bold"})
        self.assertEqual(node2.to_html(), '<span class="bold">goodbye</span>')


class TestParentNode(unittest.TestCase):

    def test_init(self):
        node = ParentNode(
        [
            LeafNode("Bold text", "b"),
            LeafNode( "Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
        ],
        "p"
        )
        test_string = node.to_html()
        self.assertEqual(test_string, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
        nested_node = ParentNode(
            [
                ParentNode(
                    [
                        LeafNode("Nested Node Text", "p")
                    ],
                    "div"
                )
            ],
            "div"
        )
        expected_html = "<div><div><p>Nested Node Text</p></div></div>"
        actual_html = nested_node.to_html()
        self.assertEqual(expected_html, actual_html)


if __name__ == "__main__":
    unittest.main()
