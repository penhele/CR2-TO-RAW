#!/usr/bin/env python

# import what we need
import numpy as np
import os
import glob
import time
import argparse
from PIL import Image
import rawpy

# params
parser = argparse.ArgumentParser(description='Convert CR2 to JPG')
parser.add_argument('-s', '--source', help='Source folder of CR2 files', required=True)
parser.add_argument('-d', '--destination', help='Destination folder for converted JPG files', required=True)
args = parser.parse_args()

# dirs and files
raw_file_type = ".CR2"
raw_dir = os.path.abspath(args.source) + '/'
converted_dir = os.path.abspath(args.destination) + '/'
raw_images = glob.glob(raw_dir + '*' + raw_file_type)

# converter function which iterates through list of files
def convert_cr2_to_jpg(raw_images):
    for raw_image in raw_images:
        print(f"Converting the following raw image: {raw_image} to JPG")

        # file vars
        file_name = os.path.basename(raw_image)
        file_without_ext = os.path.splitext(file_name)[0]
        file_timestamp = os.path.getmtime(raw_image)

        # parse CR2 image
        with rawpy.imread(raw_image) as raw:
            rgb = raw.postprocess()

            # prep JPG details
            jpg_image_location = os.path.join(converted_dir, file_without_ext + '.jpg')
            img = Image.fromarray(rgb)
            img.save(jpg_image_location, format="jpeg")

            # update JPG file timestamp to match CR2
            os.utime(jpg_image_location, (file_timestamp, file_timestamp))

            # close to prevent too many open files error
            img.close()

# call function
if __name__ == "__main__":
    # Create destination directory if it does not exist
    if not os.path.exists(converted_dir):
        os.makedirs(converted_dir)

    convert_cr2_to_jpg(raw_images)
