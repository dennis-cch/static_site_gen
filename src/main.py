import os
import shutil
from copystatic import get_all_path
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    get_all_path(os.listdir(dir_path_static), dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
    #generate_page(
    #    os.path.join(dir_path_content, "index.md"),
    #    template_path,
    #    os.path.join(dir_path_public, "index.html"),
    #)





if __name__ == "__main__":
    main()
