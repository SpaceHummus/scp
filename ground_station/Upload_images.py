import sys
sys.path.insert(1, '../common')
from gdrive_handler import GDriveHandler
import logging
import sys
from datetime import datetime
import os

def Upload_images_to_drive(gDrive_folder_ID, local_folder):
    g_drive_handler = GDriveHandler(gDrive_folder_ID)

    processed_images_folder_id = g_drive_handler.get_folder_id("11 Processed Images", gDrive_folder_ID)
    print("Processed images folder id: ", processed_images_folder_id)

    for file in os.listdir(local_folder + "Merged_images"):
        print("Uploading file:", local_folder + "Merged_images/" + file, "to GDrive (folder 11)")
        g_drive_handler.upload_file(local_folder + "Merged_images/" + file, file, processed_images_folder_id)
    for file in os.listdir(local_folder):
        if file.endswith(".avi"):
            print("Uploading movie: ", local_folder + file, " to GDrive (folder 11)")
            g_drive_handler.upload_file(local_folder + file, file, processed_images_folder_id)


# Upload_images_to_drive("1z6weX9LhJIZ8iZd_F1t-uAKWvTeuineh", "C:/Users/GAL/Desktop/Space_Hummus/Images/cycle1/")
GDrive_folder_id = sys.argv(1)
local_folder = sys.argv(2)

Upload_images_to_drive(GDrive_folder_id, local_folder)

# Usage example:
# python Upload_images.py "1z6weX9LhJIZ8iZd_F1t-uAKWvTeuineh" "C:/Users/GAL/Desktop/Space_Hummus/Images/cycle1/"