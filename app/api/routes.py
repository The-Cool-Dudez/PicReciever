from app.api import bp
from app.models import Images
from app.db import db

from flask import request, current_app, jsonify, abort
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
from os.path import join

UPLOAD_FOLDER = "uploads/"

#get link for image
@bp.route('/get/<int:id>')
def get(id):
    image = Images.query.filter_by(id=id).first()
    if image is None:
        return jsonify({
            "status": "failure",
            "message": "No image with that id exists."
        })
    return jsonify({
        "status": "ok",
        "url": urljoin(request.base_url, "/static/" + image.path)
    })

#view image
@bp.route('/view/<int:id>')
def view(id):
    image = Images.query.filter_by(id=id).first()
    if image is None:
        abort(404)
    return current_app.send_static_file(join(UPLOAD_FOLDER, image.path))

@bp.route('/download/<int:id>')
def download():
    return ""

#upload image
@bp.route('/upload', methods=['POST'])
def image():
    if 'image' in request.files:
        f = request.files['image']
        if f.filename == '':
            return jsonify({
                "status": "failure",
                "message": "No file uploaded"
            })

        filename = secure_filename(f.filename)
        path = join(UPLOAD_FOLDER, filename)

        img = Images.query.filter_by(path=path).first()
        if img is not None:
            return jsonify({
                "status": "failure",
                "message": "File with that name already exists"
            })

        # add the file to the database
        image = Images(path)
        db.session.add(image)
        db.session.commit()
        f.save(join(current_app.root_path, "static", path)) #save the file

        return jsonify({"status": "ok"})
    return jsonify({"status": "failure"})
