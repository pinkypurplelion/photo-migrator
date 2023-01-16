# Plan:
# 1. Parse the JSON data files in the directory
# 2. Parse the available images in the directory
# 3. If data file & image available, modify image data and move to new directory
# 4. Otherwise, move image/data file to new directory

# Readme:
# the raw files: /raw
#
#
#


# module imports
import os
import shutil
import json
import piexif
import datetime
import math


# This is my path
PATH_RAW = "raw"
PATH_DATA = "data"
PATH_MEDIA = "media"
PATH_FINAL = "final"

# to store files in a list
path_raw_files = os.walk(PATH_RAW)

data_files = []
media_files = []

# Will separate the images and data files into separate folders (PATH_DATA & PATH_MEDIA) from the PATH_RAW directory
print("Separating images and data files...")
for (root, dirs, file) in path_raw_files:
    for f in file:
        if '.json' in f:
            shutil.move(os.path.join(root, f), os.path.join('data', f))
            data_files.append(f)
        else:
            shutil.move(os.path.join(root, f), os.path.join('media', f))
            media_files.append(f)

# Walks the media & data files and adds any existing files
path_media_files = os.walk(PATH_MEDIA)
path_data_files = os.walk(PATH_DATA)
for (root, dirs, file) in path_media_files:
    for f in file:
        if '.json' in f:
            data_files.append(f)
        else:
            media_files.append(f)

for (root, dirs, file) in path_data_files:
    for f in file:
        if '.json' in f:
            data_files.append(f)
        else:
            media_files.append(f)


print(data_files)
print(media_files)

def degToDmsRational(deg_float):
    minFloat = deg_float % 1 * 60
    secFloat = minFloat % 1 * 60
    deg = math.floor(deg_float)
    min = math.floor(minFloat)
    sec = round(secFloat * 100)

    deg = abs(deg) * 1
    min = abs(min) * 1
    sec = abs(sec) * 1

    return ((deg, 1), (min, 1), (sec, 100))



print("Modifying images...")
for f in media_files:
    if '.jpg' in f.lower() and f + '.json' in data_files:
        print(f + '.json')
        print("Found a match:", f)
        media_data = json.load(open(os.path.join('data', f + '.json'))) # change to data dir for production
        data_title = media_data.get('title', '')
        data_photo_time = media_data.get('photoTakenTime', '')
        data_location = media_data.get('geoData', '')
        print(data_title, data_photo_time, data_location)

        exif_dict = piexif.load(os.path.join('media', f)) # change to media dir for production
        print(piexif.dump(exif_dict))
        print(exif_dict)
        exif_dict['0th'][270] = data_title
        dt = datetime.datetime.fromtimestamp(int(data_photo_time['timestamp']))
        dt_str = dt.strftime("%y:%m:%d %H:%M:%S")
        exif_dict['0th'][306] = dt_str
        exif_dict['Exif'][36867] = dt_str
        exif_dict['Exif'][36868] = dt_str
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N'
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'E'
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = degToDmsRational(data_location['latitude'])
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = degToDmsRational(data_location['longitude'])

        print(exif_dict)
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, os.path.join('media', f))

        shutil.move(os.path.join('media', f), os.path.join('final', 'media', f))
        shutil.move(os.path.join('data', f + '.json'), os.path.join('final', 'data', f + '.json'))
    else:
        print("No match found for:", f)



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
