import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        split_nodes = []
        split_text = node.text.split(delimiter)
        if len(split_text)%2 == 0:
            raise ValueError ("invalid markdown, formatted section not closed")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i %2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))
        new_node.extend(split_nodes)
    return new_node

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_node = []
    for node in old_nodes:
        split_nodes = []
        if extract_markdown_images(node.text) == [] or node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        images = extract_markdown_images(node.text)
        original_text = node.text
        for image_alt, image_link in images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            original_text = sections[1]
            if sections[0] == "":
                split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                continue
            split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        if sections[1] != "":
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_node.extend(split_nodes)
    return new_node

def split_nodes_link(old_nodes):
    new_node = []
    for node in old_nodes:
        split_nodes = []
        if extract_markdown_links(node.text) == [] or node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        links = extract_markdown_links(node.text)
        original_text = node.text
        for link_alt, link_link in links:
            sections = original_text.split(f"[{link_alt}]({link_link})", 1)
            original_text = sections[1]
            if sections[0] == "":
                split_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
                continue
            split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
        if sections[1] != "":
            split_nodes.append(TextNode(sections[1], TextType.TEXT))
        new_node.extend(split_nodes)
    return new_node