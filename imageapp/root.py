import os
import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticDirectory

from . import html, image

class RootDirectory(Directory):
    _q_exports = ['static']
    static = StaticDirectory(os.path.join(os.path.dirname(__file__),'static'))

    @export(name='')                    # this makes it public.
    def index(self):
        # return html.render('index.html')
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print 'request.form.keys(): ', request.form.keys()

        the_file = request.form['file']
        # print dir(the_file)
        # print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))
        datatype = the_file.base_filename.split('.')[-1]

        image.add_image(data, datatype)
        # return html.render('index.html')
        return html.render('index.html')
        # TODO: actually redirect
        # return quixote.redirect('/')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        item = image.get_latest_image()
        response.set_content_type(item[1])
        return item[0] 
