from textnode import TextType, TextNode
import re 

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    text = ""
    i = 0
    j = 0
    delim = 0
    if delimiter not in old_nodes.text:
        raise Exception("Invalid markdown synthax")
    
    while i < len(old_nodes.text):
        if old_nodes.text[i] != delimiter[j]:
            text += old_nodes.text[i]
        elif j+1 < len(delimiter):
            j+=1
        elif j+1 == len(delimiter):
            delim += 1
            j = 0
            if (delim % 2):
                if text != "":
                    nodes.append(TextNode(text, TextType.TEXT))
            else:
                nodes.append(TextNode(text, text_type))
            text = ""
        i+=1
    if text != "":
        nodes.append(TextNode(text, TextType.TEXT))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def split_nodes_link(old_nodes):
    nodes = []
    text = ""
    img = ""
    i = 0
    j = 0
    switch = 0
    while i < len(old_nodes.text):
        if old_nodes.text[i] != "[":
            text += old_nodes.text[i]
        else:
            switch = 1
            while i + j < len(old_nodes.text) and switch < 4:
                if old_nodes.text[i+j] == "]" and switch == 1:
                    switch += 1
                elif old_nodes.text[i+j] == "(" and switch == 2:
                    switch +=1
                elif old_nodes.text[i+j] == ")" and switch ==3:
                    switch+=1
                img += old_nodes.text[i+j]
                j+=1
            if switch == 4:
                if text != "":
                    nodes.append(TextNode(text, TextType.TEXT))
                img = extract_markdown_links(img)
                nodes.append(TextNode(img[0][0], TextType.LINK, img[0][1]))
                text = ""
                img = ""
                i+=j-1
            j = 0
        i+=1
    if text != "":
        nodes.append(TextNode(text, TextType.TEXT))
    return nodes

def split_nodes_image(old_nodes):
    nodes = []
    text = ""
    link = ""
    i = 0
    j = 0
    switch = 0
    while i < len(old_nodes.text):
        if old_nodes.text[i] != "!":
            text += old_nodes.text[i]
        else:
            switch = 1
            while i + j < len(old_nodes.text) and switch < 5:
                if old_nodes.text[i+j] == "[" and switch == 1:
                    switch += 1
                elif old_nodes.text[i+j] == "]" and switch == 2:
                    switch += 1
                elif old_nodes.text[i+j] == "(" and switch == 3:
                    switch +=1
                elif old_nodes.text[i+j] == ")" and switch ==4:
                    switch+=1
                link += old_nodes.text[i+j]
                j+=1
            if switch == 5:
                if text != "":
                    nodes.append(TextNode(text, TextType.TEXT))
                link = extract_markdown_images(link)
                nodes.append(TextNode(link[0][0], TextType.IMAGE, link[0][1]))
                text = ""
                link = ""
                i+=j-1
            else:
                text += old_nodes.text[i]
            j = 0
        i+=1
    if text != "":
        nodes.append(TextNode(text, TextType.TEXT))
    return nodes

def text_to_textnodes(text):
    final_nodes = []
    string = ""
    string2 = ""
    i = 0
    j = 0
    switch = 0
    while i < len(text.text):
        if text.text[i] == "_":
            j = i + 1
            string2 += text.text[i]
            while text.text[j] != "_":
                string2 += text.text[j]
                j+=1
            if text.text[j] == "_":
                string += string2 + "_"
                nodes = split_nodes_delimiter(TextNode(string, TextType.TEXT), "_", TextType.ITALIC)
                for node in nodes:
                    final_nodes.append(node)
                i=j +1
                string = ""
                string2 = ""
        elif text.text[i] == "`":
            j = i + 1
            string2 += text.text[i]
            while text.text[j] != "`":
                string2 += text.text[j]
                j+=1
            if text.text[j] == "`":
                string+= string2 +  "`"
                nodes = split_nodes_delimiter(TextNode(string, TextType.TEXT), "`", TextType.CODE)
                for node in nodes:
                    final_nodes.append(node)
                i=j +1
                string = ""
                string2 = ""
        elif text.text[i] == "*" and text.text[i+1] == "*":
            j = i + 2
            string2 += "**"
            while text.text[j] != "*":
                string2 += text.text[j]
                j+=1
            if text.text[j] == "*" and text.text[j+1] == "*":
                string += string2 + "**"
                j+=2
                nodes = split_nodes_delimiter(TextNode(string, TextType.TEXT), "**", TextType.BOLD)
                for node in nodes:
                    final_nodes.append(node)
                
                i=j
                string = ""
                string2 = ""
                
        elif text.text[i] == "!":
            final_nodes.append(TextNode(string, TextType.TEXT))
            string2 += text.text[i]
            j+=1
            switch = 1
            while i + j < len(text.text) and switch < 5:
                if text.text[i+j] == "[" and switch == 1:
                    switch += 1
                elif text.text[i+j] == "]" and switch == 2:
                    switch += 1
                elif text.text[i+j] == "(" and switch == 3:
                    switch +=1
                elif text.text[i+j] == ")" and switch ==4:
                    switch+=1
                string2 += text.text[i+j]
                j+=1
            if switch == 5:
                nodes = split_nodes_image(TextNode(string2, TextType.TEXT))
                for node in nodes:
                    final_nodes.append(node)
                i+=j-1
                string = ""
                string2 = ""
        elif text.text[i] == "[":
            final_nodes.append(TextNode(string, TextType.TEXT))
            string2 += text.text[i]
            switch = 1
            while i + j < len(text.text) and switch < 4:
                if text.text[i+j] == "]" and switch == 1:
                    switch += 1
                elif text.text[i+j] == "(" and switch == 2:
                    switch +=1
                elif text.text[i+j] == ")" and switch ==3:
                    switch+=1
                string2 += text.text[i+j]
                j+=1
            if switch == 4:
                nodes = split_nodes_link(TextNode(string2,TextType.TEXT))
                for node in nodes:
                    final_nodes.append(node)
                string = ""
                string2 =""
                i+=j-1
        if i < len(text.text):
            string += text.text[i]  
        j = 0
        i+=1
    if string != "":
        final_nodes.append(TextNode(string, TextType.TEXT))
   
    return final_nodes



