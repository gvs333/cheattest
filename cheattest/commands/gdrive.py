import os
import glob
from typing import List, Set

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from oauth2client.service_account import ServiceAccountCredentials

from cheattest.commands.base import BaseCommand
from cheattest.constants import IMAGES_DIR
from cheattest.utils import Utils


class DriveBaseCommand(BaseCommand):
    DRIVE_SCOPE = ["https://www.googleapis.com/auth/drive"]

    def __init__(self,
                 drive_api_json_path: str,
                 drive_dir_name: str,
                 **kwargs):
        drive_api_json_path = Utils.resolve_path(drive_api_json_path)

        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            drive_api_json_path,
            self.DRIVE_SCOPE
        )
        self.drive = GoogleDrive(gauth)

        # get folder with images and answers
        query = {
            'q': f"trashed=False and title='{drive_dir_name}'"
                 "and mimeType='application/vnd.google-apps.folder'"
        }
        file_list: List[GoogleDriveFile] = self.drive.ListFile(query).GetList()

        if not file_list:
            raise Exception(f"Not found folder {drive_dir_name} on gdrive.")

        self.folder_id: str = file_list[0]['id']


class SyncImagesCommand(DriveBaseCommand):
    """Syncs local images with google Drive."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_images_gdrive_query = {
            'q': f"'{self.folder_id}' in parents and trashed=false "
                 "and mimeType='image/jpeg'"
        }

    def do(self):
        local_images_paths = set(glob.glob(os.path.join(IMAGES_DIR, "*.jpeg")))

        remote_images_list: List[GoogleDriveFile] = self.drive.ListFile(self.remote_images_gdrive_query).GetList()
        remote_images_names_set: Set[str] = set(file['title'] for file in remote_images_list)

        for local_image in local_images_paths:
            if os.path.basename(local_image) in remote_images_names_set:
                continue

            gdrive_file_obj = self.drive.CreateFile({
                'title': os.path.basename(local_image),
                'mimeType': 'image/jpeg',
                'parents': [{'id': self.folder_id}]
            })
            gdrive_file_obj.SetContentFile(local_image)
            gdrive_file_obj.Upload()


class SyncRemoteAnswersCommand(DriveBaseCommand):
    """Downloads remote answers from Gdrive and overrides local ones."""

    def __init__(self,
                 answers_remote_filename: str,
                 answers_local_filepath: str,
                 **kwargs):
        super().__init__(**kwargs)
        self.local_answers_path = Utils.resolve_path(answers_local_filepath)
        self.answers_gdrive_query = {
            'q': f"'{self.folder_id}' in parents and trashed=false "
                 f"and title='{answers_remote_filename}'"
        }

    def do(self):
        result_list: List[GoogleDriveFile] = self.drive.ListFile(self.answers_gdrive_query).GetList()

        if not result_list:
            return

        answers_fileobj = result_list[0]
        content: str = answers_fileobj.GetContentString()

        with open(self.local_answers_path, 'w') as f:
            f.write(content)
