import os
import shutil
import logging

def copy_files_recursive(source, dest):
    """
    Recursively copy all files and directories from the source directory to the
    destination directory.
    """
    if not os.path.exists(dest):
        os.mkdir(dest)
        
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(dest, item)
        logging.info("Copying %s to %s", s, d)
        if os.path.isdir(s):
            copy_files_recursive(s, d)
        else:
            shutil.copy(s, d)
