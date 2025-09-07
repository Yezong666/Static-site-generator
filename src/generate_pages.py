from markdown_blocks import extract_title, markdown_to_html_node
import os

def generate_pages_recursive(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    directory = os.listdir("content")
    to_generate = []
    for file in directory:
        if file[-3:] == ".md":
            to_generate.append((f"content/{file}",file))
        elif os.path.isdir(f"content/{file}"):
            subdir = os.listdir(f"content/{file}")
            os.mkdir(f"docs/{file}")
            for subfile in subdir:
                if subfile[-3:] == ".md":
                    to_generate.append((f"content/{file}/{subfile}",file + "/" + subfile))
                elif os.path.isdir(f"content/{file}/{subfile}"):
                    subsubdir = os.listdir(f"content/{file}/{subfile}")
                    if not os.path.exists(f"docs/{file}/{subfile}"):
                        os.mkdir(f"docs/{file}/{subfile}")
                    for subsubfile in subsubdir:
                        print(subsubfile)
                        if subsubfile[-3:] == ".md":
                            to_generate.append((f"content/{file}/{subfile}/{subsubfile}",file + "/" + subfile + "/" + subsubfile))

    directory = os.listdir("content/blog")
    for markdown in to_generate:
        content = ""
        template = ""
        with open(markdown[0]) as f:
            content = f.read()
        with open(template_path) as f:
            template = f.read()

        html_nodes = markdown_to_html_node(content)
        html = html_nodes.to_html()
        title = extract_title(content)

        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)
        template = template.replace("href=\"/", f"href=\"{basepath}")
        template = template.replace("src=\"/", f"src=\"{basepath}")

        #print(f"{dest_path}/{markdown[1][:-3]}.html")
        with open(f"{dest_path}/{markdown[1][:-3]}.html", "x") as f:
            f.write(template) 