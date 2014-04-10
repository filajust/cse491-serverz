# image handling API

images = {}

def add_image(data, datatype):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    images[image_num] = data, datatype
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def get_image_num():
    return max(images.keys())
