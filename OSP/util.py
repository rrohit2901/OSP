import os
import shutil

path = './Manager'
for r, d, f in os.walk(path):
    for files in f:
        f_name = os.path.join(r,files)
        shutil.move(f_name, './statics2')