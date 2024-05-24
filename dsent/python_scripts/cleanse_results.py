
import os
import shutil
import sys

for root, dirs, files, in os.walk(sys.argv[1]):
    for file_name in files:
        if 'config.json' in file_name or 'system.pc.com_1.device' in file_name:
            f_path = os.path.join(root,file_name)
            print(f'removing {file_name} ({f_path})')
            os.remove(f_path)
    for dir_name in dirs:
        if 'fs' in dir_name:
            dir_path = os.path.join(root,dir_name)
            print(f'removing {dir_path}')
            shutil.rmtree(dir_path)
