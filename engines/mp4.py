import filedate
import os
import json
import datetime

from engines.util import move_completed_files

SUPPORTED_FILE_TYPES = ['mp4', 'mov']


def process_image(media_path, data_path, final_path, file):
    print(f"Running process_image for file: {file} with supported file types: {SUPPORTED_FILE_TYPES}")
    file_date = filedate.File(os.path.join(media_path, file))

    # Get file date
    file_date.get()

    media_data = json.load(open(os.path.join(data_path, file + '.json')))  # change to data dir for production

    data_photo_time = media_data.get('photoTakenTime', '')

    dt = datetime.datetime.fromtimestamp(int(data_photo_time['timestamp']))
    dt_str = dt.strftime("%d.%m.%Y %H:%M")
    print('Modifying file: ', file, dt_str)

    # Set file date
    file_date.set(
        created=dt_str,
        modified=dt_str,
        accessed=dt_str
    )

    move_completed_files(media_path, data_path, final_path, file)
