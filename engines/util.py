import math
import shutil
import os


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


def move_completed_files(media_path, data_path, final_path, file):
    shutil.move(os.path.join(media_path, file), os.path.join(final_path, 'media', file))
    shutil.move(os.path.join(data_path, file + '.json'), os.path.join('final', 'data', file + '.json'))
    print("Modified image data and moved to final directory: ", file)
