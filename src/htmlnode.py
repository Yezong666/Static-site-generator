from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception("NotImplementedError")
    
    def props_to_html(self):
        string = ""
        if self.props != None:
            i = len(self.props)
            for key in self.props:
                string += key + "=\"" + self.props[key] + "\""
                if i > 1:
                    string += " "
                    i -= 1
        return string
    
    def __repr__(self):
        string = ""
        if self.tag != None:
            string += self.tag + " "
        if self.value != None:
            string += self.value + " "
        if self.children != None:
            string += self.children + " "
        if self.props != None:
            string += self.props_to_html()
        return string

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)



    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise Exception("No tag found: ")
        if self.children == None:
            raise Exception("No children found: ")
        string =  "<" + self.tag + ">"
        for child in self.children:
            string += child.to_html()
        string += "</" + self.tag + ">"
        return string
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception(ValueError)
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {" href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src" : text_node.url,
                                    "alt" : text_node.text, })

        


