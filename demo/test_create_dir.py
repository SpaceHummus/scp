from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() 
drive = GoogleDrive(gauth)
folder_id = '1TeYo5TB0DSDe4QAPa_7Wjta79ZxSd4pQ'

file_metadata = {
  'title': 'Ella',
  'parents':  [{'id': folder_id}],
  'mimeType': 'application/vnd.google-apps.folder'
}

folder = drive.CreateFile(file_metadata)
folder.Upload()




