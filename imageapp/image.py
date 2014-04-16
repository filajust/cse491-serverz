# image handling API
from . import imageapp_sql
from time import time, strftime

# store it as a list
images = []

def add_image(image, datatype):
    # print 'images.keys() again', images.keys()
    if images:
        image_num = len(images)
        #image_num = max(images.keys()) + 1
    else:
        image_num = 0

    # images[image_num] = data, datatype
    images.append(image)
    imageapp_sql.insert(image)
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    # image_num = max(images.keys())
    image_num = len(images) - 1
    if image_num < 0:
        return None
    else:
        return images[image_num]

def get_image_num():
    return len(images)
    # return max(images.keys())

def load_images(aDict):
    img = create_image_dict(data = aDict["data"], fileName = aDict["file_name"],
                                               description = aDict["description"])
    images.append(img)

def create_image_dict(data = "", fileName = "dice.png", 
    description = "No description available"):
    img = {"data" : data}
    img["file_name"] = fileName
    img["description"] = description
    img["commentList"] = []
    img["thumbnail"] = "" 
                            
    return img

def add_comment(img, comment):
    commentList = img["commentList"]
    commentList.append(comment)
    img["commentList"] = commentList

    return img 

def get_comments(img):
    return img["commentList"]
