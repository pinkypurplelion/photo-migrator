import filedate
import shutil
import os
import json
import datetime

SUPPORTED_FILE_TYPES = ['mp4', 'mov']

def process_image(media_path, data_path, final_path, file):
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

    shutil.move(os.path.join(media_path, file), os.path.join(final_path, 'media', file))
    shutil.move(os.path.join(data_path, file + '.json'), os.path.join('final', 'data', file + '.json'))
    print("Modified image data and moved to final directory: ", file)
    print('t')
