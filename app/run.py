from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.tarea_controller import task_bp
from controllers.user_controller import worker_bp
from flask_swagger_ui import get_swaggerui_blueprint
from database import db

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Tareas API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(task_bp, url_prefix="/api")
app.register_blueprint(worker_bp, url_prefix="/api")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)