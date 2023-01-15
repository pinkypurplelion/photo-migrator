# Plan:
# 1. Parse the JSON data files in the directory
# 2. Parse the available images in the directory
# 3. If data file & image available, modify image data and move to new directory
# 4. Otherwise, move image/data file to new directory


# module imports
import os
import shutil
import json
import piexif


# This is my path
path = "raw"

# to store files in a list
files = os.walk(path)

data_files = []
media_files = []

# Will separate the images and data files into separate folders.
print("Separating images and data files...")
for (root, dirs, file) in files:
    for f in file:
        if '.json' in f:
            # shutil.move(os.path.join(root, f), os.path.join('data', f))
            data_files.append(f)
        else:
            # shutil.move(os.path.join(root, f), os.path.join('media', f))
            media_files.append(f)

print(data_files)
print(media_files)

print("Modifying images...")
for f in media_files:
    if f + '.json' in data_files:
        print(f + '.json')
        print("Found a match:", f)
        media_data = json.load(open(os.path.join('raw', f + '.json'))) # change to data dir for production
        print(media_data)
        exif_dict = piexif.load(os.path.join('raw', f)) # change to media dir for production
        print(exif_dict)


# for (root, dirs, file) in media_files:
#     for f in file:
#         print(f.split('.')[0] + '.json')
#         for (root, dirs, file) in data_files:
#
#
#         if (f.split('.')[0] + '.json') in data_files:
#             print("Found a match!")
#             # do something
#
#
#
# for (root, dirs, file) in data_files:
#     print()
