from camera_handler import CameraHandler

# a script to take pictures in all cameras in a range of focus values

f_start = 10
f_end = 1000
f_step = 10

camera = CameraHandler()


def take_pictures(camera_id):
    camera.change_active_camera(camera_id)
    for f in range(f_start,f_end,f_step):
        camera.change_focus(f)
        print(f"taking image. camera:{camera_id} focus:{f}")
        camera.take_pic("focus_test")


take_pictures("A")
take_pictures("B")
take_pictures("C")
take_pictures("D")



