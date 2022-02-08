import sys

GDrive_folder = sys.argv[1]
Local_folder = sys.argv[2]
First_image_time = sys.argv[3]
Last_image_time = sys.argv[4]
Exp_start_time = sys.argv[5]
Cameras_list = sys.argv[6]
Focus_list = sys.argv[7]

print("input 1 before deleting ?: GDrive_folder: ", GDrive_folder)
if GDrive_folder[0] == "?":
    GDrive_folder = GDrive_folder[1:]
if GDrive_folder[-1] == "?":
    GDrive_folder = GDrive_folder[:len(GDrive_folder)-1]
print("input 1 after deleting ?: GDrive_folder: ", GDrive_folder)

print("input 3 before deleting ?: First_image_time: ", First_image_time)
if First_image_time[0] == "?":
    First_image_time = First_image_time[1:]
if First_image_time[-1] == "?":
    First_image_time = First_image_time[:len(First_image_time)-1]
print("input 3 after deleting ?: First_image_time: ", First_image_time)

print("input 4 before deleting ?: Last_image_time: ", Last_image_time)
if Last_image_time[0] == "?":
    Last_image_time = Last_image_time[1:]
if Last_image_time[-1] == "?":
    Last_image_time = Last_image_time[:len(Last_image_time)-1]
print("input 4 after deleting ?: Last_image_time: ", Last_image_time)

print("input 5 before deleting ?: Exp_start_time: ", Exp_start_time)
if Exp_start_time[0] == "?":
    Exp_start_time = Exp_start_time[1:]
if Exp_start_time[-1] == "?":
    Exp_start_time = Exp_start_time[:len(Exp_start_time)-1]
print("input 5 after deleting ?: Exp_start_time: ", Exp_start_time)


# python download_images.py GDrive_folder First_image_time Last_image_time Cameras_list Focus_list Local_folder

# python Process_images.py Local_folder Exp_start_time Cameras_list

# python Upload_images.py GDrive_folder Local_folder
