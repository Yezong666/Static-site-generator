from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "**Bold**"
    ITALIC = "_Italic_"
    CODE = "`Code`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, y):
        if self.text == y.text and self.text_type == y.text_type and self.url == y.url:
            return True
        return False

    def __repr__(self):
        if self.url != None:
            string = "TextNode(" + self.text + ", " + self.text_type.value + ", " + self.url + ")"
        else:
            string = "TextNode(" + self.text + ", " + self.text_type.value + ")"
        
        return string


