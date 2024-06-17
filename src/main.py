import os
import shutil
import logging

from copy_static import copy_files_recursive
from generate_page import generate_pages_recursive

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"

def main() -> None:
    if os.path.exists(DIR_PATH_PUBLIC):
        logging.info("Deleting public directory...")
        shutil.rmtree(DIR_PATH_PUBLIC)
    
    logging.info("Copying static files to public directory...")
    copy_files_recursive(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    logging.info("Generating index.html...")
    generate_pages_recursive(
        DIR_PATH_CONTENT,
        TEMPLATE_PATH,
        DIR_PATH_PUBLIC
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()