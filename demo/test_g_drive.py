# pip3 install pydrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

file_id = ""
gauth = GoogleAuth()      
# gauth.CommandLineAuth() # need this only one time per user, after that credentials are stored in credentials.json     
drive = GoogleDrive(gauth)
folder_id = "1usWtERCev43R107ccgdIZG83ORlwGnyB"
file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
for f in file_list:
    print('title: %s, id: %s' % (f['title'], f['id']))
    title = f['title']
    if title == "01 Commands":
        folder_id = f['id']
        file_list2 = drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
        for i in file_list2:
            print('title: %s, id: %s' % (i['title'], i['id']))
            title = i['title']
            if title == "logic_states.yaml":
                file_id = i['id']

file = drive.CreateFile({'id': file_id})
file.GetContentFile('logic_states.yaml') 
