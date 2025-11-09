from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_ls = os.listdir(dir_path_content)
    for file_path in dir_path_ls:
        file_path = Path(os.path.join(dir_path_content, file_path))
        if os.path.isdir(file_path):
            nested_dest_dir_path = Path(os.path.join(dest_dir_path, file_path.name))
            generate_pages_recursive(file_path, template_path, nested_dest_dir_path)
        if file_path.suffix == ".md":
            from_file = open(file_path, "r")
            markdown_content = from_file.read()
            from_file.close()

            template_file = open(template_path, "r")
            template = template_file.read()
            template_file.close()

            node = markdown_to_html_node(markdown_content)
            html = node.to_html()

            title = extract_title(markdown_content)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)

            dest_dir_path = Path(os.path.join(dest_dir_path, file_path.name))
            dest_dir_path = dest_dir_path.with_suffix(".html")
            if dest_dir_path.parent != "":
                os.makedirs(dest_dir_path.parent, exist_ok=True)
            to_file = open(dest_dir_path, "w")
            to_file.write(template)
        
def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")