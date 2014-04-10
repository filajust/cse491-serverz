# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image, imageapp_sql

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
    # image.load_images()

    # add_test_image()
    load_images()
    # some_data = open('imageapp/dice.png', 'rb').read()
    # image.add_image(some_data, 'png')

# Add some default images
def add_test_image():
    some_data = open('imageapp/dice.png', 'rb').read()
    img = image.create_image_dict(data = some_data, fileName = "dice.png",\
    description = "Dice")
    image.add_image(img, 'png')
    '''
    commentForm = {'i': 0, 'user': 'Justin', 'comment': 'testing'}
    image.add_comment(commentForm)
    '''

def teardown():                         # stuff that should be run once.
    pass

def load_images():
    imageDictList = imageapp_sql.load_all_images()
    for imgDict in imageDictList:
        image.load_images(imgDict)
