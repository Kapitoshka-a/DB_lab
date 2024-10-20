from flask import Flask
from instagram.auth.controller.user_controller import user_bp
from instagram.auth.route import init_routes

app = Flask(__name__)

# Ініціалізуємо маршрути
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
