from flask import request
from json import dumps
from app.models import Images


from . import bp

#upload image
@bp.route('/image', methods=['POST'])
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
