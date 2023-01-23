import json
import piexif
import datetime
import os

from engines.util import degToDmsRational, move_completed_files

SUPPORTED_FILE_TYPES = ['jpg']


def process_image(media_path, data_path, final_path, file):
    print(f"Running process_image for file: {file} with supported file types: {SUPPORTED_FILE_TYPES}")
    media_data = json.load(open(os.path.join(data_path, file + '.json')))
    data_title = media_data.get('title', '')
    data_photo_time = media_data.get('photoTakenTime', '')
    data_location = media_data.get('geoData', '')
    print(data_title, data_photo_time, data_location)

    exif_dict = piexif.load(os.path.join(media_path, file))
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

    # print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, os.path.join(media_path, file))

    move_completed_files(media_path, data_path, final_path, file)
