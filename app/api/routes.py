from app.api import bp
from app.models import Images
from app.db import db

from flask import request, current_app
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
from os.path import join
from json import dumps

UPLOAD_FOLDER = "uploads/"

#get link for image
@bp.route('/get/<int:id>')
def get(id):
    image = Images.query.filter_by(id=id).first()
    if image is None:
        return ""
    print(request.base_url)
    return urljoin(request.base_url + "/" + image.path)

#view image
@bp.route('/view/<int:id>')
def view(id):
    return ""

@bp.route('/download/<int:id>')
def download():
    return ""

#upload image
@bp.route('/upload', methods=['POST'])
def image():
    if 'image' in request.files:
        f = request.files['image']
        if f.filename == '':
            return dumps({
                "status": "failure",
                "message": "No file uploaded"
            })

        filename = secure_filename(f.filename)
        path = join(UPLOAD_FOLDER, filename)

        img = Images.query.filter_by(path=path).first()
        if img is not None:
            return dumps({
                "status": "failure",
                "message": "File with that name already exists"
            })

        # add the file to the database
        image = Images(path)
        db.session.add(image)
        db.session.commit()
        f.save(join(current_app.root_path, "static", path)) #save the file

        return dumps({"status": "ok"})
    return dumps({"status": "failure"})
