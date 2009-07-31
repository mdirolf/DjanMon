import datetime
import string
import random
import mimetypes
import cStringIO as StringIO

from PIL import Image
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from pymongo.connection import Connection
from pymongo import DESCENDING
import gridfs

db = Connection().sms
fs = gridfs.GridFS(db)
page_size = 10

def _generate_filename(name):
    """Generate a unique filename to use for GridFS, using a given name.

    Just appends some random characters before the file extension and
    checks for uniqueness.
    """
    filename = name.rsplit(".", 1)
    filename[0] = "%s-%s" % (filename[0],
                             "".join(random.sample(string.letters + string.digits, 10)))
    filename = ".".join(filename)

    # Try again if this filename already exists
    try:
        fs.open(filename, "r")
        return _generate_filename(name)
    except IOError:
        return filename

def index(request, page=0):
    if request.method == 'POST':
        if 'nickname' not in request.POST or 'text' not in request.POST:
            return HttpResponseRedirect("/")

        message = {"nickname": request.POST['nickname'],
                   "text": request.POST['text'],
                   "date": datetime.datetime.utcnow()}

        if "image" in request.FILES:
            filename = _generate_filename(request.FILES['image'].name)

            # Only accept appropriate file extensions
            if not filename.endswith((".jpg", ".JPG", ".jpeg", ".JPEG", ".png",
                                      ".PNG", ".bmp", ".BMP", ".gif", ".GIF")):
                raise web.seeother("/")

            message["image"] = filename

            # Save fullsize image
            image = request.FILES['image'].read()
            full = fs.open(filename, "w")
            full.write(image)
            full.close()

            # Save thumbnail
            thumb = fs.open(filename, "w", "thumb")
            image = Image.open(StringIO.StringIO(image))
            image.thumbnail((80, 60), Image.ANTIALIAS)
            data = StringIO.StringIO()
            image.save(data, image.format)
            thumb.write(data.getvalue())
            thumb.close()
            data.close()

        db.messages.insert(message)
        return HttpResponseRedirect("/")
    else:
        page = int(page)

        previous = "hack"
        if page > 0:
            previous = page - 1

        next = "hack"
        if db.messages.count() > (page + 1) * page_size:
            next = page + 1

        messages = db.messages.find().sort("date", DESCENDING).limit(page_size).skip(page * page_size)
        return render_to_response('status/index.html', {'messages': messages,
                                                        'previous': previous,
                                                        'next': next})

def file(request, collection_or_filename, filename=None):
    if filename is not None:
        f = fs.open(filename, "r", collection_or_filename)
    else:
        f = fs.open(collection_or_filename, "r")
    data = f.read()
    mimetype = f.content_type or mimetypes.guess_type(filename or collection_or_filename)
    f.close()
    return HttpResponse(data, mimetype=mimetype)
