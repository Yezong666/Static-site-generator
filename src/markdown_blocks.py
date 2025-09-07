from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from splits import text_to_textnodes
from htmlnode import text_node_to_html_node
from textnode import TextType, TextNode

class BlockType(Enum):
    paragraph = "p"
    heading = "#"
    code = "```"
    quote = ">"
    unordered_list = "- "
    ordered_list = "n. "



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for i in range(0, len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] != "":
            final_blocks.append(blocks[i])
    return final_blocks

def block_to_type(block_markdown):
    if block_markdown[0] == "#":
        return BlockType.heading
    if block_markdown[0:3] == "```" and block_markdown[-3:] == "```":
        return BlockType.code
    if block_markdown[0] == ">":
        i = 0
        quote = True
        while i < len(block_markdown):
            if block_markdown[i] == "\n":
                if i + 1 < len(block_markdown):
                    if block_markdown[i+1] != ">":
                        quote = False
            i+=1
        if quote == True:
            return BlockType.quote
    if block_markdown[0:2] == "- ":
        i = 0
        unorderedlist = True
        while i < len(block_markdown):
            if block_markdown[i] == "\n":
                if i + 2 < len(block_markdown):
                    s = block_markdown[i+1] + block_markdown[i+2]
                    if block_markdown[i+1:i+3] != "- ":
                        unorderedlist = False
            i+=1
        if unorderedlist == True:
            return BlockType.unordered_list
    if block_markdown[0:3] == "1. ":
        i = 0
        ordered_list = True
        n = 2
        while i < len(block_markdown):
            if block_markdown[i] == "\n":
                if i + 3 < len(block_markdown):
                    if block_markdown[i+1:i+4] != (str(n) + ". "):
                        ordered_list = False
                    else:
                        n+=1
            i+=1
        if ordered_list == True:
            return BlockType.ordered_list
    return BlockType.paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_list = []
    for block in blocks:
        blocktype = block_to_type(block)
        if blocktype == BlockType.quote:
            nodes = text_to_textnodes(TextNode(block, TextType.TEXT))
            nodes[0].text = nodes[0].text[2:]
            child_nodes = []
            for node in nodes:
                child_nodes.append(text_node_to_html_node(node))
            block_list.append(ParentNode("blockquote", child_nodes))
        elif blocktype == BlockType.unordered_list:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                childs = []
                nodes = text_to_textnodes(TextNode(line[2:], TextType.TEXT))
                for node in nodes:
                    childs.append(text_node_to_html_node(node))
                child_nodes.append(ParentNode("li", childs))
            block_list.append(ParentNode("ul", child_nodes))
        elif blocktype == BlockType.ordered_list:
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                childs = []
                nodes = text_to_textnodes(TextNode(line[3:], TextType.TEXT))
                for node in nodes:
                    childs.append(text_node_to_html_node(node))
                child_nodes.append(ParentNode("li", childs))
            block_list.append(ParentNode("ol", child_nodes))
        elif blocktype == BlockType.code:
            block_list.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(block[4:-3], TextType.TEXT))])]))
        elif blocktype == BlockType.heading:
            i = 0
            while block[i] == "#":
                i+=1
            nodes = text_to_textnodes(TextNode(block[i+1:], TextType.TEXT))
            child_nodes = []
            for node in nodes:
                child_nodes.append(text_node_to_html_node(node))
            block_list.append(ParentNode(f"h{i}", child_nodes))
        elif blocktype == BlockType.paragraph:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            nodes = text_to_textnodes(TextNode(paragraph, TextType.TEXT))
            child_nodes = []
            for node in nodes:
                child_nodes.append(text_node_to_html_node(node))
            block_list.append(ParentNode("p", child_nodes))
    return ParentNode("div", block_list)

def extract_title(markdown):
    lines = markdown.split("\n")
    s = ""

    for line in lines:
        i = 0
        while i < len(line):
            if line[i] == "#":
                if i+1 < len(line):
                    if line[i+1] == " ":
                        return line[i+2:]
                    else:
                        break
            i+=1
    raise Exception("No header")