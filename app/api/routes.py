from app.api import bp

@bp.route('get/<int:id>')
def get(id):
    return ""
