from flask import request
from app.api import bp
from werkzeug.utils import secure_filename

from app.models import Images
from app.db import db
from urllib.parse import urljoin
from os.path import join

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

        print(f)
        img = Images.query.filter_by(path=path).first()
        if img is not None:
            return dumps({
                "status": "failure",
                "message": "File with that name already exists"
            })

        image = Images(path)
        db.session.add(image)
        db.session.commit()
        f.save(path)
        return dumps({"status": "ok"})
    return dumps({"status": "failure"})
