from abc import abstractmethod
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# create a new folder in G-Drive
# title - The name of the folder
# folder_id - The G-Drive parent folder id
# return - True if sucess otherwise False
def create_folder(title,folder_id):
  try: 
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() 
    drive = GoogleDrive(gauth)

    file_metadata = {
      'title': title,
      'parents':  [{'id': folder_id}],
      'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    return True
  except:
    return False

def test(n1,n2):
  try:
    return n1//n2
  except:
    print("ERROR divided by zero")
    return False

f_id = '1TeYo5TB0DSDe4QAPa_7Wjta79ZxSd4pQ'
name = 'Ella22'


if create_folder(name,f_id):
  print("Sucess")
else:
  print("No Sucess")