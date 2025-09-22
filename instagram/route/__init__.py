from instagram.controller.procedure_controller import comment_bp
from instagram.controller.user_controller import user_bp


def init_routes(app):
    app.register_blueprint(user_bp, url_prefix='/app')
    app.register_blueprint(comment_bp, url_prefix='/procedures')

