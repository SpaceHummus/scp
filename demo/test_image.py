from PIL import Image
def image_weight(filename):
    image_file = Image.open(filename)
    print("File Size In Bytes:- "+str(len(image_file.fp.read())))






image_weight("21-10-03__06_37_CD_F0160.jpg")