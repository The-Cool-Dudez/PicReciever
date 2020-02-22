from app.api import bp
from app.models import Images
from app.db import db

from flask import request, current_app, jsonify, abort
from werkzeug.utils import secure_filename
from urllib.parse import urljoin
from os.path import join
from json import dumps

UPLOAD_FOLDER = "uploads/"

def get_image_url(path):
    return urljoin(request.base_url, "/static/" + path)

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
        "url": get_image_url(image.path)
    })

#view image
@bp.route('/view/<int:id>')
def view(id):
    image = Images.query.filter_by(id=id).first()
    if image is None:
        abort(404)
    return current_app.send_static_file(image.path)

@bp.route('/download/<int:id>')
def download():
    return ""

@bp.route('/images')
def images():
    images = Images.query.all()
    images_json = {"images": []}
    for image in images:
        images_json["images"].append({
            "id": image.id,
            "url": get_image_url(image.path)
        })
    return jsonify(images_json)

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
