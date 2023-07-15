import sys
import os
import shutil
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import argparse

def backup_folder(source_path, destination_path, compress=True):
    # Create a timestamp for the backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Get the current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if the destination path already exists
    if os.path.exists(destination_path):
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))

    # Create the backup folder if it doesn't exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Get a list of all the files and folders in the source path
    file_list = os.listdir(source_path)

    # Create a list of files and folders to be backed up
    backup_list = []

    # Iterate through each file and folder in the source path
    for file_name in file_list:
        file_path = os.path.join(source_path, file_name)

        # Check if the file is a folder
        if os.path.isdir(file_path):
            # Recursively call this function for each subfolder
            backup_list += backup_folder(file_path, destination_path, compress)
        else:
            # Check if the file already exists in the backup folder
            if file_name in os.listdir(destination_path):
                # If the file already exists, compare the timestamps
                if os.path.getmtime(file_path) == os.path.getmtime(os.path.join(destination_path, file_name)) and \
                   os.path.getatime(file_path) == os.path.getatime(os.path.join(destination_path, file_name)) and \
                   os.path.getctime(file_path) == os.path.getctime(os.path.join(destination_path, file_name)):
                    # If the timestamps are the same, compare the file sizes
                    if os.path.getsize(file_path) == os.path.getsize(os.path.join(destination_path, file_name)):
                        # If the file sizes are the same, the backups are identical, so skip the backup
                        continue
                else:
                    # If the timestamps are different, or the file sizes are different, copy the file to the backup folder
                    shutil.copy2(file_path, destination_path)
                    backup_list.append(file_name)

    # Compose the email message
    email_message = MIMEMultipart()
    email_message['From'] = 'you@example.com'
    email_message['To'] = 'recipient@example.com'
    email_message['Subject'] = 'Backup completed at ' + current_time

    # Add the backup file list to the email message
    attachment = MIMEApplication(backup_list, _subtype='txt')
    attachment.add_header('Content-Disposition)