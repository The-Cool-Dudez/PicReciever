from app.api import bp

from app.models import Images
from urllib.parse import urljoin

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
            return dumps({"status": "failure"})
        print(f)
        image = Images("images/" + f.filename)
        db.session.add(image)
        db.session.commit()
        return dumps({"status": "ok"})
    return dumps({"status": "failure"})
