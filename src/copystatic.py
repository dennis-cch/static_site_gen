import os
import shutil

def get_all_path(listdir, current, public):
    if not os.path.exists(public):
        os.mkdir(public)
        
    for path in listdir:
        dst_dir = os.path.join(public, path)
        src_dir = os.path.join(current, path)
        if os.path.isfile(src_dir):
            shutil.copy(src_dir, dst_dir)
        elif os.path.isdir(src_dir):
            get_all_path(os.listdir(src_dir), src_dir, dst_dir)
    return