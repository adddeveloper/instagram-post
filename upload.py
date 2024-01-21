import os
import random
from instagrapi import Client
import time
import shutil
import mimetypes

caption = ''

# Prompt user to choose an account
usninput = input("Which account do you want to upload to?\nEnter the number: ")

# Dictionary containing account information
accounts = {
    '1': {
        'username': 'your instagram username',
        'password': 'your password',
        'media_folder': 'folder of content'
    }
}

# Check if the chosen account is valid
if usninput in accounts:
    chosen_account = accounts[usninput]
else:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

client = Client()
client.login(chosen_account['username'], chosen_account['password'])

if not os.path.exists('done'):
    os.makedirs('done')

media_folder = chosen_account['media_folder']
random_number = int(input("wait time (minutes): "))

while True:
    dir_list = [d for d in os.listdir(media_folder) if os.path.isdir(os.path.join(media_folder, d)) and d not in ('done', 'sites')]

    if not dir_list:
        print("No folders left.")
        break

    chosen_dir = random.choice(dir_list)
    file_list = os.listdir(os.path.join(media_folder, chosen_dir))

    if not file_list:
        dir_list.remove(chosen_dir)
        continue

    file_name = random.choice(file_list)
    file_path = os.path.join(media_folder, chosen_dir, file_name)
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        media_type = mime_type.split('/')[0]

        if media_type in ('image', 'video'):
            if media_type == 'image':
                client.photo_upload(file_path, caption=caption)
            elif media_type == 'video':
                client.video_upload(file_path, caption=caption)
            print("~~~~~~~~~~~~~~~~~~~~~~ new upload ~~~~~~~~~~~~~~~~~~~~~~")
            print("Uploaded: ", file_name)
            print("\n\n It will take: ", random_number, "minute(s) to upload.")
            time.sleep(random_number * 60)
