'''
Script to copy images with horizontal orientation from a source folder to a destination folder.

Usage:
python copy_horizontal_images.py <source_folder> <destination_folder>
'''
import os
import shutil
import argparse
from PIL import Image

def copy_horizontal_images(source_folder, destination_folder):
    '''
    Copies images with horizontal orientation from source_folder to destination_folder.
    Only processes .jpg, .jpeg, and .png files.
    '''
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder: {destination_folder}")

    copied_files = 0
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        if not os.path.isfile(source_path):
            continue

        file_ext = filename.lower().split('.')[-1]
        if file_ext not in ['jpg', 'jpeg', 'png']:
            continue

        try:
            with Image.open(source_path) as img:
                width, height = img.size
                if width > height:
                    destination_path = os.path.join(destination_folder, filename)
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: {filename}")
                    copied_files += 1
                else:
                    print(f"Skipped (vertical/square): {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print(f"\nFinished. Copied {copied_files} horizontal images to {destination_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy horizontal JPG and PNG images from a source to a destination folder."
    )
    parser.add_argument("source_folder", help="Path to the source folder containing images.")
    parser.add_argument("destination_folder", help="Path to the destination folder for horizontal images.")

    args = parser.parse_args()

    if not os.path.isdir(args.source_folder):
        print(f"Error: Source folder '{args.source_folder}' not found.")
    else:
        copy_horizontal_images(args.source_folder, args.destination_folder)
